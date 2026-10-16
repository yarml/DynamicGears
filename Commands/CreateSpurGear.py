from .DesignCommand import DesignCommand
from .InputFlow import InputFlow
from ..Fusion import FusionCore, Fusion
from .. import Utils

ID = Utils.id_cmd('CreateSpurGear')
RESID = 'SpurGear'
Name = 'Spur Gear'
Description = 'Creates a solid spur gear.'

class CreateSpurGearCommand(DesignCommand):
    def __init__(self):
        super().__init__(ID, Name, Description, RESID)

    def on_preview(self, args: FusionCore.CommandEventArgs):
        super().on_preview(args)
        args.isValidResult = self.flow.validate()
    
        if not args.isValidResult:
            return

        gear = CreateGearFeature(self.radiusInput.value, self.heightInput.value)

        base_feat = self.comp.features.baseFeatures.add()
        base_feat.startEdit()
        self.comp.bRepBodies.add(gear, base_feat)
        base_feat.finishEdit()

    def make_flow(self) -> InputFlow:
        flow = InputFlow[CreateSpurGearCommand](self)
        flow.add_step(_PlaneSelectStep(self))
        flow.add_step(_AxisSelectStep(self))
        flow.add_step(_ParamStep(self))
        return flow

    def make_ui(self, inputs: FusionCore.CommandInputs):
        self.planeInput = inputs.addSelectionInput('plane', 'Plane', 'Select base plane')
        self.planeInput.setSelectionLimits(1, 1)
        self.planeInput.addSelectionFilter('ConstructionPlanes')
        self.planeInput.addSelectionFilter('PlanarFaces')

        self.axisInput = inputs.addSelectionInput('axis', 'Axis', 'Select center axis')
        self.axisInput.setSelectionLimits(1, 1)
        self.axisInput.addSelectionFilter('ConstructionLines')
        self.axisInput.addSelectionFilter('LinearEdges')


        radiusValue = FusionCore.ValueInput.createByReal(1)
        self.radiusInput = inputs.addDistanceValueCommandInput('radius', 'Radius', radiusValue)
        self.radiusInput.setManipulator(FusionCore.Point3D.create(0, 0, 0), FusionCore.Vector3D.create(1, 0, 0))

        heightValue = FusionCore.ValueInput.createByReal(0.5)
        self.heightInput = inputs.addDistanceValueCommandInput('height', 'Height', heightValue)
        self.heightInput.setManipulator(FusionCore.Point3D.create(0, 0, 0), FusionCore.Vector3D.create(0, 0, 1))

def CreateGearFeature(radius: float, height: float) -> Fusion.BRepBody:
    tbrep = Fusion.TemporaryBRepManager.get()
    cylinder = tbrep.createCylinderOrCone(FusionCore.Point3D.create(0, 0, 0), radius, FusionCore.Point3D.create(0, 0, height), radius)
    return cylinder

class _PlaneSelectStep(InputFlow.Step[CreateSpurGearCommand]):
    def is_complete(self) -> bool:
        return self.cmd.planeInput.selectionCount == 1

    def activate(self):
        self.cmd.planeInput.hasFocus = True

    def show(self):
        self.cmd.planeInput.isVisible = True
    def hide(self):
        self.cmd.planeInput.isVisible = False

class _AxisSelectStep(InputFlow.Step[CreateSpurGearCommand]):
    def __init__(self, cmd):
        super().__init__(cmd)

    def is_complete(self) -> bool:
        return self.cmd.axisInput.selectionCount == 1

    def activate(self):
        self.cmd.axisInput.hasFocus = True

    def show(self):
        self.cmd.axisInput.isVisible = True
    def hide(self):
        self.cmd.axisInput.isVisible = False

class _ParamStep(InputFlow.Step[CreateSpurGearCommand]):
    def is_complete(self) -> bool:
        return self.cmd.radiusInput.value > 0 and self.cmd.heightInput.value != 0

    def show(self):
        self.cmd.radiusInput.isVisible = True
        self.cmd.radiusInput.isEnabled = True

        self.cmd.heightInput.isVisible = True
        self.cmd.heightInput.isEnabled = True

    def hide(self):
        self.cmd.radiusInput.isVisible = False
        self.cmd.radiusInput.isEnabled = False

        self.cmd.heightInput.isVisible = False
        self.cmd.heightInput.isEnabled = False

INSTANCE = CreateSpurGearCommand()
