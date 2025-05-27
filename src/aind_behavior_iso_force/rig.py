# Import core types
from __future__ import annotations

# Import core types
from typing import Literal, Optional

import aind_behavior_services.calibration.load_cells as lcc
import aind_behavior_services.calibration.water_valve as wvc
import aind_behavior_services.rig as rig
from aind_behavior_services.calibration import aind_manipulator
from aind_behavior_services.rig import AindBehaviorRigModel
from pydantic import BaseModel, Field

__version__ = "0.1.0"


class AindManipulatorAdditionalSettings(BaseModel):
    """Additional settings for the manipulator device"""

    spout_axis: aind_manipulator.Axis = Field(default=aind_manipulator.Axis.Y1, description="Spout axis")


class AindManipulatorDevice(aind_manipulator.AindManipulatorDevice):
    """Overrides the default settings for the manipulator device by spec'ing additional_settings field"""

    additional_settings: AindManipulatorAdditionalSettings = Field(
        default=AindManipulatorAdditionalSettings(), description="Additional settings"
    )


class RigCalibration(BaseModel):
    water_valve: wvc.WaterValveCalibration = Field(default=..., description="Water valve calibration")


class AindIsoForceRig(AindBehaviorRigModel):
    version: Literal[__version__] = __version__
    triggered_camera_controller: rig.cameras.CameraController[rig.cameras.SpinnakerCamera] = Field(
        ..., description="Required camera controller to triggered cameras."
    )
    harp_behavior: rig.harp.HarpBehavior = Field(..., description="Harp behavior")
    harp_lickometer: rig.harp.HarpLicketySplit = Field(..., description="Harp lickometer")
    harp_load_cells: lcc.LoadCells = Field(..., description="Harp load cells")
    harp_clock_generator: rig.harp.HarpWhiteRabbit = Field(..., description="Harp clock generator")
    harp_environment_sensor: Optional[rig.harp.HarpEnvironmentSensor] = Field(
        default=None, description="Harp Environment sensor"
    )
    manipulator: AindManipulatorDevice = Field(..., description="Manipulator")
    calibration: RigCalibration = Field(..., description="Load cells calibration")
