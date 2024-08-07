from azure_iac.bicep_engines.modules.base_resource_engine import BaseResourceEngine


class SourceResourceEngine(BaseResourceEngine):
    def __init__(self,
                 bicep_template: str,
                 module_template: str) -> None:
        super().__init__(bicep_template, module_template)

        # resource.module states and variables
        self.module_var_principal_id_name = ''
        self.module_var_outbound_ip_name = ''

        # identity settings, system identity is default
        self.module_identity_type = '\'SystemAssigned\''
        self.module_user_identities = []

    # return the principal id variable name of current engine
    def get_identity_id(self) -> str:
        return self.module_var_principal_id_name
    
    # return the public ip variable name of current engine
    def get_outbound_ip(self) -> str:
        return self.module_var_outbound_ip_name

    # return the endpoint variable name of current engine
    def get_endpoint(self) -> str:
        return self.module_var_endpoint_name
    
	# enable user identity on the resource of current engine
    def enable_user_identity(self, identity_id):
        self.module_identity_type = '\'SystemAssigned, UserAssigned\''
        self.module_user_identities.append('\'${' + identity_id + '}\'')
