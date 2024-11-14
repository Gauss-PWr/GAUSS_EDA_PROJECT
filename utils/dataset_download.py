import os
from kaggle.api.kaggle_api_extended import KaggleApi
from dotenv import load_dotenv
from config import DATASET

def download_kaggle_dataset(delete_files=[]):
    """
    Downloads a dataset specified in the .env file from Kaggle and extracts its contents into the 'data' folder in the root directory.
    Files specified in the 'delete_files' argument will be removed after extraction.

    Parameters:
    - delete_files (list, optional): A list of string file names to be deleted from the 'data' folder after extraction. Defaults to an empty list.
    """

    api = KaggleApi()
    api.authenticate()
    dataset = os.getenv("DATASET")

    root_dir = os.path.dirname(os.path.dirname(__file__))
    data_folder_path = os.path.join(root_dir, 'data')
    os.makedirs(data_folder_path, exist_ok=True)
    api.dataset_download_files(dataset, path=data_folder_path, unzip=True, force=True)

    if delete_files:
        for file_name in delete_files:
            file_path = os.path.join(data_folder_path, file_name.strip())
            if os.path.exists(file_path):
                os.remove(file_path)

    return 'Download completed'