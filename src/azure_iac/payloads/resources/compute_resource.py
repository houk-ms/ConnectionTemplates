from azure_iac.payloads.resources.base_resource import BaseResource


class ComputeResource(BaseResource):
    def __init__(self):
        self.settings = []
        self.service = None
