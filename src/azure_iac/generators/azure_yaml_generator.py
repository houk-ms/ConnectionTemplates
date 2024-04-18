from azure_iac.payloads.payload import Payload
from azure_iac.bicep_engines.azure_yaml_engine import AzureYamlEngine
from azure_iac.generators.base_generator import BaseGenerator
from azure_iac.helpers import file_helper


class AzureYamlGenerator(BaseGenerator):
    def __init__(self, payload: Payload):
        super().__init__(payload)

    def generate(self, output_folder: str='./'):
        # generate azure.yaml file
        azureyaml_engine = AzureYamlEngine()
        azureyaml_engine.services = self.payload.services
        file_helper.create_file('{}/azure.yaml'.format(output_folder), azureyaml_engine.render_template())
