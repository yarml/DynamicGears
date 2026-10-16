from .DesignCommand import DesignCommand
from .. import Utils

ID = Utils.id_cmd('InsertSpurGear')
RESID = 'SpurGear'
Name = 'Spur Gear'
Description = 'Creates a solid spur gear.'

class InsertSpurGearCommand(DesignCommand):
    def __init__(self):
        super().__init__(ID, Name, Description, RESID)

# INSTANCE = InsertSpurGearCommand()
