json-schema
-------------
The following json-schemas are used as the format definition of the input for this task. They are the result of the `Pydantic`` models defined in `src/aind_behavior_vr_foraging`, and are also used to generate `src/Extensions/AindBehaviorVrForaging.cs` via `Bonsai.Sgen`.

`Download Schema <https://raw.githubusercontent.com/AllenNeuralDynamics/Aind.Behavior.IsoForce/main/src/DataSchemas/aind_behavior_iso_force.json>`_

Task Logic Schema
~~~~~~~~~~~~~~~~~
.. jsonschema:: https://raw.githubusercontent.com/AllenNeuralDynamics/Aind.Behavior.IsoForce/main/src/DataSchemas/aind_behavior_iso_force.json#/$defs/AindIsoForceTaskLogic
   :lift_definitions:
   :auto_reference:


Rig Schema
~~~~~~~~~~~~~~
.. jsonschema:: https://raw.githubusercontent.com/AllenNeuralDynamics/Aind.Behavior.IsoForce/main/src/DataSchemas/aind_behavior_iso_force.json#/$defs/AindIsoForceRig
   :lift_definitions:
   :auto_reference:
