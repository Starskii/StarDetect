import dataclasses
import json


@dataclasses.dataclass
class Annotation:
    class_identifier: int
    center_x: float
    center_y: float
    width: float
    height: float
    color: str