import re

from azure_iac.helpers.constants import ClientType

def get_client_type(language: str) -> ClientType:
    if language == 'js' or language == 'ts':
        return ClientType.NODE
    if language == 'java':
        return ClientType.JAVA
    if language == 'python' or language == 'py':
        return ClientType.PYTHON
    if language == 'csharp' or language == 'dotnet':
        return ClientType.DOTNET
    return ClientType.DEFAULT

def join_segments(segments: tuple, kv_separator = "=", separator = ";") -> str:
        conn_str_segs = []
        for key, value in segments:
            conn_str_segs.append(key + kv_separator + value)
        return separator.join(conn_str_segs)

def decorate_var(value: str, iac_type: str) -> str:
    if iac_type == "tf":
        return f"\"{value}\""
    
    # bicep
    # `'${var}'` should be `${var}` directly
    if re.match(r'^\${[^}]*}$', value):
        return value[2:-1]
    else:
        return '\'{}\''.format(value)
