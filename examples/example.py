import datetime
import os

import aind_behavior_services.rig as rig
from aind_behavior_services.calibration import load_cells as lcc
from aind_behavior_services.calibration.aind_manipulator import (
    AindManipulatorCalibration,
    AindManipulatorCalibrationInput,
    AindManipulatorCalibrationOutput,
    Axis,
    AxisConfiguration,
    ManipulatorPosition,
)
from aind_behavior_services.calibration.water_valve import (
    Measurement,
    WaterValveCalibration,
    WaterValveCalibrationInput,
    WaterValveCalibrationOutput,
)
from aind_behavior_services.session import AindBehaviorSessionModel

import aind_behavior_iso_force.task_logic as tl
from aind_behavior_iso_force.rig import AindIsoForceRig, AindManipulatorDevice, RigCalibration


def mock_session() -> AindBehaviorSessionModel:
    """Generates a mock AindBehaviorSessionModel model"""
    return AindBehaviorSessionModel(
        date=datetime.datetime.now(tz=datetime.timezone.utc),
        experiment="AindVrForaging",
        root_path="c://",
        subject="test",
        notes="test session",
        experiment_version="0.1.0",
        allow_dirty_repo=True,
        skip_hardware_validation=False,
        experimenter=["Foo", "Bar"],
    )


def mock_rig() -> AindIsoForceRig:
    """Generates a mock AindVrForagingRig model"""

    manipulator_calibration = AindManipulatorCalibration(
        output=AindManipulatorCalibrationOutput(),
        input=AindManipulatorCalibrationInput(
            full_step_to_mm=(ManipulatorPosition(x=0.010, y1=0.010, y2=0.010, z=0.010)),
            axis_configuration=[
                AxisConfiguration(axis=Axis.Y1, min_limit=-1, max_limit=15000),
                AxisConfiguration(axis=Axis.X, min_limit=-1, max_limit=15000),
                AxisConfiguration(axis=Axis.Z, min_limit=-1, max_limit=15000),
            ],
            homing_order=[Axis.Y1, Axis.X, Axis.Z],
            initial_position=ManipulatorPosition(y1=0, y2=0, x=0, z=0),
        ),
    )

    water_valve_input = WaterValveCalibrationInput(
        measurements=[
            Measurement(valve_open_interval=1, valve_open_time=1, water_weight=[1, 1], repeat_count=200),
            Measurement(valve_open_interval=2, valve_open_time=2, water_weight=[2, 2], repeat_count=200),
        ]
    )
    water_valve_calibration = WaterValveCalibration(
        input=water_valve_input, output=water_valve_input.calibrate_output(), date=datetime.datetime.now()
    )
    water_valve_calibration.output = WaterValveCalibrationOutput(slope=00.01, offset=0)  # For testing purposes

    video_writer = rig.cameras.VideoWriterFfmpeg(frame_rate=120, container_extension="mp4")

    load_cells_calibration = lcc.LoadCellsCalibration(
        output=lcc.LoadCellsCalibrationOutput(),
        input=lcc.LoadCellsCalibrationInput(),
        date=datetime.datetime.now(),
    )
    return AindIsoForceRig(
        rig_name="test_rig",
        triggered_camera_controller=rig.cameras.CameraController[rig.cameras.SpinnakerCamera](
            frame_rate=120,
            cameras={
                "MyCamera0": rig.cameras.SpinnakerCamera(
                    serial_number="23373889",
                    binning=1,
                    exposure=5000,
                    gain=0,
                    video_writer=video_writer,
                    adc_bit_depth=rig.cameras.SpinnakerCameraAdcBitDepth.ADC10BIT,
                    pixel_format=rig.cameras.SpinnakerCameraPixelFormat.MONO8,
                ),
            },
        ),
        harp_load_cells=lcc.LoadCells(port_name="COM8", calibration=load_cells_calibration),
        harp_behavior=rig.harp.HarpBehavior(port_name="COM7"),
        harp_lickometer=rig.harp.HarpLicketySplit(port_name="COM11"),
        harp_clock_generator=rig.harp.HarpWhiteRabbit(port_name="COM10"),
        manipulator=AindManipulatorDevice(port_name="COM9", calibration=manipulator_calibration),
        calibration=RigCalibration(water_valve=water_valve_calibration),
    )


def mock_task_logic() -> tl.AindIsoForceTaskLogic:
    """Generates a mock AindVrForagingTaskLogic model"""

    operation_control = tl.OperationControl(
        force=tl.ForceOperationControl(
            left=tl.LoadCellInput(channel=0, is_inverted=False),
            right=tl.LoadCellInput(channel=0, is_inverted=True),
            push=tl.LoadCellInput(channel=1, is_inverted=False),
            pull=tl.LoadCellInput(channel=1, is_inverted=True),
        )
    )
    trial_template = tl.Trial(
        inter_trial_interval=tl.uniform_distribution_value(min=4, max=8),
        quiescence_period=tl.QuiescencePeriod(
            duration=tl.scalar_value(0.0), force_threshold=tl.ForceThreshold(push=2000, pull=2000)
        ),
        response_period=tl.ResponsePeriod(
            duration=tl.scalar_value(600.0),
            force_threshold=tl.ForceThreshold(pull=3050, push=2800),
            rewarded_action=tl.Action.PUSH,
            force_duration=tl.scalar_value(0.2),
        ),
        reward_period=tl.Reward(amount=tl.scalar_value(1.0), delay=tl.scalar_value(0)),
    )
    return tl.AindIsoForceTaskLogic(
        task_parameters=tl.AindIsoForceTaskParameters(
            operation_control=operation_control,
            environment=tl.Environment(
                shuffle=False,
                repeat_count=0,
                block_statistics=[tl.BlockGenerator(block_size=tl.scalar_value(50), trial_template=trial_template)],
            ),
        )
    )


def main(path_seed: str = "./local/{schema}.json"):
    example_session = mock_session()
    example_rig = mock_rig()
    example_task_logic = mock_task_logic()

    os.makedirs(os.path.dirname(path_seed), exist_ok=True)

    models = [example_task_logic, example_session, example_rig]

    for model in models:
        with open(path_seed.format(schema=model.__class__.__name__), "w", encoding="utf-8") as f:
            f.write(model.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
