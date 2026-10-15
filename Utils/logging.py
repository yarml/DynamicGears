import traceback
import adsk.core
from .. import Config

app = adsk.core.Application.get()
ui = app.userInterface

def log(message: str, level: adsk.core.LogLevels = adsk.core.LogLevels.InfoLogLevel, force_console: bool = False):
    print(message)  

    if level == adsk.core.LogLevels.ErrorLogLevel:
        log_type = adsk.core.LogTypes.FileLogType
        app.log(message, level, log_type)

    if Config.DEBUG or force_console:
        log_type = adsk.core.LogTypes.ConsoleLogType
        app.log(message, level, log_type)


def handle_error(name: str, show_message_box: bool = False):
    log('===== Error =====', adsk.core.LogLevels.ErrorLogLevel)
    log(f'{name}\n{traceback.format_exc()}', adsk.core.LogLevels.ErrorLogLevel)

    if show_message_box:
        ui.messageBox(f'{name}\n{traceback.format_exc()}')
