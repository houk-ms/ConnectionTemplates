from typing import List
from terraform_engines.modules.base_resource_engine import BaseResourceEngine

class StoreResourceEngine(BaseResourceEngine):
    def __init__(self,
                 bicep_template: str,
                 module_template: str) -> None:
        super().__init__(bicep_template, module_template)

        # resource module states and variables
        self.module_params_secrets = []

    # return the store name of current engine
    def save_secret(self, secrets: List[tuple]) -> str:
        # add and deduplicate secrets
        existing_secret_names = [secret[0] for secret in self.module_params_secrets]
        for secret in secrets:
            if secret[0] not in existing_secret_names:
                self.module_params_secrets.append(secret)