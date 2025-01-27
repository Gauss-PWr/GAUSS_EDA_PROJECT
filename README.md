# Road Traffic Accidents Analysis  

Developed as part of the "Gauss" Student Society by [Dominik Kukla](https://github.com/DominikKukla), [Wojciech Kowal](https://github.com/WojtekKowal), and [Mariia Kopylova](https://github.com/marika731).<br>
This project analyzes the **"Road Traffic Accidents"** dataset from Kaggle using **Python**, **Pandas**, and **Plotly**.

## Dataset Overview  
- Collected from Addis Ababa Sub-city police departments (2017–2020).  
- Contains 32 features and 12,316 records.  

## Project Highlights  
- Data preprocessing and cleaning.  
- Numerical, univariate, and multivariate analysis.  
- Insightful visualizations.  
- Conclusions and key findings based on the data.  

---

## Installation

### Step 1: Set Up Kaggle API Key
1. Log in to [Kaggle](https://www.kaggle.com/), go to **Account** > **API**, and click **Create New API Token** to download `kaggle.json`.
2. Place `kaggle.json` in:
   - **Linux/macOS**: `~/.kaggle/`
   - **Windows**: `%USERPROFILE%\.kaggle\`

### Step 2: Configure `.env` File
Create a `.env` file in the project root with:

```plaintext
DATASET_PATH="saurabhshahane/road-traffic-accidents"