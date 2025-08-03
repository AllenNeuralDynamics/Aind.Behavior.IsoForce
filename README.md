# aind-iso-force

![CI](https://github.com/AllenNeuralDynamics/Aind.Behavior.IsoForce/actions/workflows/ci.yml/badge.svg)
[![PyPI - Version](https://img.shields.io/pypi/v/aind-behavior-iso-force)](https://pypi.org/project/aind-behavior-iso-force/)
[![License](https://img.shields.io/badge/license-MIT-brightgreen)](LICENSE)
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

A repository for the IsoForce task.

---

## 📋 General instructions

This repository follows the project structure laid out in the [Aind.Behavior.Services repository](https://github.com/AllenNeuralDynamics/Aind.Behavior.Services).

---

## 🔧 Prerequisites

Pre-requisites for running the project can be found [here](https://github.com/AllenNeuralDynamics/Aind.Behavior.Services?tab=readme-ov-file#prerequisites).

---

## 🚀 Deployment

For convenience, once third-party dependencies are installed, `Bonsai` and `python` virtual environments can be bootstrapped by running:

```powershell
./scripts/deploy.ps1
```

from the root of the repository.

## ⚙️ Generating settings files

The IsoForce task is instantiated by a set of three settings files that strictly follow a DSL schema. These files are:
- `task_logic.json`
- `rig.json`
- `session.json`

Examples on how to generate these files can be found in the `./Examples` directory of the repository. Once generated, these are the the only required inputs to run the Bonsai workflow in `./src/main.bonsai`.

### 🕹️Task logic

```mermaid
    ---
    config:
    theme: mc
    look: classic
    ---
    classDiagram
        class QuiescencePeriod {
            +duration
            +threshold
        }
        class ResponsePeriod {
            +duration
            +attempt_threshold
            +time_threshold
        }
        class RewardPeriod {
            +duration
            +passive/active
        }
        class ITI {
            +duration
        }
        QuiescencePeriod --> ResponsePeriod : if force < threshold for duration
        ResponsePeriod --> ResponsePeriod : if force < attempt_threshold
        ResponsePeriod --> ITI : if force > attempt_threshold for < time_threshold
        ResponsePeriod --> RewardPeriod : if force > attempt_threshold for ≥ time_threshold
        RewardPeriod --> ITI : if lick then Reward
        ITI --> QuiescencePeriod : if wait > duration
```

## 🎮 Experiment launcher (CLABE)

To manage experiments and input files, this repository contains a launcher script that can be used to run the IsoForce task. This script is located at `./src/aind_behavior_iso_force/launcher.py`. It can be run from the command line as follows:

```powershell
uv run ./src/aind_behavior_iso_force/launcher.py
```

or via the registered `clabe` command:

```powershell
uv run clabe
```

Additional arguments can be passed to the script as needed:

```powershell
uv run clabe -h
```

or via a `./local/clabe_custom.yml` file.

In order to run the launcher script, optional dependencies should be installed via:

```powershell
uv sync --extra launcher
```

Additional custom launcher scripts can be created and used as needed.

## 🔍 Primary data quality-control

Once an experiment is collected, the primary data quality-control script can be run to check the data for issues. This script can be launcher using:

```powershell
uv run ./src/aind_behavior_iso_force/data_qc.py <path-to-data-dir>
```

In order to run the script, optional dependencies should be installed via:

```powershell
uv sync --extra data
```

## 🔄 Regenerating schemas

DSL schemas can be modified in `./src/aind_behavior_iso_force/rig.py` (or `(...)/task_logic`.py`).

Once modified, changes to the DSL must be propagated to `json-schema` and `csharp` API. This can be done by running:

```powershell
uv run ./src/aind_behavior_iso_force/regenerate.py
```
