from jinja2 import Environment, FileSystemLoader


class BaseEngine:
    def __init__(self, template_path) -> None:
        self.template = template_path
    
    def render(self) -> str:
        env = Environment(loader=FileSystemLoader('terraform_templates/'))
        template = env.get_template()
        return template.render(engine=self)