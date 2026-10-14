from .. import utils
from .. import config
import os

ROOT_RESDIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ui', 'resources'))

def resdir(resid: str) -> str:
    return os.path.join(ROOT_RESDIR, resid.removeprefix(f'{config.NAMESPACE}_{config.ADDIN_NAME}_'))
