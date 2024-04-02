from jinja2 import Environment, FileSystemLoader
from helpers.file_helper import get_absolute_path


class BaseEngine:
    def __init__(self, template_path) -> None:
        self.template = template_path
    
    def render(self) -> str:
        env = Environment(loader=FileSystemLoader(get_absolute_path('./terraform_templates/')))
        template = env.get_template(self.template)
        return template.render(engine=self)