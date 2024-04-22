import os
import sys
sys.path.append(os.path.abspath('../'))
import json
from azure_iac.payloads.payload import Payload
from azure_iac.generators.bicep_generator import BicepGenerator
from azure_iac.generators.terraform_generator import TerraformGenerator


class Command:
    def __init__(self):
        pass

    def execute(self,
                payload=None,
                payload_path=None, 
                output_path=None,
                generate_bicep=True,
                generate_terraform=True):
        
        # payload validation
        if not payload and not payload_path:
            raise ValueError('`payload` or `payload_path` is required')
        
        # output path validation
        if not output_path:
            raise ValueError('`output_path` is required')

        if not payload:
            content = open(payload_path, 'r').read()
            input_json = json.loads(content)
            payload = Payload.from_json(input_json)

        if generate_bicep:
            bicep_generator = BicepGenerator(payload)
            bicep_generator.generate(output_path+'/infra_bicep')
        
        if generate_terraform:
            terraform_generator = TerraformGenerator(payload)
            terraform_generator.generate(output_path+'/infra_terraform')


def main():
    command = Command()
    if len(sys.argv) > 2:
        command.execute(
            payload_path = sys.argv[1], 
            output_path = sys.argv[2])
    else:
        from colorama import Fore, Style
        print(Fore.YELLOW + '''Please run command with correct syntax: 
              ./generator.exe <your-payload>.json <your-output-folder>''' + Style.RESET_ALL)


if __name__ == '__main__':
    main()