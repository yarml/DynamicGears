from . import config

def id(type: str, name: str) -> str:
    return f'{config.NAMESPACE}_{config.ADDIN_NAME}_{type}_{name}'

def id_cmd(name: str) -> str:
    return id('Command', name)

def id_ui_dropdown(name: str) -> str:
    return id('UI_Dropdown', name)
