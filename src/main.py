import sys
import json
from payloads.payload import Payload
from generators.bicep_generator import BicepGenerator
from generators.terraform_generator import TerraformGenerator

def main(payload_path='../test.payload.json', output_path='../output'):
    content = open(payload_path, 'r').read()
    input_json = json.loads(content)

    payload = Payload.from_json(input_json)
    infra_generator = TerraformGenerator(payload)
    infra_generator.generate(output_path+'/infra')


if len(sys.argv) > 2:
    main(sys.argv[1], sys.argv[2])
else:
    main()
    print("Please provide the payloads.json file path and output folder path.")