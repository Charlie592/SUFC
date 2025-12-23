# SUFC - Football Analytics Project

## Overview
This repository contains football analytics tools and notebooks focused on exploratory data analysis (EDA) and recruitment analysis, with a particular emphasis on evaluating right-back positions.

## Project Structure
```
SUFC/
├── data/                 # Data files (ignored in git)
│   ├── raw/              # Raw data files
│   └── processed/        # Processed/cleaned data
├── src/                  # Python source code
│   ├── __init__.py
│   ├── utils.py          # Data loading and helpers
│   ├── features.py       # Pillar feature lists and availability helpers
│   └── scoring.py        # Per90, z-scoring, pillar/overall, feasibility, flags
├── outputs/              # Generated outputs (e.g., shortlist.csv, plots)
├── 01_analysis.ipynb     # Exploratory data analysis
├── 02_rightback_recruitment.ipynb  # RB recruitment methodology and shortlist
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Charlie592/SUFC.git
cd SUFC
```

2. Create a virtual environment (recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting Jupyter Notebook
```bash
jupyter notebook
```

## Analysis Focus Areas

### 1. Exploratory Data Analysis (EDA)
The EDA notebook (`01_analysis.ipynb`) covers:
- **Data Overview**: Dataset structure, features, and summary statistics
- **Missing Data Analysis**: Identifying and handling missing values
- **Distribution Analysis**: Understanding the distribution of key metrics (defensive actions, passing accuracy, physical attributes)
- **Correlation Analysis**: Examining relationships between different player attributes
- **Position-Specific Insights**: Comparing right-backs against other positions
- **Data Quality Assessment**: Identifying outliers and data inconsistencies

### 2. Right-Back Recruitment Analysis
The recruitment methodology (`02_rightback_recruitment.ipynb`) ranks RB/RWB candidates for a Wilder-style 3-5-2/5-3-2 via:
- **Eligibility cohort**: Position in {DR, DMR} and minutes ≥ 1000
- **Per90 creation**: Only on counting stats; safe divide-by-zero handling
- **League-aware standardisation**: Z-scores by league for all pillar metrics
- **Pillars**: Build-up, Creation, Defending (mean of available z-scores)
- **Overall + bonuses**: Weighted pillars plus small age/minutes bonuses
- **Feasibility overlay**: Market value, contract, GBE → practicality score
- **Priority score**: Recruitment_Score × Feasibility_Score
- **Risk flags**: Heuristics to annotate profiles (e.g., cross volume vs efficiency)
- **Outputs**: Top-N shortlist CSV at `./outputs/shortlist.csv` and bar chart
- **Sensitivity**: Re-rank under ±10% weight shifts to check robustness

## Key pillars and features

### Build-up
- % Passing
- Progressive Carries per90
- Ball Prog. by Carrying per90
- Pass Receipts in Space Completed
- % Passing Under Pressure

### Creation
- Expected Assists per90
- Open Play Key Passes per90
- Completed Crosses per90
- Cross Efficiency
- xT Passing per90

### Defending
- Successful Tackles per90
- Interceptions per90
- Tackles/Was Dribbled
- % Aerial Wins

## Dependencies
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **matplotlib**: Plotting
- **seaborn**: Statistical visualization (optional)
- **statsmodels**: Statistical tools (optional)
- **scikit-learn**: ML utilities (optional)
- **jupyter**: Notebook environment


## Contributing
This is a technical assessment project. For questions or suggestions, please contact the repository owner.
