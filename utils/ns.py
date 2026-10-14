from . import config

def idfor(type: str, name: str) -> str:
    return f'{config.NAMESPACE}_{config.ADDIN_NAME}_{type}_{name}'

def cmdid(name: str) -> str:
    return idfor('Command', name)

def dropdownid(name: str) -> str:
    return idfor('UI_Dropdown', name)
