from .bc import ButtonCommand
from . import CreateSpurGear

commands: list[ButtonCommand] = [
    CreateSpurGear.INSTANCE,
]

def start():
    for command in commands:
        command.start()

def stop():
    for command in commands:
        command.stop()