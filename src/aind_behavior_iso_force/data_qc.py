import os
import typing as t
from pathlib import Path

import pandas as pd
import pydantic
import pydantic_settings
from contraqctor import contract, qc
from contraqctor.contract.harp import HarpDevice

from . import __semver__
from .data_contract import dataset
from .rig import AindIsoForceRig


class IsoForceQcSuite(qc.Suite):
    def __init__(self, dataset: contract.Dataset):
        self.dataset = dataset

    def test_end_session_exists(self):
        """Check that the session has an end event."""
        end_session = self.dataset["Behavior"]["Logs"]["EndSession"]

        if not end_session.has_data:
            return self.fail_test(
                None, "EndSession event does not exist. Session may be corrupted or not ended properly."
            )

        assert isinstance(end_session.data, pd.DataFrame)
        if end_session.data.empty:
            return self.fail_test(None, "No data in EndSession. Session may be corrupted or not ended properly.")
        else:
            return self.pass_test(None, "EndSession event exists with data.")


def make_qc_runner(dataset: contract.Dataset) -> qc.Runner:
    _runner = qc.Runner()
    loading_errors = dataset.load_all(strict=False)
    exclude: list[contract.DataStream] = []

    # Exclude commands to Harp boards as these are tested separately
    for cmd in dataset["Behavior"]["HarpCommands"]:
        for stream in cmd:
            if isinstance(stream, contract.harp.HarpRegister):
                exclude.append(stream)

    # Add the outcome of the dataset loading step to the automatic qc
    _runner.add_suite(qc.contract.ContractTestSuite(loading_errors, exclude=exclude), group="Data contract")

    # Add Harp tests for ALL Harp devices in the dataset
    for stream in (_r := dataset["Behavior"]):
        if isinstance(stream, HarpDevice):
            commands = t.cast(HarpDevice, _r["HarpCommands"][stream.name])
            _runner.add_suite(qc.harp.HarpDeviceTestSuite(stream, commands), stream.name)

    # Add Harp Hub tests
    _runner.add_suite(
        qc.harp.HarpHubTestSuite(
            dataset["Behavior"]["HarpClockGenerator"],
            [harp_device for harp_device in dataset["Behavior"] if isinstance(harp_device, HarpDevice)],
        ),
        "HarpHub",
    )

    # Add camera qc
    rig: AindIsoForceRig = dataset["Behavior"]["InputSchemas"]["Rig"].data
    for camera in dataset["BehaviorVideos"]:
        _runner.add_suite(
            qc.camera.CameraTestSuite(camera, expected_fps=rig.triggered_camera_controller.frame_rate), camera.name
        )

    # Add Csv tests
    csv_streams = [stream for stream in dataset.iter_all() if isinstance(stream, contract.csv.Csv)]
    for stream in csv_streams:
        _runner.add_suite(qc.csv.CsvTestSuite(stream), stream.name)

    # Add the IsoForce specific tests
    _runner.add_suite(IsoForceQcSuite(dataset), "IsoForce")

    return _runner


class DataQcCli(pydantic_settings.BaseSettings, cli_prog_name="data-qc", cli_kebab_case=True):
    data_path: pydantic_settings.CliPositionalArg[os.PathLike] = pydantic.Field(
        description="Path to the session data directory."
    )
    version: str = pydantic.Field(default=__semver__, description="Version of the dataset.")

    def cli_cmd(self):
        vr_dataset = dataset(Path(self.data_path), self.version)
        runner = make_qc_runner(vr_dataset)
        runner.run_all_with_progress()


if __name__ == "__main__":
    cli = pydantic_settings.CliApp().run(DataQcCli)
