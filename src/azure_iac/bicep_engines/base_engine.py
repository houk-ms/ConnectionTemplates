import sys
import os
import pkg_resources
from jinja2 import Environment, FileSystemLoader

from azure_iac.helpers.file_helper import get_absolute_path


class BaseEngine:
    def __init__(self) -> None:
        pass

    def render(self, template_path) -> str:
        # The logic makes sure it works for 
        # 1. normal python execution
        # 2. as binary of pyinstaller
        # 3. as a released package
        
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            template_dir = os.path.join(sys._MEIPASS, 'bicep_templates')
        else:
            template_dir = pkg_resources.resource_filename('azure_iac', 'bicep_templates')

        env = Environment(
            loader=FileSystemLoader(template_dir),
        )
        template = env.get_template(template_path)
        return template.render(engine=self)