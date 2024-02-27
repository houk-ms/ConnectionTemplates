from .roleassignment_engine import RoleAssginmentEngine


class StorageRoleAssignmentEngine(RoleAssginmentEngine):
    def __init__(self, connector):
        super().__init__(connector)
        self.service_brand_name = 'role assignment for Azure Storage Account'

        self.main_params = [
            ('storageBlobDataContributorRole', 'string', "'ba92f5b4-2d11-453d-a403-e96b0029c9fe'", None)
        ]

        self.module_params = [
            ('name', 'guid(storageBlobDataContributorRole, resourceGroup().id)'),
            ('roleDefinitionId', 'storageBlobDataContributorRole')
        ]

        self.module_symbolic_name = 'storageRoleAssignmentDeployment'
        self.module_bicep_file = 'storageaccount.roleassignment.bicep'
        self.module_deployment_name = 'storage-role-assignment-deployment'


    def set_module_param_principal_id(self, principal_id):
        self.module_params.append(('principalId', principal_id))
