from azure_iac.bicep_engines.base_engine import BaseEngine
from azure_iac.bicep_engines.models.template import Template


class ReadMeEngine(BaseEngine):
    def __init__(self):
        self.template = Template.README.value

        self.resources = []

    def render_template(self) -> str:
        return self.render(self.template)