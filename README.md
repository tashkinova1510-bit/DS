# TMDB Movie Box Office Analysis

**Author:** Anna Tashkinova  
**Type:** Educational portfolio project

## Overview
EDA, ROI, корреляции, доверительные интервалы и t-тесты Уэлча.

## Tools
Python, Pandas, NumPy, SciPy, Matplotlib, Seaborn, Jupyter Notebook.

## Dataset
https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata

## How to run
1. Install dependencies: `pip install -r requirements.txt`.
2. Download `tmdb_5000_movies.csv` from the source and save it in `data/`.
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
