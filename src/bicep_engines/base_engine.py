from jinja2 import Environment, FileSystemLoader
from helpers.file_helper import get_absolute_path

class BaseEngine:
    def __init__(self) -> None:
        pass
    
    def render(self, template_path) -> str:
        env = Environment(loader=FileSystemLoader(get_absolute_path('./bicep_templates/')))
        template = env.get_template(template_path)
        return template.render(engine=self)