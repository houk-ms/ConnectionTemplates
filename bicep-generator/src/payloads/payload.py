from payloads.resource import Resource
from payloads.binding import Binding
from payloads.service import Service


class Payload():
    def __init__(self):
        self.resources = []
        self.bindings = []
        self.services = []
    
    def from_json(json):
        payload = Payload()
        for resource in json['resources']:
            payload.resources += Resource.from_json(resource)
        for binding in json['bindings']:
            payload.bindings.append(Binding.from_json(binding, payload.resources))
        for service in json['services']:
            payload.services.append(Service.from_json(service, payload.resources))
        return payload
