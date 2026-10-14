from ..bc import ButtonCommand
from ... import utils

ID = utils.cmdid('CreateSpurGear')
Name = 'Spur Gear'
Description = 'Creates a solid spur gear.'

class CreateSpurGearCommand(ButtonCommand):
    def __init__(self):
        super().__init__(ID, Name, Description)

INSTANCE = CreateSpurGearCommand()
