from engines.base_engine import BaseEngine
from engines.models.template import Template

class ParamEngine(BaseEngine):
    def __init__(self):
        self.template = Template.PARAM.value

        self.name = None
        self.type = None
        self.value = None
        # if the param value is a raw string
        self.value_is_raw = True

    def render_template(self) -> str:
        return self.render(self.template)

    def from_tuple(ptuple):
        param_engine = ParamEngine()
        param_engine.name = ptuple[0]
        param_engine.type = ptuple[1]
        param_engine.value = ptuple[2]
        
        if len(ptuple) > 3:
            param_engine.value_is_raw = ptuple[3]

        return param_engine