from azure_iac.terraform_engines.base_engine import BaseEngine
from azure_iac.terraform_engines.models.template import Template


class VariableEngine(BaseEngine):
    def __init__(self):
        super().__init__(Template.VARIABLE.value)

        self.name = None
        self.value = None
        # if the param value is a secure string
        self.value_is_secure = False

    def from_tuple(ptuple):
        var_engine = VariableEngine()
        var_engine.name = ptuple[0]
        var_engine.value = ptuple[1]

        if len(ptuple) > 2:
            var_engine.value_is_secure = ptuple[2]
        
        return var_engine

    def get_value_placeholder(self):
        # value placeholder for user to fill in (used in variables.tf file)
        return '<...>'