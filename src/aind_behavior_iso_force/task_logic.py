from __future__ import annotations

from enum import Enum, IntFlag
from typing import Annotated, List, Literal, Optional, Self, Union

import aind_behavior_services.task_logic.distributions as distributions
from aind_behavior_services.task_logic import AindBehaviorTaskLogicModel, TaskParameters
from pydantic import BaseModel, Field, model_validator
from typing_extensions import TypeAliasType

from aind_behavior_iso_force import __version__

from .rig import lcc


def scalar_value(value: float) -> distributions.Scalar:
    """
    Helper function to create a scalar value distribution for a given value.

    Args:
        value (float): The value of the scalar distribution.

    Returns:
        distributions.Scalar: The scalar distribution type.
    """
    return distributions.Scalar(distribution_parameters=distributions.ScalarDistributionParameter(value=value))


def uniform_distribution_value(min: float, max: float) -> distributions.UniformDistribution:
    """
    Helper function to create a uniform distribution for a given range.

    Args:
        min (float): The minimum value of the uniform distribution.
        max (float): The maximum value of the uniform distribution.

    Returns:
        distributions.Uniform: The uniform distribution type.
    """
    return distributions.UniformDistribution(
        distribution_parameters=distributions.UniformDistributionParameters(max=max, min=min)
    )


def normal_distribution_value(mean: float, std: float) -> distributions.Normal:
    """
    Helper function to create a normal distribution for a given range.

    Args:
        mean (float): The mean value of the normal distribution.
        std (float): The standard deviation of the normal distribution.

    Returns:
        distributions.Normal: The normal distribution type.
    """
    return distributions.NormalDistribution(
        distribution_parameters=distributions.NormalDistributionParameters(mean=mean, std=std)
    )


class Action(IntFlag):
    """Defines the action types"""

    NONE = 0
    LEFT = 1 << 0
    RIGHT = 1 << 1
    RIGHT_LEFT = LEFT | RIGHT
    PUSH = 1 << 2
    PULL = 1 << 3
    PUSH_PULL = PUSH | PULL


class ForceThreshold(BaseModel):
    left: Optional[float] = Field(default=None, description="Left force threshold")
    right: Optional[float] = Field(default=None, description="Right force threshold")
    push: Optional[float] = Field(default=None, description="Push force threshold")
    pull: Optional[float] = Field(default=None, description="Pull force threshold")

    def from_action(self, action: Action) -> Optional[float]:
        """
        Returns the force threshold for the given action.

        Args:
            action (Action): The action to get the force threshold for.

        Returns:
            Optional[float]: The force threshold for the action, or None if no threshold is set.
        """
        if bin(action).count("1") != 1:
            raise ValueError("Only one flag in the Action enum can be set at a time.")
        if action == Action.LEFT:
            return self.left
        elif action == Action.RIGHT:
            return self.right
        elif action == Action.PUSH:
            return self.push
        elif action == Action.PULL:
            return self.pull
        return None


class QuiescencePeriod(BaseModel):
    """Defines a quiescence settings"""

    duration: distributions.Distribution = Field(
        default=scalar_value(0.5),
        description="Duration force has to stay below threshold to start the trial.",
        validate_default=True,
    )
    force_threshold: ForceThreshold = Field(
        default=ForceThreshold(),
        description="Threshold for the force sensors to be considered quiescent. If None, the threshold will be ignored.",
        validate_default=True,
    )


class ResponsePeriod(BaseModel):
    """Defines a response period"""

    duration: distributions.Distribution = Field(
        default=scalar_value(0.5),
        description="Duration of the response period. I.e. the time the animal has to make a choice.",
        validate_default=True,
    )
    force_threshold: ForceThreshold = Field(
        default=ForceThreshold(),
        description="Threshold for the force sensors to be considered active. If None, the crossings will be ignored.",
        validate_default=True,
    )
    rewarded_action: Action = Field(default=Action.NONE)
    force_duration: distributions.Distribution = Field(
        default=scalar_value(0.05), description="Duration the force must stay above threshold.", validate_default=True
    )

    @model_validator(mode="after")
    def _validate_rewarded_action_vs_threshold(self) -> Self:
        if self.rewarded_action != Action.NONE:
            if self.force_threshold.from_action(self.rewarded_action) is None:
                raise ValueError("Force threshold must be set for the rewarded action.")
        return self


