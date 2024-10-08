from enum import Enum
from typing import Optional

from pydantic import Extra

from schema.charts.utils.utils import BaseModel, ConfigurableClass, create_json_schema_conditionals


class SchedulerType(str, Enum):
    DAEMON = "DagsterDaemonScheduler"
    CUSTOM = "CustomScheduler"


class DaemonSchedulerConfig(BaseModel):
    maxCatchupRuns: Optional[int]
    maxTickRetries: Optional[int]


class SchedulerConfig(BaseModel):
    daemonScheduler: Optional[DaemonSchedulerConfig]
    customScheduler: Optional[ConfigurableClass]

    class Config:
        extra = Extra.forbid


class Scheduler(BaseModel):
    type: SchedulerType
    config: SchedulerConfig

    class Config:
        extra = Extra.forbid
        schema_extra = {
            "allOf": create_json_schema_conditionals({SchedulerType.CUSTOM: "customScheduler"})
        }
