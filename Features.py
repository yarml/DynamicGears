from .Fusion import Fusion
from . import Utils

def start():
    SpurGearFeatureDef = Fusion.CustomFeatureDefinition.create(Utils.id_feature('SpurGear'), 'Spur Gear', Utils.resdir('SpurGear'))

def stop():
    pass
