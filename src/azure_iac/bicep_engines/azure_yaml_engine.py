from azure_iac.bicep_engines.base_engine import BaseEngine
from azure_iac.bicep_engines.models.template import Template
from azure_iac.payloads.service import Service


class AzureYamlEngine(BaseEngine):
    def __init__(self):
        self.template = Template.AZURE_YAML.value

        self.services = []

    def render_template(self) -> str:
        return self.render(self.template)
