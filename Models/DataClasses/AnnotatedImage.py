import dataclasses
from Annotation import Annotation
import json


@dataclasses.dataclass
class AnnotatedImage:
    path: str
    image_width_px: int
    image_height_px: int
    annotations: [Annotation]
