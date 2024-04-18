import json
from azure_iac.payloads.payload import Payload
from azure_iac.generators.base_generator import BaseGenerator
from azure_iac.helpers import file_helper


class DotEnvGenerator(BaseGenerator):
    def __init__(self, payload: Payload):
        super().__init__(payload)

    def generate(self, output_folder: str='./'):
        # generate .env folder, with folder structure as below
        # .env
        # |--config.json
        # |--<myenv>
        # |----.env
        # |----config.json

        default_env = 'myenv'

        config_json = {
            "version": 1,
            "defaultEnvironment": default_env
        }

        # create .azure folder and default env config
        file_helper.create_file('{}/.azure/config.json'.format(output_folder), 
                                json.dumps(config_json, ensure_ascii=False, indent=4))
        
        # create .env file
        file_helper.create_file('{}/.azure/{}/.env'.format(output_folder, default_env),
                                'AZURE_ENV_NAME="{}"'.format(default_env)),
        
        # create env config
        file_helper.create_file('{}/.azure/{}/config.json'.format(output_folder, default_env),
                                '{}')
