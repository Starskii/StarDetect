import os
def create_directory(directory_path: str) -> str:
    directory_path_index = 0
    directory_name = directory_path
    while os.path.exists(directory_name):
        directory_path_index += 1
        directory_name = directory_path + str(directory_path_index)
    os.makedirs(directory_name)
    return directory_name