import dataclasses
from Models.DataClasses.Classification import Classification
from Models.DataClasses.Dataset import Dataset
from typing import List
import json


@dataclasses.dataclass
class Profile:
    profile_name: str
    class_list: List[Classification]
    dataset_list: List[Dataset]
