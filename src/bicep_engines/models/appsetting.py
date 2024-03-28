from enum import Enum


class AppSettingType(str, Enum):
    KeyValue = "keyvalue"
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

    def get_secret_name(self) -> str:
        return self.value.split('.')[0].replace('Deployment', '-connstr').lower()