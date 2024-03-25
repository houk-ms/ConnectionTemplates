from payloads.payload import Payload
from payloads.binding import Binding
from payloads.models.resource_type import ResourceType
from payloads.models.connection_type import ConnectionType

class BaseGenerator:
    def __init__(self, payload: Payload):
        self.payload = payload
        self.validate_payload()
        self.auto_complete_payload()

    def validate_payload(self):
        #TODO: Implement validation
        pass

    def auto_complete_payload(self):        
        implicit_bindings = []
        for binding in self.payload.bindings:
            # when binding store is keyvault, add implicit binding for source to keyvault
            if binding.store is not None and binding.store.type == ResourceType.AZURE_KEYVAULT:
                implicit_binding = Binding()
                implicit_binding.source = binding.source
                implicit_binding.target = binding.store
                implicit_binding.connection = ConnectionType.SYSTEMIDENTITY
                implicit_bindings.append(implicit_binding)
        # no need to dedup
        self.payload.bindings.extend(implicit_bindings)