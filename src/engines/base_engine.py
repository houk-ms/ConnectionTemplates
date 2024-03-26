from jinja2 import Environment, FileSystemLoader


class BaseEngine:
    def __init__(self) -> None:
        pass
    
    def render(self, template_path) -> str:
        env = Environment(loader=FileSystemLoader('templates/'))
        template = env.get_template(template_path)
        return template.render(engine=self)