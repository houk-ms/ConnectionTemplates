from typing import List
from bicep_engines.base_engine import BaseEngine
from bicep_engines.param_engine import ParamEngine
from bicep_engines.output_engine import OutputEngine


class BaseResourceEngine(BaseEngine):
    def __init__(self,
                 bicep_template: str,
                 module_template: str) -> None:
        self.bicep_template = bicep_template
        self.module_template = module_template

        # resource.module states and variables
        self.module_name = None
        
        # main.bicep states and variables
        self.main_params = []
        self.main_outputs = []

        # dependency engines
        self.depend_engines = []


    # add a engine as a dependency to current engine
    # this is used to control module provision order
    def add_dependency_engine(self, engine: BaseEngine) -> None:
        if engine not in self.depend_engines:
            self.depend_engines.append(engine)

    # return the dependency engines required by current engine
    # this is used to provision dependent resources before the current resource
    def get_dependency_engines(self) -> List[BaseEngine]:
        return self.depend_engines

    # return the param engines required by current engine
    def get_param_engines(self) -> List[ParamEngine]:
        return [ParamEngine.from_tuple(param) for param in self.main_params]

    # return the output engines required by current engine
    def get_output_engines(self) -> List[OutputEngine]:
        return [OutputEngine.from_tuple(output) for output in self.main_outputs]

    # return the rendered bicep of current engine
    def render_bicep(self) -> str:
        return self.render(self.bicep_template)

    # return the rendered module of current engine
    def render_module(self) -> str:
        return self.render(self.module_template)