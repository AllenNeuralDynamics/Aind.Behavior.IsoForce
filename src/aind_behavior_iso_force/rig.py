# Import core types
from typing import Literal, Optional

import aind_behavior_services.rig.load_cells as lcc
import aind_behavior_services.rig.water_valve as wvc
from aind_behavior_services.rig import Rig, aind_manipulator, cameras, harp
from pydantic import BaseModel, Field

from aind_behavior_iso_force import __semver__


class AindManipulatorDevice(aind_manipulator.AindManipulator):
    """Overrides the default settings for the manipulator device by spec'ing additional_settings field"""

    spout_axis: aind_manipulator.Axis = Field(default=aind_manipulator.Axis.Y1, description="Spout axis")


class RigCalibration(BaseModel):
    water_valve: wvc.WaterValveCalibration = Field(default=..., description="Water valve calibration")


class AindIsoForceRig(Rig):
    version: Literal[__semver__] = __semver__
    triggered_camera_controller: cameras.CameraController[cameras.SpinnakerCamera] = Field(
        description="Required camera controller to triggered cameras."
    )
    harp_behavior: harp.HarpBehavior = Field(description="Harp behavior")
    harp_lickometer: harp.HarpLicketySplit = Field(description="Harp lickometer")
    harp_load_cells: lcc.LoadCells = Field(description="Harp load cells")
    harp_clock_generator: harp.HarpWhiteRabbit = Field(description="Harp clock generator")
    harp_environment_sensor: Optional[harp.HarpEnvironmentSensor] = Field(
        default=None, description="Harp Environment sensor"
    )
    manipulator: AindManipulatorDevice = Field(description="Manipulator")
    calibration: RigCalibration = Field(description="Load cells calibration")
