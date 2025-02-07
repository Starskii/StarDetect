import dataclasses
import json


@dataclasses.dataclass
class Annotation:
    class_identifier: int
    center_x: float
    center_y: float
    width: float
    height: float

# annotation = Annotation(0, .5, .5, .1, .1)
# print(json.dumps(dataclasses.asdict(annotation), indent=4))