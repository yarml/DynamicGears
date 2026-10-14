from ..bc import ButtonCommand
from ... import utils

ID = utils.id_cmd('InsertSpurGear')
RESID = 'SpurGear'
Name = 'Spur Gear'
Description = 'Creates a solid spur gear.'

class InsertSpurGearCommand(ButtonCommand):
    def __init__(self):
        super().__init__(ID, Name, Description, RESID)

INSTANCE = InsertSpurGearCommand()
