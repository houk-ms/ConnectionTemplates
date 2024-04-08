from azure_iac.terraform_engines.modules.base_resource_engine import BaseResourceEngine


class FirewallResourceEngine(BaseResourceEngine):
    def __init__(self, template_path: str) -> None:
        super().__init__(template_path)

        # resource module states and variables
        self.module_params_allow_ips = []


    # allow the ip to access the resource of current engine
    def allow_firewall(self, public_ip: str) -> None:
        if public_ip not in self.module_params_allow_ips:
            self.module_params_allow_ips.append(public_ip)
