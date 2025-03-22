import dataclasses
from Models.DataClasses.Classification import Classification
from Models.DataClasses.Dataset import Dataset
from typing import List


@dataclasses.dataclass
class TrainingSet:
    training_set_name: str
    training_set_path: str
    validation_split_percentage: float
    number_of_images_training: int
    number_of_images_validation: int
