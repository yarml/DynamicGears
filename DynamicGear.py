from . import ui
from . import commands
from . import utils

def run(context):
    try:
        commands.start()
        ui.start()
    except:
        utils.handle_error('run')

def stop(context):
    try:
        ui.stop()
        commands.stop()
        utils.clear_handlers()
    except:
        utils.handle_error('stop')