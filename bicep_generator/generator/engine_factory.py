from models.connector import (
    SourceType,
    TargetType
)
from engines.webapp_engine import WebAppEngine
from engines.webapp_serviceconnector_engine import WebAppServiceConnectorEngine
from engines.storage_engine import StorageEngine
from engines.storage_roleassignment_engine import StorageRoleAssignmentEngine
from engines.storage_firewall_engine import StorageFirewallEngine
from engines.postgresql_engine import PostgresqlEngine
from engines.postgresql_firewall_engine import PostgresqlFirewallEngine
from engines.keyvault_engine import KeyvaultEngine
from engines.keyvault_firewall_engine import KeyvaultFirewallEngine
from engines.keyvault_accesspolicy_engine import KeyvaultAccessPolicyEngine
from engines.keyvault_secret_engine import KeyvaultSecretEngine


def get_source_engine(connector):
    source_engine_map = {
        SourceType.WebApp.value: WebAppEngine
    }
    source_engine = source_engine_map.get(connector.source_type)
    return source_engine(connector)


def get_service_connector_engine(connector):
    service_connector_engine_map = {
        SourceType.WebApp.value: WebAppServiceConnectorEngine
    }
    service_connector_engine = service_connector_engine_map.get(connector.source_type)
    return service_connector_engine(connector)


def get_target_engine(connector):
    target_engine_map = {
        TargetType.Storage.value: StorageEngine,
        TargetType.Postgres.value: PostgresqlEngine,
        TargetType.Keyvaykt.value: KeyvaultEngine,
    }
    target_engine = target_engine_map.get(connector.target_type)
    return target_engine(connector)


def get_role_assignment_engine(connector):
    target_ra_engine_map = {
        TargetType.Storage.value: StorageRoleAssignmentEngine,
        TargetType.Keyvaykt.value: KeyvaultAccessPolicyEngine,
    }
    target_ra_engine = target_ra_engine_map.get(connector.target_type)
    return target_ra_engine(connector)


def get_firewall_engine(connector):
    target_firewall_engine_map = {
        TargetType.Storage.value: StorageFirewallEngine,
        TargetType.Postgres.value: PostgresqlFirewallEngine,
        TargetType.Keyvaykt.value: KeyvaultFirewallEngine,
    }
    target_firewall_engine = target_firewall_engine_map.get(connector.target_type)
    return target_firewall_engine(connector)


def get_secret_engine(connector):
    return KeyvaultSecretEngine(connector)