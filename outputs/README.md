# Analysis Outputs

This directory contains generated visualizations and reports from the exploratory data analysis.

## Generated Files

When you run the analysis notebook (`01_analysis.ipynb`), the following files will be created:

### Visualizations

1. **correlation_heatmap.png** - Heatmap showing correlations between age and performance metrics
2. **age_vs_goals.png** - Scatter plot of age vs goals with trend line
3. **age_vs_assists.png** - Scatter plot of age vs assists with trend line
4. **age_vs_passing.png** - Scatter plot of age vs passing percentage with trend line
5. **performance_by_age_groups.png** - Box plots comparing performance metrics across age groups

### Reports

1. **eda_report.md** - Comprehensive markdown report with:
   - Dataset overview and statistics
   - Correlation analysis
   - Key observations and insights
   - Recommendations for Sheffield United recruitment strategy
   - Conclusions

## Usage

All visualizations are saved in high resolution (300 DPI) and are suitable for presentations and reports.

The markdown report can be:
- Viewed directly in any markdown viewer
- Converted to PDF using tools like pandoc
- Included in other documentation

## Note

This directory is tracked by git but the actual output files are ignored (see `.gitignore`).
Only this README and the `.gitkeep` file are committed to version control.
