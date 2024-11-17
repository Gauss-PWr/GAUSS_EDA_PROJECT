import os
from kaggle.api.kaggle_api_extended import KaggleApi
from dotenv import load_dotenv
from utils.config import DATASET_PATH

def download_kaggle_dataset():
    """
    Downloads and extracts a Kaggle dataset specified in the .env file to the 'data' folder in the project root.

    Environment:
    - DATASET_PATH (str): Kaggle dataset identifier in .env (e.g., 'username/dataset-name').

    Returns:
    - str: Confirmation message on successful download and extraction.
    """

    api = KaggleApi()
    api.authenticate()
    dataset = os.environ["DATASET_PATH"]

    root_dir = os.path.dirname(os.path.dirname(__file__))
    data_folder_path = os.path.join(root_dir, 'data')
    os.makedirs(data_folder_path, exist_ok=True)
    api.dataset_download_files(dataset, path=data_folder_path, unzip=True, force=True)

    return 'Download completed'