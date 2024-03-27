from payloads.payload import Payload
from payloads.binding import Binding
from payloads.models.resource_type import ResourceType
from payloads.models.connection_type import ConnectionType
from payloads.resources.keyvault import KeyVaultResource

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
        # add a keyvault resource if secret binding exists and there is 
        # not a keyvault resource in the payload
        keyvault_resource = KeyVaultResource()
        is_existing_keyvault = False
        for resource in self.payload.resources:
            if resource.type == ResourceType.AZURE_KEYVAULT:
                is_existing_keyvault = True
                keyvault_resource = resource
                break
        
        has_secret_binding = False
        for binding in self.payload.bindings:
            # only application insights support secret connection without a key vault
            if binding.connection == ConnectionType.SECRET \
                and binding.target.type != ResourceType.AZURE_APPLICATION_INSIGHTS:
                binding.store = keyvault_resource
                has_secret_binding = True
        
        if not is_existing_keyvault and has_secret_binding:
            self.payload.resources.append(keyvault_resource)


    def add_implicit_bindings(self):
        # when binding store is keyvault, add implicit binding for source to keyvault
        for binding in self.payload.bindings:
            if binding.store is not None and binding.store.type == ResourceType.AZURE_KEYVAULT:
                implicit_binding = Binding()
                implicit_binding.source = binding.source
                implicit_binding.target = binding.store
                implicit_binding.connection = ConnectionType.SYSTEMIDENTITY
                
                # check duplicated binding
                existing_bingdings = [binding.get_identifier() for binding in self.payload.bindings]
                if implicit_binding.get_identifier() not in existing_bingdings:
                    self.payload.bindings.append(implicit_binding)
