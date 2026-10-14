from .. import Fusion
from .. import utils
from ..commands import CreateSpurGear

WORKSPACE_DESIGN_ID = 'FusionSolidEnvironment'

PANEL_CREATE_SOLID_ID = 'SolidCreatePanel'
PANEL_ASSEMBLE_ID = 'AssemblePanel'
PANEL_INSERT_ASSEMBLY_ID = 'InsertAssemblyPanel'

DROPDOWN_CREATE_GEAR_ID = utils.dropdownid('CreateGear')

UI = utils.UI

def start():
    workspace = UI.workspaces.itemById(WORKSPACE_DESIGN_ID)
    panel_create_solid = workspace.toolbarPanels.itemById(PANEL_CREATE_SOLID_ID)
    #PANEL_ASSEMBLE = WORKSPACE_DESIGN.toolbarPanels.itemById(PANEL_ASSEMBLE_ID)
    #PANEL_INSERT_ASSEMBLY = WORKSPACE_DESIGN.toolbarPanels.itemById(PANEL_INSERT_ASSEMBLY_ID)

    dropdown_create_gear = panel_create_solid.controls.addDropDown('Gear', utils.icon_folder(DROPDOWN_CREATE_GEAR_ID), DROPDOWN_CREATE_GEAR_ID, 'PrimitivePipe', False)

    dropdown_create_gear.controls.addCommand(UI.commandDefinitions.itemById(CreateSpurGear.ID))
    


def stop():
    workspace = UI.workspaces.itemById(WORKSPACE_DESIGN_ID)
    panel_create_solid = workspace.toolbarPanels.itemById(PANEL_CREATE_SOLID_ID)
    dropdown_create_gear = panel_create_solid.controls.itemById(DROPDOWN_CREATE_GEAR_ID)

    if dropdown_create_gear:
        for ctl in dropdown_create_gear.controls:
            ctl.deleteMe()
        dropdown_create_gear.deleteMe()
