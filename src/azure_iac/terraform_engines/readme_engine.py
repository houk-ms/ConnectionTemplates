from azure_iac.terraform_engines.base_engine import BaseEngine
from azure_iac.terraform_engines.models.template import Template


class ReadMeEngine(BaseEngine):
    def __init__(self):
        self.template = Template.README.value

        self.resources = []

    def render_template(self) -> str:
        return self.render()