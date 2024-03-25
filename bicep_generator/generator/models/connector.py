from enum import Enum


class SourceType(Enum):
    WebApp = 'webapp'
    ContainerApp = 'containerapp'


class TargetType(Enum):
    Storage = 'storage'
    Postgres = 'postgresql'
    Redis = 'redis'
    Keyvaykt = 'keyvault'
    AppInsights = 'appinsights'
    Cosmos = 'cosmos'
    ContainerApp = 'containerapp'


class AuthType(Enum):
    Secret = 'secret'
    SystemIdentity = 'system-identity'
    UserIdentity = 'user-identity'
    ServicePrincipal = 'service-principal'
    Http = 'http'


class ClientType(Enum):
    Python = 'python'
    Java = 'java'
    Dotnet = 'dotnet'


class NetworkSolution(Enum):
    Blank = 'default'
    IpFirewall = 'ipfirewall'


class Connector():
    def __init__(self, source_type, source_id, source_props, target_type, target_id, target_props, auth_type, client_type, kv_store, network_solution):
        self.source_type = source_type
        self.source_id = source_id
        self.source_props = source_props

        self.target_type = target_type
        self.target_id = target_id
        self.target_props =target_props

        self.auth_type = auth_type
        self.client_type = client_type
        self.kv_store = kv_store
        self.network_solution = network_solution
