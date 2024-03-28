from terraform_engines.base_engine import BaseEngine
from terraform_engines.models.template import Template

class OutputEngine(BaseEngine):
    def __init__(self):
        super().__init__(Template.OUTPUT.value)

        self.name = None
        self.value = None

    def render_template(self) -> str:
        return self.render(self.template)

    def from_tuple(otuple) -> BaseEngine:
        param_engine = OutputEngine()
        param_engine.name = otuple[0]
        param_engine.value = otuple[1]
        return param_engine


class OutputsEngine(BaseEngine):
    def __init__(self):
        super().__init__(Template.OUTPUTS.value)
    
        self.outputs = []
    
    def render_template(self) -> str:
        return self.render(self.template)