from .ButtonCommand import ButtonCommand
from . import CreateSpurGear, InsertSpurGear
import itertools

PART_COMMANDS: list[ButtonCommand] = [
    CreateSpurGear.INSTANCE
]

ASSEMBLY_COMMANDS: list[ButtonCommand] = [
    InsertSpurGear.INSTANCE
]
commands = list(itertools.chain(PART_COMMANDS, ASSEMBLY_COMMANDS))

def start():
    for command in commands:
        command.start()

def stop():
    for command in commands:
        command.stop()