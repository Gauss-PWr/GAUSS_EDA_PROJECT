import os
from kaggle.api.kaggle_api_extended import KaggleApi

# Initialize the Kaggle API
api = KaggleApi()
api.authenticate()

# Specify the name of the dataset
dataset = 'saurabhshahane/road-traffic-accidents'

# Get the directory path of the current script (the 'data' folder)
script_dir = os.path.dirname(__file__)

# Download the dataset into the 'data' folder (same folder as the script)
# This will unzip the files in the specified directory
api.dataset_download_files(dataset, path=script_dir, unzip=True)

# Path to the 'cleaned.csv' file
cleaned_file_path = os.path.join(script_dir, 'cleaned.csv')

# Check if the 'cleaned.csv' file exists and remove it if found
if os.path.exists(cleaned_file_path):
    os.remove(cleaned_file_path)
    print(f"The file {cleaned_file_path} has been removed.")

# Print a success message once the dataset is downloaded
print("Dataset downloaded successfully!")