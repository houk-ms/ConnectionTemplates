import sys
import json
from payloads.payload import Payload
from generators.bicep_generator import BicepGenerator
from generators.terraform_generator import TerraformGenerator


class Command:
    def __init__(self):
        pass

    def execute(self, payload_path='../test.payload.json', output_path='../output'):
        content = open(payload_path, 'r').read()
        input_json = json.loads(content)

        payload = Payload.from_json(input_json)
        bicep_generator = BicepGenerator(payload)
        bicep_generator.generate(output_path+'/infra_bicep')
        terraform_generator = TerraformGenerator(payload)
        terraform_generator.generate(output_path+'/infra_terraform')


if __name__ == '__main__':
    command = Command()
    if len(sys.argv) > 2:
        command.execute(sys.argv[1], sys.argv[2])
    else:
        command.execute()
        from colorama import Fore, Style
        print(Fore.YELLOW + '''Please run command with correct syntax: 
              ./generator.exe <your-payload>.json <your-output-folder>''' + Style.RESET_ALL)
