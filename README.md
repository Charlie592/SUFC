# SUFC - Football Analytics Project
Sheffield United Technical Assessment

## Overview
This repository contains football analytics tools and notebooks focused on exploratory data analysis (EDA) and recruitment analysis, with a particular emphasis on evaluating right-back positions.

## Project Structure
```
SUFC/
├── data/               # Data files (ignored in git)
│   ├── raw/           # Raw data files
│   └── processed/     # Processed/cleaned data
├── notebooks/          # Jupyter notebooks for analysis
│   ├── 01_analysis.ipynb                    # Exploratory Data Analysis
│   └── 02_rightback_recruitment.ipynb  # Right-back recruitment analysis
├── src/                # Python source code
│   ├── __init__.py
│   ├── data_processing.py  # Data loading and preprocessing
│   ├── analysis.py         # Analysis functions
│   └── visualization.py    # Plotting and visualization utilities
├── outputs/            # Generated outputs (plots, reports, models)
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Charlie592/SUFC.git
cd SUFC
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Analysis

#### Option 1: Jupyter Notebook (Interactive)
```bash
jupyter notebook
# Open 01_analysis.ipynb and run all cells
```

#### Option 2: Python Script (Automated)
```bash
python example_analysis.py
```

This will:
- Load and process your data
- Generate all visualizations
- Create correlation analysis
- Generate comprehensive EDA report
- Save all outputs to the `outputs/` directory

### Required Data Format

Place your right-back player data CSV file in the `data/` directory. The analysis expects columns including:
- `Age` - Player age
- `Goals` - Goals scored
- `Assists` - Assists provided
- `% Passing` - Passing accuracy percentage

See the notebook for the complete workflow.

## Analysis Focus Areas

### 1. Exploratory Data Analysis (EDA)
The EDA notebook (`01_analysis.ipynb`) covers:
- **Data Overview**: Dataset structure, features, and summary statistics
- **Missing Data Analysis**: Identifying and handling missing values
- **Distribution Analysis**: Understanding the distribution of key metrics (age, goals, assists, passing)
- **Correlation Analysis**: Examining relationships between age and performance metrics
- **Correlation Heatmap**: Visual representation of metric correlations
- **Scatter Plot Analysis**: Age vs individual performance metrics with trend lines
- **Age Group Comparison**: Performance metrics across different age brackets
- **Insights Generation**: Automated textual insights from correlation data
- **Comprehensive Reporting**: Full EDA report with recommendations

### 2. Right-Back Recruitment Analysis
The recruitment analysis notebook (`02_rightback_recruitment.ipynb`) focuses on:
- **Performance Metrics**: Key performance indicators for right-backs
  - Defensive actions (tackles, interceptions, blocks)
  - Passing statistics (accuracy, progressive passes, key passes)
  - Physical attributes (pace, stamina, work rate)
  - Attacking contribution (crosses, assists, xA)
- **Player Profiling**: Clustering and categorizing right-backs by playing style
  - Defensive-minded fullbacks
  - Attacking wingbacks
  - Balanced/complete fullbacks
- **Comparative Analysis**: Benchmarking candidates against current squad
- **Age vs. Performance**: Evaluating experience and potential
- **Market Value Analysis**: Cost-effectiveness and transfer value assessment
- **Scouting Recommendations**: Data-driven shortlist generation

## Key Metrics for Right-Back Evaluation

### Defensive Metrics
- Tackles per 90 minutes
- Interceptions per 90 minutes
- Duels won percentage
- Clearances and blocks

### Passing & Build-up
- Pass completion rate
- Progressive passes
- Passes into final third
- Cross accuracy

### Attacking Contribution
- Expected Assists (xA)
- Key passes per 90
- Successful dribbles
- Shot-creating actions

### Physical & Positional
- Distance covered per match
- Sprints per match
- Positional discipline metrics

## Dependencies
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **matplotlib**: Basic plotting and visualization
- **seaborn**: Statistical data visualization
- **scikit-learn**: Machine learning and clustering algorithms
- **jupyter**: Interactive notebook environment

## Generated Outputs

Running the analysis generates the following files in the `outputs/` directory:

### Visualizations
- `age_distribution.png` - Histogram of player age distribution
- `correlation_heatmap.png` - Heatmap showing correlations between metrics
- `age_vs_goals.png` - Scatter plot with trend line
- `age_vs_assists.png` - Scatter plot with trend line
- `age_vs_passing.png` - Scatter plot with trend line
- `performance_by_age_groups.png` - Box plots comparing age groups

### Reports
- `eda_report.md` - Comprehensive markdown report with:
  - Dataset overview and statistics
  - Correlation analysis and insights
  - Key observations
  - Recommendations for Sheffield United
  - Conclusions

All visualizations are saved in high resolution (300 DPI) suitable for presentations.

## Contributing
This is a technical assessment project. For questions or suggestions, please contact the repository owner.
