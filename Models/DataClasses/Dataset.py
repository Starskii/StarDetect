import dataclasses
from AnnotatedImage import AnnotatedImage
import json



@dataclasses.dataclass
class Dataset:
    dataset_name: str
    annotated_images: [AnnotatedImage]