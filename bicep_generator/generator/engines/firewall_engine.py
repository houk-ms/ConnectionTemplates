from .base_engine import BaseEngine

# Firewall engine interface
class FirewallEngine(BaseEngine):
    def __init__(self, connector):
        super().__init__(connector)


    def set_module_param_outbound_ip(self, outbound_ip):
        raise NotImplementedError('Target engine does not implement the method')
    