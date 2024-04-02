from payloads.payload import Payload

class BaseGenerator:
    def __init__(self, payload: Payload):
        self.payload = payload
        self.validate_payload()
        self.complete_payloads()
        self.add_implicit_bindings()

    def validate_payload(self):
        #TODO: Implement validation
        pass
    
    def complete_payloads(self):
        pass

    def add_implicit_bindings(self):
        pass