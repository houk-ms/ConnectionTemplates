from azure_iac.payloads.payload import Payload
from azure_iac.payloads.models.resource_type import TargetDefaultConnectionType


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
        # if connection is not defined, set default connection type
        for binding in self.payload.bindings:
            if binding.connection is None:
                binding.connection = TargetDefaultConnectionType.get(binding.target.type)
        return True

    def add_implicit_bindings(self):
        pass