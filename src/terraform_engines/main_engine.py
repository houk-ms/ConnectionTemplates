from terraform_engines.base_engine import BaseEngine
from terraform_engines.models.template import Template

class MainEngine(BaseEngine):
    def __init__(self):
        self.template = Template.MAIN.value

        self.resources = []

    def render_template(self) -> str:
        return self.render(self.template)