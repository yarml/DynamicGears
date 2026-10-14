from .. import Fusion
from .. import utils
from ..commands import PART_COMMANDS, ASSEMBLY_COMMANDS

WORKSPACE_DESIGN_ID = 'FusionSolidEnvironment'

PANEL_CREATE_SOLID_ID = 'SolidCreatePanel'
PANEL_ASSEMBLE_ID = 'AssemblePanel'
PANEL_INSERT_ASSEMBLE_ID = 'InsertAssemblePanel'

DROPDOWN_CREATE_GEAR_ID = utils.id_ui_dropdown('CreateGear')
DROPDOWN_INSERT_GEAR_ID = utils.id_ui_dropdown('InsertGear')
DROPDOWN_ASSEMBLE_GEAR_ID = utils.id_ui_dropdown('AssembleGear')

UI = utils.UI

_dropdowns: list[Fusion.DropDownControl] = []

def start():
    resdir = utils.resdir('GearDropdown')

    workspace = UI.workspaces.itemById(WORKSPACE_DESIGN_ID)

    panel_create_solid = workspace.toolbarPanels.itemById(PANEL_CREATE_SOLID_ID)
    panel_assemble = workspace.toolbarPanels.itemById(PANEL_ASSEMBLE_ID)
    panel_insert_assemble = workspace.toolbarPanels.itemById(PANEL_INSERT_ASSEMBLE_ID)

    dropdown_create_gear = panel_create_solid.controls.addDropDown('Gear', resdir, DROPDOWN_CREATE_GEAR_ID, 'SeparatorAfter_PrimitivePipe')
    dropdown_assemble_gear = panel_assemble.controls.addDropDown('Gear', resdir, DROPDOWN_ASSEMBLE_GEAR_ID, 'SeparatorAfter_FusionDuplicateWithJointsCommand')
    dropdown_insert_gear = panel_insert_assemble.controls.addDropDown('Gear', resdir, DROPDOWN_INSERT_GEAR_ID, 'SeparatorAfter_FusionAddCanvasCommand')

    for cmd in PART_COMMANDS:
        if cmd.cmd_def:
            dropdown_create_gear.controls.addCommand(cmd.cmd_def)
    for cmd in ASSEMBLY_COMMANDS:
        if cmd.cmd_def:
            dropdown_assemble_gear.controls.addCommand(cmd.cmd_def)
            dropdown_insert_gear.controls.addCommand(cmd.cmd_def)

    global _dropdowns
    _dropdowns = [dropdown_create_gear, dropdown_assemble_gear, dropdown_insert_gear]
    


def stop():
    for dropdown in _dropdowns:
        for control in dropdown.controls:
            control.deleteMe()
        dropdown.deleteMe()
