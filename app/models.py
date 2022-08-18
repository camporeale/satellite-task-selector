"""Models module"""
from typing import List, Set, Union
from enum import Enum
from pydantic import BaseModel, PositiveFloat, Field


class ResourcesEnum(str, Enum):
    "ResourcesEnum"
    PROC = "proc"
    DISK = "disk"
    CAMERA = "camera"
    MISC = "misc"


class Task(BaseModel):
    """Task"""

    name: str
    resources: Set[ResourcesEnum]
    profit: PositiveFloat
    buffered: Union[bool, None]

    class Config:
        """model config"""

        use_enum_values = True
        schema_extra = {
            "example": {
                "name": "capture for client 1234",
                "resources": ["disk", "camera", "proc"],
                "profit": 9.2,
            }
        }


class BatchSelection(BaseModel):
    """BatchSelection"""

    selected_tasks: List[Union[Task, None]]
    buffered_tasks: List[Union[Task, None]]
    profit: PositiveFloat = Field(...)

    class Config:
        """model config"""

        use_enum_values = True
        schema_extra = {
            "example": {
                "selected_tasks": [
                    {
                        "name": "capture for client 1234",
                        "resources": ["disk", "camera"],
                        "profit": 9.2,
                        "buffered": False,
                    },
                    {
                        "name": "check proc",
                        "resources": ["proc"],
                        "profit": 3,
                        "buffered": True,
                    },
                ],
                "buffered_tasks": [
                    {
                        "name": "clean satellite disk",
                        "resources": ["disk"],
                        "profit": 1.2,
                        "buffered": True,
                    },
                    {
                        "name": "test task",
                        "resources": ["proc"],
                        "profit": 2.1,
                        "buffered": True,
                    },
                ],
                "profit": 12.2,
            }
        }
