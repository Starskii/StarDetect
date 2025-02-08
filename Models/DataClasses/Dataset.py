import dataclasses
from Models.DataClasses.AnnotatedImage import AnnotatedImage
from typing import List
import json



@dataclasses.dataclass
class Dataset:
    dataset_name: str
    annotated_images: List[AnnotatedImage]