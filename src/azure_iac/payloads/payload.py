from azure_iac.payloads.resource import Resource
from azure_iac.payloads.binding import Binding
from azure_iac.payloads.service import Service


class Payload():
    def __init__(self) -> None:
        self.resources = []
        self.bindings = []
        self.services = []
    
    def from_json(json: dict) -> 'Payload':
        payload = Payload()
        
        # required properties
        if 'resources' not in json:
            raise ValueError('`resources` property is not found in payload')
        for resource in json['resources']:
            try:
                payload.resources.extend(Resource.from_json(resource))
            except Exception as e:
                print(f'Warning: detect resource failed, resource: {resource}, error: {e}')
        
        # for resource reference in bindings and services
        resource_dict = {resource.get_identifier(): resource for resource in payload.resources}
        
        # optional properties
        if 'bindings' in json:
            for binding in json['bindings']:
                try:
                    payload.bindings.append(Binding.from_json(binding, resource_dict))
                except Exception as e:
                    print(f'Warning: detect binding failed, binding: {binding}, error: {e}')
        
        # optional properties
        # if 'services' in json:
        #     for service in json['services']:
        #         payload.services.append(Service.from_json(service, resource_dict))
        
        return payload
