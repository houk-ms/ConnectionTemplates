from azure_iac.bicep_engines.base_engine import BaseEngine
from azure_iac.bicep_engines.models.template import Template


class ParamEngine(BaseEngine):
    def __init__(self):
        self.template = Template.PARAM.value

        self.name = None
        self.type = None
        self.value = None
        # if the param value is a raw string
        self.value_is_raw = True
        # if the param value is a secure string
        self.value_is_secure = False

    def render_template(self, in_bicep=True) -> str:
        # param is in .bicep or .bicepparam file
        self.in_bicep = in_bicep
        return self.render(self.template)

    def from_tuple(ptuple):
        param_engine = ParamEngine()
        param_engine.name = ptuple[0]
        param_engine.type = ptuple[1]
        param_engine.value = ptuple[2]
        
        if len(ptuple) > 3:
            param_engine.value_is_raw = ptuple[3]
        if len(ptuple) > 4:
            param_engine.value_is_secure = ptuple[4]

        return param_engine
    
    def get_name_placeholder(self):
        # name placeholder for user to fill in (used in .bicepparam file)
        return '<...>'