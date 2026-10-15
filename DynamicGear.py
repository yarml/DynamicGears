from . import UI
from . import Commands
from . import Features
from . import Utils

def run(context):
    try:
        Commands.start()
        Features.start()
        UI.start()
    except:
        Utils.handle_error('run')

def stop(context):
    try:
        UI.stop()
        Features.stop()
        Commands.stop()
        Utils.clear_handlers()
    except:
        Utils.handle_error('stop')