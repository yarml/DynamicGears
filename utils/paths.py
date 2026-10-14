from .. import utils
from .. import config
import os

ROOT_ICON_FOLDER = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ui', 'resources'))

def icon_folder(name: str) -> str:
    return os.path.join(ROOT_ICON_FOLDER, name.removeprefix(f'{config.NAMESPACE}_{config.ADDIN_NAME}_'))
