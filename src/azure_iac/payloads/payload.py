from azure_iac.payloads.resource import Resource
from azure_iac.payloads.binding import Binding
from azure_iac.payloads.service import Service
from azure_iac.payloads.models.project_type import ProjectType


class Payload():
    def __init__(self) -> None:
        self.projectType = None
        self.resources = []
        self.bindings = []
        self.services = []
    
    def from_json(json: dict) -> 'Payload':
        payload = Payload()

        # optional property
        if 'projectType' in json:
            try:
                payload.projectType = ProjectType(json['projectType'])
            except Exception as e:
                print(f'Warning: detect projectType failed, projectType: {json["projectType"]}, error: {e}')
        
        # required property
        if 'resources' not in json:
            raise ValueError('`resources` property is not found in payload')
        
        for resource in json['resources']:
            try:
                payload.resources.extend(Resource.from_json(resource))
            except Exception as e:
                print(f'Warning: detect resource failed, resource: {resource}, error: {e}')
            # set projectType for resource
            for resource in payload.resources:
                resource.projectType = payload.projectType
        
        # for resource reference in bindings and services
        resource_dict = {resource.get_identifier(): resource for resource in payload.resources}
        
        # optional property
        if 'bindings' in json:
            for binding in json['bindings']:
                try:
                    payload.bindings.append(Binding.from_json(binding, resource_dict))
                except Exception as e:
                    print(f'Warning: detect binding failed, binding: {binding}, error: {e}')
        
        # optional property
        if 'services' in json:
            for service in json['services']:
                try:
                    dservice = Service.from_json(service, resource_dict)
                    payload.services.append(dservice)
                    source = Resource.from_expression(service.get('host'), resource_dict)
                    source.service = service
                except Exception as e:
                    print(f'Warning: detect service failed, service: {service}, error: {e}')
        
        # optional property
        if 'settings' in json:
            for setting in json['settings']:
                try:
                    source = Resource.from_expression(setting.get('resource'), resource_dict)
                    if source.type.is_compute():
                        source.settings = [env for env in setting.get('envs', []) if env.get('value')]
                except Exception as e:
                    print(f'Warning: detect setting failed, setting: {setting}, error: {e}')

        return payload
