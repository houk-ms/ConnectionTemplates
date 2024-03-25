from generators.base_generator import BaseGenerator
from engines import engine_factory
from helpers import file_helper
from handlers.binding_handler import BindingHandler
from payloads.payload import Payload
from payloads.resource import Resource


class InfraGenerator(BaseGenerator):
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
    

    def init_resource_engines(self):
        # Create engines for each resource deployments
        for resource in self.payload.resources:
            resource_engine = engine_factory.get_resource_engine_from_type(resource.type)
            self.resource_engines.append(resource_engine(resource))
            if resource.type.is_compute() and resource in [binding.source for binding in self.payload.bindings]:
                setting_engine = engine_factory.get_setting_engine_from_type(resource.type)
                self.setting_engines.append(setting_engine(resource))


    def init_dependency_engines(self):
        # Create dependency engines from each resource engine
        for engine in self.resource_engines:
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
        for binding in self.payload.bindings:
            binding_handler =BindingHandler(binding, 
                                            self._get_resource_engine_by_resource(binding.source), 
                                            self._get_resource_engine_by_resource(binding.target), 
                                            self._get_resource_engine_by_resource(binding.store),
                                            self._get_setting_engine_by_resource(binding.source))
            binding_handler.process_engines()


    def generate_biceps(self, output_folder: str):
        # TODO: use jinja to generate the main.bicep file

        # generate main.bicep file
        main_bicep = ''
        for engine in self.param_engines:
            main_bicep += engine.render_template()
        main_bicep += '\n\n'
        for engine in self.dependency_engines:
            main_bicep += engine.render_module()
        for engine in self.resource_engines:
            main_bicep += engine.render_module()
        for engine in self.setting_engines:
            main_bicep += engine.render_module()
        for engine in self.output_engines:
            main_bicep += engine.render_template()
        file_helper.create_file('{}/main.bicep'.format(output_folder), main_bicep)
        
        # generate dependency bicep files
        # duplicated dependency engines does not matter as the bicep file will be overwritten
        for engine in self.dependency_engines:
            bicep_file_name = engine.bicep_template.split('/')[-1].replace('.jinja', '')
            file_helper.create_file('{}/{}'.format(output_folder, bicep_file_name), engine.render_bicep())

        # generate resource bicep files
        # duplicated resource engines does not matter as the bicep file will be overwritten
        for engine in self.resource_engines:
            bicep_file_name = engine.bicep_template.split('/')[-1].replace('.jinja', '')
            file_helper.create_file('{}/{}'.format(output_folder, bicep_file_name), engine.render_bicep())
        
        for engine in self.setting_engines:
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
        #TODO: use dict to dedup
        deduped = []
        for engine in engine_list:
            if engine.name not in [e.name for e in deduped]:
                deduped.append(engine)
        return deduped

    def _dedup_engines_by_type(self, engine_list):
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
         