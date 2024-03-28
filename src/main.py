import json
from payloads.payload import Payload
from generators.bicep_generator import BicepGenerator

def main():
    input_file = '../test.payload.json'
    content = open(input_file, 'r').read()
    input_json = json.loads(content)

    payload = Payload.from_json(input_json)
    infra_generator = BicepGenerator(payload)
    infra_generator.generate('../output')

if __name__ == '__main__':
    main()