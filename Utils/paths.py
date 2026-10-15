from .. import Config
import os

ROOT_RESDIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Resources'))

def resdir(resid: str) -> str:
    return os.path.join(ROOT_RESDIR, resid.removeprefix(f'{Config.NAMESPACE}_{Config.ADDIN_NAME}_'))
