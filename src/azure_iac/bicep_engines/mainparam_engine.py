from azure_iac.bicep_engines.base_engine import BaseEngine
from azure_iac.bicep_engines.models.template import Template


class MainParamEngine(BaseEngine):
    def __init__(self):
        self.template = Template.MAINPARAM.value

        self.params = None

    def render_template(self) -> str:
        return self.render(self.template)