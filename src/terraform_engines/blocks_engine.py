from terraform_engines.base_engine import BaseEngine
from terraform_engines.models.template import Template

class BlocksEngine(BaseEngine):
    def __init__(self):
        super().__init__(Template.BLOCKS.value)
    
        self.blocks = []
