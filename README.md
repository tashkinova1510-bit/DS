# Student Performance Factors

**Author:** Anna Tashkinova  
**Type:** Educational portfolio project

## Overview
Исследование связей между подготовкой, посещаемостью и результатами экзаменов; корреляция Пирсона.

## Tools
Python, Pandas, NumPy, SciPy, Matplotlib, Seaborn, Jupyter Notebook.

## Dataset
https://www.kaggle.com/datasets/lainguyn123/student-performance-factors

## How to run
1. Install dependencies: `pip install -r requirements.txt`.
2. Download `StudentPerformanceFactors.csv` from the source and save it in `data/`.
3. Open `notebooks/analysis.ipynb` in JupyterLab or Jupyter Notebook. Run cells with the working directory set to `notebooks/` so `../data/...` paths resolve.

## Scope and limitations
This is an exploratory/statistical analysis project, **not** a trained machine-learning model. Results and interpretations should be verified against a fresh notebook run. Observed correlations do not establish causation.

## Repository contents
- `notebooks/analysis.ipynb` — original analysis and plots
- `data/README.md` — dataset download instructions
- `requirements.txt` — Python dependencies
- `.gitignore` — files excluded from Git

## Reproducibility
Run the notebook top-to-bottom after installing dependencies. Published notebook outputs are educational and should be checked against the dataset.
