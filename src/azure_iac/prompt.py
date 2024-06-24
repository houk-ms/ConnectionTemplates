import os
import sys
import json
import copy
sys.path.append(os.path.abspath('../'))
from azure_iac.generators.bicep_generator import BicepGenerator
from azure_iac.generators.terraform_generator import TerraformGenerator
from azure_iac.payloads.payload import Payload
from azure_iac.prompt_handler.config_service_handler import ConfigServiceHandler


class CommandWithPrompt():
    def __init__(self):
        pass

    def execute(self,
                user_prompt='',
                output_path=None,
                generate_bicep=True,
                generate_terraform=True):
        
        # process user prompt
        if user_prompt == '':
            raise ValueError('user instruction is required')
        config_service_handler = ConfigServiceHandler()
        infra_json = config_service_handler.config_services(user_prompt)
        payload = Payload.from_json(infra_json)

        # output path validation
        if not output_path:
            raise ValueError('`output_path` is required')

        if generate_bicep:
            payload_copy = copy.deepcopy(payload)
            bicep_generator = BicepGenerator(payload_copy)
            bicep_generator.generate(output_path+'/infra_bicep_prompt')
        
        if generate_terraform:
            terraform_generator = TerraformGenerator(payload)
            terraform_generator.generate(output_path+'/infra_terraform_prompt')


def main():
    command = CommandWithPrompt()
    if len(sys.argv) > 2:
        command.execute(
            user_prompt=sys.argv[1], 
            output_path=sys.argv[2])
    else:
        from colorama import Fore, Style
        print(Fore.YELLOW + '''Please run command with correct syntax: 
              ./generator.exe <your-prompt> <your-output-folder>''' + Style.RESET_ALL)


if __name__ == '__main__':
    command = CommandWithPrompt()
    user_prompts = [
        "I want to create a web app connected with a Cosmos MongoDB. I also want a frontend app that calls the backend app.",
        "I want two container apps, one as frontend to call the other backend app. The backend app use a storage as a database.",
        "I want to use container app as the hosting service. The app reads and writes data from a sql database.",
        "I want two container apps, one as frontend to call the other backend app. The backend app use a storage as a database. Use ms entra id.",
        "My app needs to be hosted on Function app that uses Open AI service."
        "The application is made from multiple components, including:\
            Search service: the backend service that provides the search and retrieval capabilities.\
            Indexer service: the service that indexes the data and creates the search indexes.\
            Web app: the frontend web application that provides the user interface and orchestrates\
            the interaction between the user and the backend services."
    ]

    for i, user_prompt in enumerate(user_prompts):
        print(i, user_prompt)
        command.execute(
            user_prompt=user_prompt,
            output_path='../../output/{i}'.format(i=i))