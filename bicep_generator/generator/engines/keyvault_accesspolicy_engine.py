from .roleassignment_engine import RoleAssginmentEngine


class KeyvaultAccessPolicyEngine(RoleAssginmentEngine):
    def __init__(self, connector):
        super().__init__(connector)
        self.service_brand_name = 'access policy for Azure Keyvault'

        self.module_params = [
            ('keyVaultName', 'keyVaultName')
        ]

        self.module_symbolic_name = 'keyvaultAccessPolicyDeployment'
        self.module_bicep_file = 'keyvault.accesspolicy.bicep'
        self.module_deployment_name = 'keyvault-access-policy-deployment'

        self.module_depends = "[keyvaultDeployment]"

    def set_module_param_principal_id(self, principal_id):
        self.module_params.append(('principalId', principal_id))
