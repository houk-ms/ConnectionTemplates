from azure_iac.terraform_engines.base_engine import BaseEngine
from azure_iac.terraform_engines.models.template import Template


class OutputEngine(BaseEngine):
    def __init__(self):
        super().__init__(Template.OUTPUT.value)

        self.name = None
        self.value = None

    def from_tuple(otuple) -> BaseEngine:
        param_engine = OutputEngine()
        param_engine.name = otuple[0]
        param_engine.value = otuple[1]
        return param_engine
