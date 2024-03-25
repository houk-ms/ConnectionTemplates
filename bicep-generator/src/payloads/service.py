from payloads.resource import Resource

class Service():
    def __init__(self):
        self.host = None
        self.language = None
        self.project = None
    
    def from_json(json, resources):
        result = Service()
        result.host = Resource.from_json(json['host'], resources)
        result.language = json['language']
        result.project = json['project']
        return result