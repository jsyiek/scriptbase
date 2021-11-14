import os

from typing import List


def recursive_file_grab(file_extensions: List[str], folder_to_search: str) -> List[str]:
    """
    Returns a list of file paths that have files with the corresponding extensions

    Parameters:
        file_extensions (List[str]): List of file extensions
        folder_to_search (str): Folder to search through for files

    Returns:
        files (List[str]): List of acceptable files
    """
    return_list = []
    for file in os.listdir(folder_to_search):

        file_path = os.path.join(folder_to_search, file)
        if os.path.isdir(file_path):
            return_list += recursive_file_grab(file_extensions, file_path)

        elif any(file.endswith(extension) for extension in file_extensions):
            return_list.append(file_path)

    return return_list

