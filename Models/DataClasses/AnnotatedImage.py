import dataclasses
from Models.DataClasses.Annotation import Annotation
from typing import List
import json


@dataclasses.dataclass
class AnnotatedImage:
    path: str
    image_width_px: int
    image_height_px: int
    annotations: List[Annotation]
