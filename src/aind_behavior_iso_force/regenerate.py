import inspect
from pathlib import Path

from aind_behavior_services.session import AindBehaviorSessionModel
from aind_behavior_services.utils import (
    convert_pydantic_to_bonsai,
    pascal_to_snake_case,
    snake_to_pascal_case,
)

import aind_behavior_iso_force.rig
import aind_behavior_iso_force.task_logic

SCHEMA_ROOT = Path("./src/DataSchemas/")
EXTENSIONS_ROOT = Path("./src/Extensions/")
NAMESPACE_PREFIX = "AindIsoForceDataSchema"


def main():
    models = [
        aind_behavior_iso_force.task_logic.AindIsoForceTaskLogic,
        aind_behavior_iso_force.rig.AindIsoForceRig,
        AindBehaviorSessionModel,
    ]

    for model in models:
        module_name = inspect.getmodule(model).__name__
        module_name = module_name.split(".")[-1]
        schema_name = f"{pascal_to_snake_case(model.__name__)}"
        namespace = f"{NAMESPACE_PREFIX}.{snake_to_pascal_case(module_name)}"

        convert_pydantic_to_bonsai(
            {schema_name: model}, schema_path=SCHEMA_ROOT, output_path=EXTENSIONS_ROOT, namespace=namespace
        )


if __name__ == "__main__":
    main()
