import dataclasses
from Classification import Classification
from Dataset import Dataset
import json

@dataclasses.dataclass
class Profile:
    profile_name: str
    class_list: [Classification]
    dataset_list: [Dataset]