import os
from kaggle.api.kaggle_api_extended import KaggleApi
from dotenv import load_dotenv

def download_and_cleanup_kaggle_dataset():
    """
    Downloads a dataset from Kaggle and extracts its contents into the 'data' folder in the root directory.
    Files specified in the 'DELETE_FILES' environment variable will be removed after extraction.

    This function:
    1. Loads dataset name and list of files to delete from environment variables using python-dotenv.
    2. Downloads and unzips the dataset specified in the .env file to the 'data' folder.
    3. Removes files listed in 'DELETE_FILES' from the 'data' folder after extraction.

    Requirements:
    - A valid Kaggle API key stored in the file 'kaggle.json' in the directory: `~/.kaggle/` (for Unix-like systems) or `%USERPROFILE%\.kaggle\` (for Windows).
    - The dataset name should be specified in the .env file under the key 'DATASET'.
    - Files to be deleted should be specified in the .env file under the key 'DELETE_FILES', separated by commas.
    """
    # Ensure fresh environment variables are loaded
    if 'DELETE_FILES' in os.environ:
        del os.environ['DELETE_FILES']
    if 'DATASET' in os.environ:
        del os.environ['DATASET']
    load_dotenv()

    # Initialize the Kaggle API
    api = KaggleApi()
    api.authenticate()

    # Get the name of the dataset from environment variables
    dataset = os.getenv("DATASET")

    # Get the directory path of the root folder (assuming this script is in the 'utils' folder)
    root_dir = os.path.dirname(os.path.dirname(__file__))

    # Specify the 'data' folder in the root directory
    data_folder_path = os.path.join(root_dir, 'data')

    # Ensure 'data' directory exists, create it if it doesn't
    os.makedirs(data_folder_path, exist_ok=True)

    # Download the dataset into the 'data' folder
    api.dataset_download_files(dataset, path=data_folder_path, unzip=True, force=True)

    # Get the list of files to delete from the environment variable
    delete_files = os.getenv("DELETE_FILES")

    # If there are files to delete, process each file
    if delete_files:
        # Split the DELETE_FILES string by commas and process each file name
        files_to_delete = delete_files.split(',')

        for file_name in files_to_delete:
            file_path = os.path.join(data_folder_path, file_name.strip())
            if os.path.exists(file_path):
                os.remove(file_path)
