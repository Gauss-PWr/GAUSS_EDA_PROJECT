# GAUSS_EDA_PROJECT

## Installation

### Step 1: Set Up Kaggle API Key
1. Log in to [Kaggle](https://www.kaggle.com/), go to **Account** > **API**, and click **Create New API Token** to download `kaggle.json`.
2. Place `kaggle.json` in:
   - **Linux/macOS**: `~/.kaggle/`
   - **Windows**: `%USERPROFILE%\.kaggle\`

### Step 2: Configure `.env` File
Create a `.env` file in the project root with:

```plaintext
DATASET_PATH="username/dataset-name"   # Replace with your dataset