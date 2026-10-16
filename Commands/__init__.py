from .DesignCommand import DesignCommand
from . import CreateSpurGear, InsertSpurGear
import itertools

PART_COMMANDS: list[DesignCommand] = [
    CreateSpurGear.INSTANCE
]

ASSEMBLY_COMMANDS: list[DesignCommand] = [
    # InsertSpurGear.INSTANCE
]
commands = list(itertools.chain(PART_COMMANDS, ASSEMBLY_COMMANDS))

def start():
    for command in commands:
        command.start()

def stop():
    for command in commands:
        command.stop()