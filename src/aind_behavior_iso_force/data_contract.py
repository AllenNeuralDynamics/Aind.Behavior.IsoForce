from pathlib import Path

from aind_behavior_services.session import AindBehaviorSessionModel
from contraqctor.contract import Dataset, DataStreamCollection
from contraqctor.contract.camera import Camera
from contraqctor.contract.csv import Csv
from contraqctor.contract.harp import (
    DeviceYmlByFile,
    HarpDevice,
)
from contraqctor.contract.json import PydanticModel, SoftwareEvents
from contraqctor.contract.mux import MapFromPaths

from . import __version__
from .rig import AindIsoForceRig
from .task_logic import AindIsoForceTaskLogic


def dataset(
    root_path: Path,
    name: str = "IsoForceDataset",
    description: str = "A IsoForce dataset",
    version: str = __version__,
) -> Dataset:
    """
    Creates a Dataset object for the IsoForce experiment.
    This function constructs a hierarchical representation of the data streams collected
    during a IsoForce experiment, including hardware device data, software events,
    and configuration files.
    Parameters
    ----------
    root_path : Path
        Path to the root directory containing the dataset
    name : str, optional
        Name of the dataset, defaults to "IsoForceDataset"
    description : str, optional
        Description of the dataset, defaults to "A IsoForce dataset"
    version : str, optional
        Version of the dataset, defaults to the package version (This is also the version of the experiment)
    Returns
    -------
    Dataset
        A Dataset object containing a hierarchical representation of all data streams
        from the IsoForce experiment, including:
        - Harp device data
        - Harp device commands
        - Software events
        - Log files
        - Configuration schemas (rig, task logic, session)
    """

    root_path = Path(root_path)
    return Dataset(
        name=name,
        version=version,
        description=description,
        data_streams=[
            DataStreamCollection(
                name="Behavior",
                description="Data from the Behavior modality",
                data_streams=[
                    HarpDevice(
                        name="HarpBehavior",
                        reader_params=HarpDevice.make_params(
                            path=root_path / "behavior/Behavior.harp",
                            device_yml_hint=DeviceYmlByFile(),
                        ),
                    ),
                    HarpDevice(
                        name="HarpManipulator",
                        reader_params=HarpDevice.make_params(
                            path=root_path / "behavior/StepperDriver.harp",
                            device_yml_hint=DeviceYmlByFile(),
                        ),
                    ),
                    HarpDevice(
                        name="HarpLickometer",
                        reader_params=HarpDevice.make_params(
                            path=root_path / "behavior/Lickometer.harp",
                            device_yml_hint=DeviceYmlByFile(),
                        ),
                    ),
                    HarpDevice(
                        name="HarpClockGenerator",
                        reader_params=HarpDevice.make_params(
                            path=root_path / "behavior/ClockGenerator.harp",
                            device_yml_hint=DeviceYmlByFile(),
                        ),
                    ),
                    HarpDevice(
                        name="HarpLoadCells",
                        reader_params=HarpDevice.make_params(
                            path=root_path / "behavior/LoadCells.harp",
                            device_yml_hint=DeviceYmlByFile(),
                        ),
                    ),
                    DataStreamCollection(
                        name="HarpCommands",
                        description="Commands sent to Harp devices",
                        data_streams=[
                            HarpDevice(
                                name="HarpBehavior",
                                reader_params=HarpDevice.make_params(
                                    path=root_path / "behavior/HarpCommands/Behavior.harp",
                                    device_yml_hint=DeviceYmlByFile(),
                                ),
                            ),
                            HarpDevice(
                                name="HarpManipulator",
                                reader_params=HarpDevice.make_params(
                                    path=root_path / "behavior/HarpCommands/StepperDriver.harp",
                                    device_yml_hint=DeviceYmlByFile(),
                                ),
                            ),
                            HarpDevice(
                                name="HarpLickometer",
                                reader_params=HarpDevice.make_params(
                                    path=root_path / "behavior/HarpCommands/Lickometer.harp",
                                    device_yml_hint=DeviceYmlByFile(),
                                ),
                            ),
                            HarpDevice(
                                name="HarpClockGenerator",
                                reader_params=HarpDevice.make_params(
                                    path=root_path / "behavior/HarpCommands/ClockGenerator.harp",
                                    device_yml_hint=DeviceYmlByFile(),
                                ),
                            ),
                            HarpDevice(
                                name="HarpLoadCells",
                                reader_params=HarpDevice.make_params(
                                    path=root_path / "behavior/HarpCommands/LoadCells.harp",
                                    device_yml_hint=DeviceYmlByFile(),
                                ),
                            ),
                        ],
                    ),
                    DataStreamCollection(
                        name="SoftwareEvents",
                        description="Software events generated by the workflow. The timestamps of these events are low precision and should not be used to align to physiology data.",
                        data_streams=[
                            SoftwareEvents(
                                name="LoadCellsCalibration",
                                description="Load cells calibration data.",
                                reader_params=SoftwareEvents.make_params(
                                    root_path / "behavior/SoftwareEvents/LoadCellsCalibration.json"
                                ),
                            ),
                            SoftwareEvents(
                                name="ProcessedCrossing",
                                description="Metadata related to processed crossing events.",
                                reader_params=SoftwareEvents.make_params(
                                    root_path / "behavior/SoftwareEvents/ProcessedCrossing.json"
                                ),
                            ),
                            SoftwareEvents(
                                name="QuiescentPeriod",
                                description="Metadata related to quiescent period events.",
                                reader_params=SoftwareEvents.make_params(
                                    root_path / "behavior/SoftwareEvents/QuiescentPeriod.json"
                                ),
                            ),
                            SoftwareEvents(
                                name="RepositoryStatus",
                                description="Metadata related to repository status information.",
                                reader_params=SoftwareEvents.make_params(
                                    root_path / "behavior/SoftwareEvents/RepositoryStatus.json"
                                ),
                            ),
                            SoftwareEvents(
                                name="ResponsePeriod",
                                description="Metadata related to response period events.",
                                reader_params=SoftwareEvents.make_params(
                                    root_path / "behavior/SoftwareEvents/ResponsePeriod.json"
                                ),
                            ),
                            SoftwareEvents(
                                name="RewardPeriod",
                                description="Metadata related to reward period events.",
                                reader_params=SoftwareEvents.make_params(
                                    root_path / "behavior/SoftwareEvents/RewardPeriod.json"
                                ),
                            ),
                            SoftwareEvents(
                                name="RngSeed",
                                description="The value of the random number generator seed.",
                                reader_params=SoftwareEvents.make_params(
                                    root_path / "behavior/SoftwareEvents/RngSeed.json"
                                ),
                            ),
                            SoftwareEvents(
                                name="TrialNumber",
                                description="An event emitted at the start of each trial. The value is the trial number.",
                                reader_params=SoftwareEvents.make_params(
                                    root_path / "behavior/SoftwareEvents/TrialNumber.json"
                                ),
                            ),
                            SoftwareEvents(
                                name="TrialNumberInBlock",
                                description="Trial number within current block.",
                                reader_params=SoftwareEvents.make_params(
                                    root_path / "behavior/SoftwareEvents/TrialNumberInBlock.json"
                                ),
                            ),
                            SoftwareEvents(
                                name="ActiveBlock",
                                description="An event emitted when a new block is started. The value is the block number.",
                                reader_params=SoftwareEvents.make_params(
                                    root_path / "behavior/SoftwareEvents/ActiveBlock.json"
                                ),
                            ),
                            SoftwareEvents(
                                name="ActiveBlockLength",
                                description="The length of the current block, in trials",
                                reader_params=SoftwareEvents.make_params(
                                    root_path / "behavior/SoftwareEvents/ActiveBlockLength.json"
                                ),
                            ),
                            SoftwareEvents(
                                name="CrossingOffset",
                                description="Metadata related to crossing offset events. In practice, ProcessedCrossing should be preferred over this event.",
                                reader_params=SoftwareEvents.make_params(
                                    root_path / "behavior/SoftwareEvents/CrossingOffset.json"
                                ),
                            ),
                            SoftwareEvents(
                                name="CrossingOnset",
                                description="Metadata related to crossing onset events.  In practice, ProcessedCrossing should be preferred over this event.",
                                reader_params=SoftwareEvents.make_params(
                                    root_path / "behavior/SoftwareEvents/CrossingOnset.json"
                                ),
                            ),
                            SoftwareEvents(
                                name="GiveReward",
                                description="The amount of reward given to a subject. The value can be null if no reward was given (P=0) or 0.0 if the reward was delivered but calculated to be 0.",
                                reader_params=SoftwareEvents.make_params(
                                    root_path / "behavior/SoftwareEvents/GiveReward.json"
                                ),
                            ),
                            SoftwareEvents(
                                name="InterTrialInterval",
                                description="Metadata related to inter-trial interval events.",
                                reader_params=SoftwareEvents.make_params(
                                    root_path / "behavior/SoftwareEvents/InterTrialInterval.json"
                                ),
                            ),
                        ],
                    ),
                    DataStreamCollection(
                        name="OperationControl",
                        description="Streams associated with online operation of the task.",
                        data_streams=[
                            Csv(
                                "CurrentForce",
                                description="The force currently applied to the joystick. The units are already calibrated. Seconds are the timestamps of the load cell readings that originated the force.",
                                reader_params=Csv.make_params(
                                    path=root_path / "behavior/OperationControl/CurrentForce.csv",
                                    index="Seconds",
                                ),
                            ),
                        ],
                    ),
                    DataStreamCollection(
                        name="Logs",
                        data_streams=[
                            SoftwareEvents(
                                name="EndSession",
                                description="A file that determines the end of the session. If the file is empty, the session is still running or it was not closed properly.",
                                reader_params=SoftwareEvents.make_params(
                                    path=root_path / "behavior/Logs/EndSession.json",
                                ),
                            ),
                        ],
                    ),
                    DataStreamCollection(
                        name="InputSchemas",
                        description="Configuration files for the behavior rig, task_logic and session.",
                        data_streams=[
                            PydanticModel(
                                name="Rig",
                                reader_params=PydanticModel.make_params(
                                    model=AindIsoForceRig,
                                    path=root_path / "behavior/Logs/rig_input.json",
                                ),
                            ),
                            PydanticModel(
                                name="TaskLogic",
                                reader_params=PydanticModel.make_params(
                                    model=AindIsoForceTaskLogic,
                                    path=root_path / "behavior/Logs/tasklogic_input.json",
                                ),
                            ),
                            PydanticModel(
                                name="Session",
                                reader_params=PydanticModel.make_params(
                                    model=AindBehaviorSessionModel,
                                    path=root_path / "behavior/Logs/session_input.json",
                                ),
                            ),
                        ],
                    ),
                ],
            ),
            MapFromPaths(
                name="BehaviorVideos",
                description="Data from BehaviorVideos modality",
                reader_params=MapFromPaths.make_params(
                    paths=root_path / "behavior-videos",
                    include_glob_pattern=["*"],
                    inner_data_stream=Camera,
                    inner_param_factory=lambda camera_name: Camera.make_params(
                        path=root_path / "behavior-videos" / camera_name
                    ),
                ),
            ),
        ],
    )
