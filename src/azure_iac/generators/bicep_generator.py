from azure_iac.payloads.payload import Payload
from azure_iac.payloads.resource import Resource
from azure_iac.payloads.binding import Binding
from azure_iac.payloads.models.resource_type import ResourceType
from azure_iac.payloads.models.connection_type import ConnectionType
from azure_iac.payloads.resources.keyvault import KeyVaultResource

from azure_iac.bicep_engines import engine_factory
from azure_iac.bicep_engines.main_engine import MainEngine

from azure_iac.generators.base_generator import BaseGenerator
from azure_iac.handlers.bicep_binding_handler import BicepBindingHandler
from azure_iac.helpers import file_helper


class BicepGenerator(BaseGenerator):
    def __init__(self, payload: Payload):
        super().__init__(payload)
        
        # engines for each resource deployments
        self.resource_engines = []
        # engines for each compute resource settings deployment
        # split from resource_engines to avoid circular dependency
        self.setting_engines = []
        # engines for dependent resource deployments
        self.dependency_engines = []
        # engines for main parameters
        self.param_engines = []
        # engines for main outputs
        self.output_engines = []
    
    def complete_payloads(self):
        # add a keyvault resource if secret binding exists and there is 
        # not a keyvault resource in the payload
        keyvault_resource = KeyVaultResource()
        is_existing_keyvault = False
        for resource in self.payload.resources:
            if resource.type == ResourceType.AZURE_KEYVAULT:
                is_existing_keyvault = True
                keyvault_resource = resource
                break
        
        has_secret_binding = False
        for binding in self.payload.bindings:
            # only application insights support secret connection without a key vault
            if binding.connection == ConnectionType.SECRET \
                and binding.target.type != ResourceType.AZURE_APPLICATION_INSIGHTS:
                binding.store = keyvault_resource
                has_secret_binding = True
        
        if not is_existing_keyvault and has_secret_binding:
            self.payload.resources.append(keyvault_resource)


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
        # Create engines for each resource deployments
        for resource in self.payload.resources:
            resource_engine = engine_factory.get_resource_engine_from_type(resource.type)
            self.resource_engines.append(resource_engine(resource))
            
            # create setting engines for compute resources if they are as the binding sources
            if resource.type.is_compute() and \
                resource in [binding.source for binding in self.payload.bindings]:
                setting_engine = engine_factory.get_setting_engine_from_type(resource.type)
                self.setting_engines.append(setting_engine(resource))


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


    def init_param_engines(self):
        # Create param engines from each resource engine
        for engine in self.resource_engines:
            self.param_engines.extend(engine.get_param_engines())

        for engine in self.dependency_engines:
            self.param_engines.extend(engine.get_param_engines())
        
        self.param_engines = self._dedup_engines_by_name(self.param_engines)
    

    def init_output_engines(self):
        # Create output engines from each resource engine
        for engine in self.resource_engines:
            self.output_engines.extend(engine.get_output_engines())
        
        for engine in self.dependency_engines:
            self.output_engines.extend(engine.get_output_engines())
        
        self.output_engines = self._dedup_engines_by_name(self.output_engines)
 

    def process_bindings(self):
        # process bindings and engines
        for binding in self.payload.bindings:
            binding_handler = BicepBindingHandler(binding, 
                self._get_resource_engine_by_resource(binding.source), 
                self._get_resource_engine_by_resource(binding.target), 
                self._get_resource_engine_by_resource(binding.store),
                self._get_setting_engine_by_resource(binding.source))
            binding_handler.process_engines()


    def generate_biceps(self, output_folder: str):
        delployment_engines = self.dependency_engines + self.resource_engines + self.setting_engines

        # generate main.bicep file
        main_engine = MainEngine()
        main_engine.params = [engine.render_template() for engine in self.param_engines]
        main_engine.outputs = [engine.render_template() for engine in self.output_engines]
        main_engine.deployments = [engine.render_module() for engine in delployment_engines]
        file_helper.create_file('{}/main.bicep'.format(output_folder), main_engine.render_template())
        
        # generate dependency bicep files
        # duplicated engines does not matter as the bicep file will be overwritten
        for engine in delployment_engines:
            bicep_file_name = engine.bicep_template.split('/')[-1].replace('.jinja', '')
            file_helper.create_file('{}/{}'.format(output_folder, bicep_file_name), engine.render_bicep())


    def generate(self, output_folder: str='./'):
        self.init_resource_engines()
        self.init_dependency_engines()
        self.init_param_engines()
        self.init_output_engines()
        self.process_bindings()
        self.generate_biceps(output_folder)


    def _get_resource_engine_by_resource(self, resource: Resource):
        # TODO: support engine identifier
        for engine in self.resource_engines:
            if engine.resource == resource:
                return engine
        return None

    def _get_setting_engine_by_resource(self, resource: Resource):
        for engine in self.setting_engines:
            if engine.resource == resource:
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
         