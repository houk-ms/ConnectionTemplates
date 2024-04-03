from enum import Enum


class AppSettingType(str, Enum):
    KeyValue = "keyvalue"
    SecretReference = "secretreference"
    KeyVaultReference = "keyvaultreference"


class AppSetting():
    def __init__(self,
                 _type: AppSettingType,
                 name: str,
                 value: str) -> None:
        self.type = _type
        self.name = name
        # raw value or keyvault secret uri
        self.value = value
        # container app secret name if saved to containerapp
        self.secret_name = self.get_secret_name()
    
    def is_raw_value(self) -> bool:
        return self.type == AppSettingType.KeyValue
    
    def is_keyvault_reference(self) -> bool:
        return self.type == AppSettingType.KeyVaultReference

    def get_secret_name(self) -> str:
        return self.name.lower().replace('_', '-')