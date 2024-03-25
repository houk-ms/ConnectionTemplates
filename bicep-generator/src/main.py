import json
from payloads.payload import Payload
from generators.infra_generator import InfraGenerator

def main():
    input_file = './test.json'
    content = open(input_file, 'r').read()
    input_json = json.loads(content)

    payload = Payload.from_json(input_json)
    infra_generator = InfraGenerator(payload)
    infra_generator.generate('./output')

if __name__ == '__main__':
    main()