import dataclasses
import json


@dataclasses.dataclass
class Classification:
    classification_name: str
    classification_id: int
    classification_color_rgb: str