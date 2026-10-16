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

    def select_plane(self, entity: FusionCore.Base, plane: FusionCore.Plane):
        self.selectedPlane = plane
        self.selectedPlaneEntity = entity
    def select_axis(self, origin: FusionCore.Point3D, direction: FusionCore.Vector3D):
        self.selectedAxisOrigin = origin
        self.selectedAxisDirection = direction

    def on_preview(self, args: FusionCore.CommandEventArgs):
        super().on_preview(args)
        args.isValidResult = self.flow.validate()
    
        if not args.isValidResult:
            return

        plane_normal = self.selectedPlane.normal.copy()
        origin_point = axis_plane_intersection(self.selectedPlane, self.selectedAxisOrigin, self.selectedAxisDirection)

        gear = CreateGearFeature(origin_point, plane_normal, self.radiusInput.value, self.heightInput.value)

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
        self.planeInput.addSelectionFilter(FusionCore.SelectionCommandInput.ConstructionPlanes)
        self.planeInput.addSelectionFilter(FusionCore.SelectionCommandInput.PlanarFaces)

        self.axisInput = inputs.addSelectionInput('axis', 'Axis', 'Select center axis')
        self.axisInput.setSelectionLimits(1, 1)
        self.axisInput.addSelectionFilter(FusionCore.SelectionCommandInput.ConstructionLines)
        self.axisInput.addSelectionFilter(FusionCore.SelectionCommandInput.LinearEdges)
        self.axisInput.addSelectionFilter(FusionCore.SelectionCommandInput.CylindricalFaces)
        self.preselect_set(self.axisInput, self.preselect_axis)

        self.radiusInput = inputs.addDistanceValueCommandInput('radius', 'Radius', FusionCore.ValueInput.createByReal(10))
        self.radiusInput.minimumValue = 0
        self.radiusInput.isMinimumValueInclusive = False

        self.heightInput = inputs.addDistanceValueCommandInput('height', 'Height', FusionCore.ValueInput.createByReal(5))

    def preselect_axis(self, selection: FusionCore.Selection, _) -> bool:
        TOLERANCE = 1e-6

        _, direction = axis_unpack(selection.entity)

        plane = self.selectedPlane

        plane_normal = plane.normal.copy()
        plane_normal.normalize()

        return abs(direction.dotProduct(plane_normal)) > TOLERANCE

def CreateGearFeature(
    comp: Fusion.Component,
    origin: FusionCore.Point3D,
    plane: FusionCore.Plane,
    planeEntity: FusionCore.Base,
    radius: float,
    height: float
) -> Fusion.BRepBody:
    comp.sketches.add(planeEntity)

    tbrep = Fusion.TemporaryBRepManager.get()
    
    normal = plane.normal.copy()
    normal.scaleBy(height)

    target = origin.copy()
    target.translateBy(normal)    

    cylinder = tbrep.createCylinderOrCone(origin, radius, target, radius)
    return cylinder

class _PlaneSelectStep(InputFlow.Step[CreateSpurGearCommand]):
    def is_complete(self) -> bool:
        return self.cmd.planeInput.selectionCount == 1

    def activate(self):
        self.cmd.planeInput.hasFocus = True
    def complete(self):
        selection = self.cmd.planeInput.selection(0).entity
        self.cmd.select_plane(selection, plane_unpack(selection))

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

    def complete(self):
        selection = self.cmd.axisInput.selection(0).entity
        selectedAxisOrigin, selectedAxisDirection = axis_unpack(selection)
        self.cmd.select_axis(selectedAxisOrigin, selectedAxisDirection)

    def show(self):
        self.cmd.axisInput.isVisible = True
    def hide(self):
        self.cmd.axisInput.isVisible = False

class _ParamStep(InputFlow.Step[CreateSpurGearCommand]):
    def is_complete(self) -> bool:
        return self.cmd.radiusInput.value > 0 and self.cmd.heightInput.value != 0

    def show(self):
        normal = self.cmd.selectedPlane.normal.copy()
        normal.normalize()

        perp = perpendicular_x_for_z(normal)

        origin_point = axis_plane_intersection(self.cmd.selectedPlane, self.cmd.selectedAxisOrigin, self.cmd.selectedAxisDirection)

        self.cmd.radiusInput.setManipulator(origin_point, perp)
        self.cmd.heightInput.setManipulator(origin_point, normal)
    
        self.cmd.radiusInput.isVisible = True
        self.cmd.radiusInput.isEnabled = True

        self.cmd.heightInput.isVisible = True
        self.cmd.heightInput.isEnabled = True

    def hide(self):
        self.cmd.radiusInput.isVisible = False
        self.cmd.radiusInput.isEnabled = False

        self.cmd.heightInput.isVisible = False
        self.cmd.heightInput.isEnabled = False            

def plane_unpack(entity: FusionCore.Base) -> FusionCore.Plane:
    if cp := Fusion.ConstructionPlane.cast(entity):
        return FusionCore.Plane.cast(cp.geometry).copy()
    elif face := Fusion.BRepFace.cast(entity):
        plane = FusionCore.Plane.cast(face.geometry).copy()
        if face.isParamReversed:
            normal = plane.normal.copy()
            normal.scaleBy(-1)
            plane = FusionCore.Plane.create(plane.origin, normal)
        return plane
    return None

def axis_unpack(entity: FusionCore.Base) -> tuple[FusionCore.Point3D, FusionCore.Vector3D]:
    if axis := Fusion.ConstructionAxis.cast(entity):
        line = FusionCore.InfiniteLine3D.cast(axis.geometry)
        return line.origin.copy(), line.direction.copy()
    elif edge := Fusion.BRepEdge.cast(entity):
        line = FusionCore.Line3D.cast(edge.geometry)
        return line.startPoint.copy(), line.startPoint.vectorTo(line.endPoint)
    elif face := Fusion.BRepFace.cast(entity):
        cylinder = FusionCore.Cylinder.cast(face.geometry)
        return cylinder.origin.copy(), cylinder.axis.copy()
    return None

def axis_plane_intersection(
    plane: FusionCore.Plane,
    axis_origin: FusionCore.Point3D,
    axis_dir: FusionCore.Vector3D,
    eps: float = 1e-9,
) -> FusionCore.Point3D | None:
    n = plane.normal.copy()
    n.normalize()

    d = axis_dir.copy()
    d.normalize()

    denom = d.dotProduct(n)
    if abs(denom) < eps:
        return None

    t = axis_origin.vectorTo(plane.origin).dotProduct(n) / denom

    d.scaleBy(t)
    result = axis_origin.copy()
    result.translateBy(d)
    return result

def perpendicular_x_for_z(normal: FusionCore.Vector3D) -> FusionCore.Vector3D:
    n = normal.copy()
    n.normalize()

    if abs(n.x) < 1.0 / 64 and abs(n.y) < 1.0 / 64:
        helper = FusionCore.Vector3D.create(0, 1, 0)
    else:
        helper = FusionCore.Vector3D.create(0, 0, 1)

    x = helper.crossProduct(n)
    x.normalize()
    return x

INSTANCE = CreateSpurGearCommand()
