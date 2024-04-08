from typing import List

from azure_iac.terraform_engines.base_engine import BaseEngine
from azure_iac.terraform_engines.variable_engine import VariableEngine
from azure_iac.terraform_engines.output_engine import OutputEngine


class BaseResourceEngine(BaseEngine):
    def __init__(self, template_path: str) -> None:
        self.template = template_path

        # resource module states and variables
        self.module_name = None
        
        # main.tf variables and outputs
        self.main_variables = []
        self.main_outputs = []

        # dependency engines
        self.depend_engines = []


    # add a module engine as a dependency to current engine
    # this is used to control resource provision order
    def add_dependency_engine(self, engine: BaseEngine) -> None:
        if engine not in self.depend_engines:
            self.depend_engines.append(engine)

    # return the dependency engines required by current engine
    # this is used to provision dependent resources before the current resource
    def get_dependency_engines(self) -> List[BaseEngine]:
        return self.depend_engines

    # return the variable engines required by current engine
    def get_variable_engines(self) -> List[VariableEngine]:
        return [VariableEngine.from_tuple(variable) for variable in self.main_variables]

    # return the output engines required by current engine
    def get_output_engines(self) -> List[OutputEngine]:
        return [OutputEngine.from_tuple(output) for output in self.main_outputs]
