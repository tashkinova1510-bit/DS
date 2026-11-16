# Checkout A/B Testing (Synthetic Data)

**Author:** Anna Tashkinova  
**Type:** Educational portfolio project

## Overview
Симуляция A/B-эксперимента со средним чеком; гипотезы и статистические выводы.

## Tools
Python, Pandas, NumPy, SciPy, Matplotlib, Seaborn, Jupyter Notebook.

## Dataset
Synthetic data generated with NumPy (`np.random.seed(42)`).

## How to run
1. Install dependencies: `pip install -r requirements.txt`.
2. No dataset download is required.
3. Open `notebooks/analysis.ipynb` in JupyterLab or Jupyter Notebook. Run cells with the working directory set to `notebooks/` so `../data/...` paths resolve.

## Scope and limitations
This is an exploratory/statistical analysis project, **not** a trained machine-learning model. Results and interpretations should be verified against a fresh notebook run. Observed correlations do not establish causation.

**Note:** Experimental observations are simulated; the results are not evidence of a real product change.

## Repository contents
- `notebooks/analysis.ipynb` — original analysis and plots
- `data/README.md` — dataset download instructions
- `requirements.txt` — Python dependencies
- `.gitignore` — files excluded from Git

## Reproducibility
Run the notebook top-to-bottom after installing dependencies. Published notebook outputs are educational and should be checked against the dataset.
