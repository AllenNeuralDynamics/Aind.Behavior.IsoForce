import logging
from pathlib import Path

from aind_behavior_services.session import AindBehaviorSessionModel
from clabe import resource_monitor
from clabe.apps import (
    AindBehaviorServicesBonsaiApp,
    BonsaiAppSettings,
)
from clabe.data_transfer.robocopy import RobocopyService, RobocopySettings
from clabe.launcher import Launcher, LauncherCliArgs
from clabe.pickers import DefaultBehaviorPicker, DefaultBehaviorPickerSettings
from pydantic_settings import CliApp

from .rig import AindIsoForceRig
from .task_logic import AindIsoForceTaskLogic

logger = logging.getLogger(__name__)


async def experiment(launcher: Launcher) -> None:
    monitor = resource_monitor.ResourceMonitor(
        constrains=[
            resource_monitor.available_storage_constraint_factory(launcher.settings.data_dir, 2e11),
        ]
    )

    # Validate resources
    monitor.run()

    # Start experiment setup
    picker = DefaultBehaviorPicker(launcher=launcher, settings=DefaultBehaviorPickerSettings())

    # Pick and register session
    session = picker.pick_session(AindBehaviorSessionModel)
    launcher.register_session(session)

    # Fetch the task settings
    task_logic = picker.pick_task_logic(AindIsoForceTaskLogic)

    # Fetch rig settings
    rig = picker.pick_rig(AindIsoForceRig)

    # Run the task via Bonsai
    bonsai_app = AindBehaviorServicesBonsaiApp(BonsaiAppSettings(workflow=Path(r"./src/main.bonsai")))

    bonsai_app.add_app_settings(launcher, rig=rig, session=session, task_logic=task_logic)
    bonsai_app.get_result(allow_stderr=True)

    # Copy everything
    launcher.copy_logs()
    RobocopyService(source=launcher.session_directory, settings=RobocopySettings()).transfer()
    return


class ClabeCli(LauncherCliArgs):
    def cli_cmd(self):
        launcher = Launcher(settings=self)
        launcher.run_experiment(experiment)
        return None


def main() -> None:
    CliApp().run(ClabeCli)


if __name__ == "__main__":
    main()
