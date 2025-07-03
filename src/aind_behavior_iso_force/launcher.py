from pathlib import Path

import clabe.behavior_launcher as behavior_launcher
from aind_behavior_services.session import AindBehaviorSessionModel
from clabe import resource_monitor
from clabe.apps import AindBehaviorServicesBonsaiApp
from clabe.logging_helper import aibs as aibs_logging
from pydantic_settings import CliApp

from aind_behavior_iso_force import __version__
from aind_behavior_iso_force.rig import AindIsoForceRig
from aind_behavior_iso_force.task_logic import AindIsoForceTaskLogic

REMOTE_DIRECTORY = Path(r"\\allen\aind\scratch\iso-force\data")


def make_launcher(settings: behavior_launcher.BehaviorCliArgs) -> behavior_launcher.BehaviorLauncher:
    srv = behavior_launcher.BehaviorServicesFactoryManager()
    srv.attach_app(AindBehaviorServicesBonsaiApp(Path(r"./src/main.bonsai")))

    srv.attach_data_transfer(behavior_launcher.robocopy_data_transfer_factory(Path(REMOTE_DIRECTORY)))

    srv.attach_resource_monitor(
        resource_monitor.ResourceMonitor(
            constrains=[
                resource_monitor.available_storage_constraint_factory(settings.data_dir, 2e11),
                resource_monitor.remote_dir_exists_constraint_factory(Path(REMOTE_DIRECTORY)),
            ]
        )
    )

    launcher: behavior_launcher.BehaviorLauncher = behavior_launcher.BehaviorLauncher(
        rig_schema_model=AindIsoForceRig,
        session_schema_model=AindBehaviorSessionModel,
        task_logic_schema_model=AindIsoForceTaskLogic,
        settings=settings,
        picker=behavior_launcher.DefaultBehaviorPicker(
            config_library_dir=Path(r"\\allen\aind\scratch\AindBehavior.db\AindIsoForce")
        ),
        services=srv,
    )

    aibs_logging.attach_to_launcher(
        launcher,
        logserver_url="eng-logtools.corp.alleninstitute.org:9000",
        project_name="iso-force",
        version=__version__,
    )

    return launcher


def main():
    args = CliApp().run(behavior_launcher.BehaviorCliArgs)
    launcher = make_launcher(args)
    launcher.main()
    return None


if __name__ == "__main__":
    main()
