from bicep_engines.base_engine import BaseEngine
from bicep_engines.models.template import Template

class MainEngine(BaseEngine):
    def __init__(self):
        self.template = Template.MAIN.value

        self.params = None
        self.deployments = None
        self.outputs = None

    def render_template(self) -> str:
        return self.render(self.template)