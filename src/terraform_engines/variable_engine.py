from terraform_engines.base_engine import BaseEngine
from terraform_engines.models.template import Template

class VariableEngine(BaseEngine):
    def __init__(self):
        super.__init__(Template.VARIABLE.value)

        self.name = None
        self.value = None

    def from_tuple(ptuple):
        param_engine = VariableEngine()
        param_engine.name = ptuple[0]
        param_engine.value = ptuple[1]

        return param_engine


class VariablesEngine(BaseEngine):
    def __init__(self):
        super.__init__(Template.VARIABLES.value)
    
        self.variables = []
