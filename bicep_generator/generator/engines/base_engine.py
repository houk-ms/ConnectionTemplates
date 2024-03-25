from models.connector import Connector

class BaseEngine():
    def __init__(self, connector):
        self.connector = connector
        self.dependency_bicep_files = []
        self.service_brand_name = ''

        self.main_params = []       # [(param_name, param_type, param_value)]

        self.module_symbolic_name = ''
        self.module_bicep_file = ''
        self.module_deployment_name = ''
        self.module_params = []     # [(param_name, param_value)]
        self.module_depends = '[]'

        self.existing_resource_symbolic_name = ''
        self.existing_resource_type = ''
        self.existing_resource_name = ''

        self.main_variables = []         # [(variable_name, variable_value)]

        self._parameter_template = \
"""{param_decorator}
param {param_name} {param_type} = {param_value}
"""


        self._variable_template = \
"""var {variable_name} = {variable_value}
"""

        self._module_template = \
"""module {module_symbolic_name} '{module_bicep_file}' = 「
    name: '{module_deployment_name}'
    params: 「
        {module_params}
    」
    dependsOn: {module_depends}
」
"""
        self._existing_resource_template = \
"""resource {existing_resource_symbolic_name} '{existing_resource_type}' existing = 「
    name: {existing_resource_name}
」
"""


    def generate_parameters(self):
        parameter_block = ''
        for param_name, praparam_type, param_value, param_decorator in self.main_params:
            parameter_template = self._parameter_template
            if param_value is None:
                parameter_template = parameter_template.replace(' = {param_value}', '')
            if param_decorator is None:
                parameter_template = parameter_template.replace('{param_decorator}\n', '')
            
            parameter_block += parameter_template.format(
                param_name = param_name,
                param_type = praparam_type,
                param_value = param_value,
                param_decorator = param_decorator
            )
        return parameter_block.replace('「', '{').replace('」', '}')


    def generate_variables(self):
        variable_block = ''
        for variable_name, variable_value in self.main_variables:
            variable_block += self._variable_template.format(
                variable_name = variable_name, 
                variable_value = variable_value
            )
        return variable_block.replace('「', '{').replace('」', '}')


    def generate_module(self):
        module_params = ''
        for name, value in self.module_params:
            module_params += '{}: {}\n        '.format(name, value)
        return self._module_template.format(
            module_symbolic_name = self.module_symbolic_name,
            module_bicep_file = self.module_bicep_file,
            module_deployment_name = self.module_deployment_name,
            module_params = module_params.strip(),
            module_depends = self.module_depends
        ).replace('「', '{').replace('」', '}')


    def generate_existing_resource(self):
        return self._existing_resource_template.format(
            existing_resource_symbolic_name = self.existing_resource_symbolic_name,
            existing_resource_type = self.existing_resource_type,
            existing_resource_name = self.existing_resource_name
        ).replace('「', '{').replace('」', '}')
