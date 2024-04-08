from azure_iac.bicep_engines.base_engine import BaseEngine
from azure_iac.bicep_engines.models.template import Template


class OutputEngine(BaseEngine):
    def __init__(self):
        self.template = Template.OUTPUT.value

        self.name = None
        self.type = None
        self.value = None

    def render_template(self) -> str:
        return self.render(self.template)

    def from_tuple(otuple) -> BaseEngine:
        param_engine = OutputEngine()
        param_engine.name = otuple[0]
        param_engine.type = otuple[1]
        param_engine.value = otuple[2]
        return param_engine