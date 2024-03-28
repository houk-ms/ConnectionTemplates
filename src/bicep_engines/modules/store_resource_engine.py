from bicep_engines.modules.base_resource_engine import BaseResourceEngine


class StoreResourceEngine(BaseResourceEngine):
    def __init__(self,
                 bicep_template: str,
                 module_template: str) -> None:
        super().__init__(bicep_template, module_template)

        # resource.module states and variables
        self.module_params_name = ''

    # return the store name of current engine
    def get_store_name(self) -> str:
        return self.module_params_name