class Reward(BaseModel):
    reward_type: Literal["Pavlovian"] = "Pavlovian"
    amount: distributions.Distribution = Field(
        default=scalar_value(1.0), description="Amount of reward to dispense", validate_default=True
    )
    delay: distributions.Distribution = Field(
        default=scalar_value(0.0), description="Delay before dispensing the reward", validate_default=True
    )


class OperantReward(Reward):
    reward_type: Literal["Operant"] = "Operant"
    time_to_collect: distributions.Distribution = Field(
        default=scalar_value(0.5), description="Time to collect the reward", validate_default=True
    )


RewardPeriod = TypeAliasType(
    "RewardPeriod", Annotated[Union[Reward, OperantReward], Field(discriminator="reward_type")]
)


class Trial(BaseModel):
    """Defines a trial"""

    inter_trial_interval: distributions.Distribution = Field(
        default=scalar_value(0.5), description="Time between trials", validate_default=True
    )
    quiescence_period: Optional[QuiescencePeriod] = Field(default=None, description="Quiescence settings")
    response_period: ResponsePeriod = Field(
        default=ResponsePeriod(), validate_default=True, description="Response settings"
    )
    reward_period: RewardPeriod = Field(default=Reward(), validate_default=True, description="Reward settings")


class BlockStatisticsMode(str, Enum):
    """Defines the mode of the environment"""

    BLOCK = "Block"
    BLOCK_GENERATOR = "BlockGenerator"


class Block(BaseModel):
    mode: Literal[BlockStatisticsMode.BLOCK] = BlockStatisticsMode.BLOCK
    trials: List[Trial] = Field(default=[], description="List of trials in the block")
    shuffle: bool = Field(default=False, description="Whether to shuffle the trials in the block")
    repeat_count: Optional[int] = Field(
        default=0, description="Number of times to repeat the block. If null, the block will be repeated indefinitely"
    )


class BlockGenerator(BaseModel):
    mode: Literal[BlockStatisticsMode.BLOCK_GENERATOR] = BlockStatisticsMode.BLOCK_GENERATOR
    block_size: distributions.Distribution = Field(
        default=uniform_distribution_value(min=50, max=60), validate_default=True, description="Size of the block"
    )
    trial_template: Trial = Field(..., description="Statistics of the trials in the block")


BlockStatistics = TypeAliasType("BlockStatistics", Annotated[Union[Block, BlockGenerator], Field(discriminator="mode")])


class Environment(BaseModel):
    block_statistics: List[BlockStatistics] = Field(..., description="Statistics of the environment")
    shuffle: bool = Field(default=False, description="Whether to shuffle the blocks")
    repeat_count: Optional[int] = Field(
        default=0,
        description="Number of times to repeat the environment. If null, the environment will be repeated indefinitely",
    )


class LoadCellInput(BaseModel):
    channel: lcc.LoadCellChannel = Field(..., description="Load cell channel number")
    is_inverted: bool = Field(default=False, description="Whether the load cell is inverted")


class ForceOperationControl(BaseModel):
    left: LoadCellInput = Field(default=LoadCellInput(channel=0, is_inverted=False), description="Left load cell input")
    right: LoadCellInput = Field(
        default=LoadCellInput(channel=0, is_inverted=True), description="Right load cell input"
    )
    push: LoadCellInput = Field(default=LoadCellInput(channel=1, is_inverted=False), description="Push load cell input")
    pull: LoadCellInput = Field(default=LoadCellInput(channel=1, is_inverted=True), description="Pull load cell input")


class OperationControl(BaseModel):
    force: ForceOperationControl = Field(
        default=ForceOperationControl(), validate_default=True, description="Operation control for force sensor"
    )


class AindIsoForceTaskParameters(TaskParameters):
    environment: Environment = Field(..., description="Environment settings")
    operation_control: OperationControl = Field(
        default=OperationControl(), validate_default=True, description="Operation control"
    )


class AindIsoForceTaskLogic(AindBehaviorTaskLogicModel):
    version: Literal[__version__] = __version__
    name: Literal["AindIsoForce"] = Field(default="AindIsoForce", description="Name of the task logic")
    task_parameters: AindIsoForceTaskParameters = Field(..., description="Parameters of the task logic")
