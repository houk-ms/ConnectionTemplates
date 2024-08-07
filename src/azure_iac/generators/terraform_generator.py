from azure_iac.payloads.binding import Binding
from azure_iac.payloads.payload import Payload
from azure_iac.payloads.resource import Resource
from azure_iac.payloads.resources.useridentity import UserIdentityResource
from azure_iac.payloads.models.connection_type import ConnectionType
from azure_iac.payloads.models.resource_type import ResourceType

from azure_iac.terraform_engines import engine_factory
from azure_iac.terraform_engines.main_engine import MainEngine
from azure_iac.terraform_engines.blocks_engine import BlocksEngine
from azure_iac.terraform_engines.modules.resource_engines.resourcegroup_engine import ResourceGroupEngine
from azure_iac.terraform_engines.readme_engine import ReadMeEngine

from azure_iac.generators.base_generator import BaseGenerator
from azure_iac.handlers.terraform_binding_handler import TerraformBindingHandler
from azure_iac.helpers import file_helper


class TerraformGenerator(BaseGenerator):
    def __init__(self, payload: Payload):
        super().__init__(payload)
        
        # engines for each resource deployments
        self.resource_engines = []
        # engines for each target resource's filrewall settings
        # split from resource_engines to avoid circular dependency
        self.firewall_engines = []
        # engine for each role assignment
        self.role_engines = []
        # engines for each key vault secret
        self.key_vault_secret_engines = []
        # engines for dependent resource deployments
        self.dependency_engines = []
        # engines for main parameters
        self.variable_engines = []
        # engines for main outputs
        self.output_engines = []


    def complete_payloads(self):
        super().complete_payloads()

        useridentity_resource = UserIdentityResource()
        is_existing_user_identity = False
        has_user_identity = False
        for resource in self.payload.resources:
            if resource.type == ResourceType.AZURE_USER_IDENTITY:
                is_existing_user_identity = True
                useridentity_resource = resource
                break

        for binding in self.payload.bindings:
            if binding.connection == ConnectionType.USERIDENTITY:
                has_user_identity = True
        
        if not is_existing_user_identity and has_user_identity:
            self.payload.resources.append(useridentity_resource)

    def add_implicit_bindings(self):
        # when binding store is keyvault, add implicit binding for source to keyvault
        for binding in self.payload.bindings:
            if binding.store is not None and binding.store.type == ResourceType.AZURE_KEYVAULT:
                implicit_binding = Binding()
                implicit_binding.source = binding.source
                implicit_binding.target = binding.store
                implicit_binding.connection = ConnectionType.SYSTEMIDENTITY
                
                # check duplicated binding
                existing_bingdings = [binding.get_identifier() for binding in self.payload.bindings]
                if implicit_binding.get_identifier() not in existing_bingdings:
                    self.payload.bindings.append(implicit_binding)

    def init_resource_engines(self):
        # Create engine for resource group
        self.resource_engines.append(ResourceGroupEngine())

        # Create engines for each resource deployments
        for resource in self.payload.resources:
            resource_engine = engine_factory.get_resource_engine_from_type(resource.type)
            self.resource_engines.append(resource_engine(resource))
            
            # create firewall engines for target resources if they are as the binding targets
            if resource in [binding.target for binding in self.payload.bindings]:
                firewall_engine = engine_factory.get_firewall_engine_from_type(resource.type)
                # target may not support separated firewall settings
                if firewall_engine is not None:
                    self.firewall_engines.append(firewall_engine(resource))

            # create role engines for target resources if they are as the binding targets
            # and the connection is system identity or user identity
            if resource in [binding.target for binding in self.payload.bindings \
                            if binding.connection == ConnectionType.SYSTEMIDENTITY or binding.connection == ConnectionType.USERIDENTITY]:
                role_engine = engine_factory.get_role_engine()
                self.role_engines.append(role_engine(resource))

            # create key vault secret engines for target resources if they are as the binding targets
            # and the connection is using secret store
            # assume one secret for one binding
            if resource in [binding.target for binding in self.payload.bindings \
                            if binding.connection == ConnectionType.SECRET \
                            and binding.store is not None and binding.store.type == ResourceType.AZURE_KEYVAULT]:
                key_vault_secret_engine = engine_factory.get_key_vault_secret_engine()
                self.key_vault_secret_engines.append(key_vault_secret_engine(resource))


    def init_dependency_engines(self):
        # Create dependency engines from each resource engine
        for engine in self.resource_engines:
            # TODO: may do it recursively in the future
            # now dependency engines don't have dependencies
            self.dependency_engines.extend(engine.get_dependency_engines())

        # dependency engines should be singleton, so that multiple instances of same resource type 
        # can share the same dependency resource. we may allow multiple dependency instances of the
        # same type in the future
        self.dependency_engines = self._dedup_engines_by_type(self.dependency_engines)


    def init_variable_engines(self):
        # Create param engines from each resource engine
        engines = self.resource_engines \
            + self.dependency_engines \
            + self.firewall_engines \
            + self.role_engines \
            + self.key_vault_secret_engines
        for engine in engines:
            self.variable_engines.extend(engine.get_variable_engines())
        

    def init_output_engines(self):
        # Create output engines from each resource engine
        engines = self.resource_engines \
            + self.dependency_engines \
            + self.firewall_engines \
            + self.role_engines \
            + self.key_vault_secret_engines
        for engine in engines:
            self.output_engines.extend(engine.get_output_engines())
        self.output_engines = self._dedup_engines_by_name(self.output_engines)
 

    def process_bindings(self):
        # process bindings and engines
        for binding in self.payload.bindings:
            binding_handler = TerraformBindingHandler(binding, 
                self._get_resource_engine_by_resource(binding.source), 
                self._get_resource_engine_by_resource(binding.target), 
                self._get_role_engine_by_resource(binding.target),
                self._get_firewall_engine_by_resource(binding.target),
                self._get_key_vault_secret_engine_by_resource(binding.target),
                self._get_user_identity_engine())  #TODO: cannot customize user identity
            binding_handler.process_engines()


    def generate_terraforms(self, output_folder: str):
        # generate main.tf file (only include compute resources)
        main_engine = MainEngine()
        source_engines = [engine for engine in self.resource_engines 
                          if (not engine.resource or engine.resource.type.is_compute())]
        main_engine.resources = [engine.render() for engine in source_engines]
        file_helper.create_file('{}/main.tf'.format(output_folder), main_engine.render())

        # generate <target>.tf files for target and dependency engines
        target_engines = [engine for engine in (
                self.resource_engines + 
                self.firewall_engines + 
                self.role_engines +
                self.key_vault_secret_engines +
                self.dependency_engines) if engine not in source_engines]
        target_engine_map = dict()
        for engine in target_engines:
            if engine.template not in target_engine_map:
                target_engine_map[engine.template] = []
            target_engine_map[engine.template].append(engine)
        
        for template, engines in target_engine_map.items():
            targets_engine = BlocksEngine()
            targets_engine.blocks = [engine.render() for engine in engines]
            tf_file_name = template.split('/')[-1].replace('.jinja', '')
            file_helper.create_file('{}/{}'.format(output_folder, tf_file_name), targets_engine.render())

        # generate variables.tf file
        variables_engine = BlocksEngine()
        variables_engine.blocks = [engine.render() for engine in self.variable_engines]
        file_helper.create_file('{}/variables.tf'.format(output_folder), variables_engine.render())

        # generate outputs.tf file
        outputs_engine = BlocksEngine()
        outputs_engine.blocks = [engine.render() for engine in self.output_engines]
        file_helper.create_file('{}/outputs.tf'.format(output_folder), outputs_engine.render())


    def generate_readme(self, output_folder: str):
        
        # generate readme file
        readme_engine = ReadMeEngine()
        for engine in self.resource_engines:
            if engine.resource is not None:
                readme_engine.resources.append(engine.resource.type.value)

        file_helper.create_file('{}/README.md'.format(output_folder), readme_engine.render_template())


    def generate(self, output_folder: str='./'):
        self.init_resource_engines()
        self.init_dependency_engines()
        self.process_bindings()
        self.init_variable_engines()
        self.init_output_engines()
        self.generate_terraforms(output_folder)
        self.generate_readme(output_folder)

    def _get_resource_engine_by_resource(self, resource: Resource):
        # TODO: support engine identifier
        for engine in self.resource_engines:
            if engine.resource == resource:
                return engine
        return None

    def _get_role_engine_by_resource(self, resource: Resource):
        # TODO: different role to same resource
        for engine in self.role_engines:
            if engine.resource == resource:
                return engine
        return None

    def _get_firewall_engine_by_resource(self, resource: Resource):
        for engine in self.firewall_engines:
            if engine.resource == resource:
                return engine
        return None
    
    def _get_key_vault_secret_engine_by_resource(self, resource: Resource):
        for engine in self.key_vault_secret_engines:
            if engine.resource == resource:
                return engine
        return None
    
    def _get_user_identity_engine(self):
        for engine in self.resource_engines:
            if engine.resource and engine.resource.type == ResourceType.AZURE_USER_IDENTITY:
                return engine
        return None
    
    def _dedup_engines_by_name(self, engine_list):
        deduped = []
        for engine in engine_list:
            if engine.name not in [e.name for e in deduped]:
                deduped.append(engine)
        return deduped

    def _dedup_engines_by_type(self, engine_list):
        # only one engine is kept for each resource and engine type
        engine_dict = dict()
        for engine in engine_list:
            engine_name = engine.__class__.__name__
            if engine_name not in engine_dict:
                engine_dict[engine_name] = []
            engine_dict[engine_name].append(engine)

        result = []
        for engines in engine_dict.values():
            deduped = []
            for engine in engines:
                if engine.resource.type not in [e.resource.type for e in deduped]:
                    deduped.append(engine)
            result.extend(deduped)
        
        return result
         