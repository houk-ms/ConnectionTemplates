import os
import sys
import pkg_resources
from jinja2 import Environment, FileSystemLoader

from azure_iac.helpers.file_helper import get_absolute_path


class BaseEngine:
    def __init__(self, template_path) -> None:
        self.template = template_path
    
    def render(self) -> str:
        # The logic makes sure it works for 
        # 1. normal python execution
        # 2. as binary of pyinstaller
        # 3. as a released package

        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            template_dir = os.path.join(sys._MEIPASS, 'terraform_templates')
        else:
            template_dir = pkg_resources.resource_filename('azure_iac', 'terraform_templates')

        env = Environment(
            loader=FileSystemLoader(template_dir),
        )
        template = env.get_template(self.template)
        return template.render(engine=self)