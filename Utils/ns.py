from . import Config

def id(type: str, name: str) -> str:
    return f'{Config.NAMESPACE}_{Config.ADDIN_NAME}_{type}_{name}'

def id_cmd(name: str) -> str:
    return id('Command', name)

def id_ui_dropdown(name: str) -> str:
    return id('UI_Dropdown', name)

def id_feature(name: str) -> str:
    return id('Feature', name)
