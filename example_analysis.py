#!/usr/bin/env python3
"""
Example script demonstrating the complete EDA workflow.

This script shows how to use the utils functions to perform a complete
exploratory data analysis on right-back player data.
"""

from pathlib import Path
import matplotlib.pyplot as plt
from src import utils

# Configuration
DATA_PATH = "data/sample_rightbacks.csv"  # Update with your data path
OUTPUT_DIR = Path("outputs")
METRICS = ['Age', 'Goals', 'Assists', '% Passing']

def main():
    """Run the complete EDA workflow."""
    
    print("=" * 70)
    print("Sheffield United Right-Back Exploratory Data Analysis")
    print("=" * 70)
    
    # 1. Load data
    print("\n1. Loading data...")
    df = utils.load_data(DATA_PATH)
    print(f"   Loaded {len(df)} players with {len(df.columns)} features")
    
    # 2. Quick summary
    print("\n2. Dataset summary:")
    utils.quick_summary(df, n=3)
    
    # 3. Check missing values
    print("\n3. Missing values:")
    missing = df.isnull().sum()
    print(f"   Total missing: {missing.sum()}")
    
    # 4. Convert to numeric
    print("\n4. Converting metrics to numeric...")
    df = utils.to_numeric_safe(df, METRICS)
    
    # 5. Basic correlations
    print("\n5. Correlation analysis:")
    utils.show_correlations(df, METRICS)
    
    # 6. Generate visualizations
    print("\n6. Generating visualizations...")
    
    # Age distribution
    print("   - Age distribution histogram")
    fig, ax = plt.subplots(figsize=(8, 5))
    df['Age'].hist(bins=20, ax=ax, color='skyblue', edgecolor='black')
    ax.set_title('Distribution of Player Ages')
    ax.set_xlabel('Age')
    ax.set_ylabel('Count')
    utils.save_fig(fig, OUTPUT_DIR / 'age_distribution.png')
    
    # Correlation heatmap
    print("   - Correlation heatmap")
    fig = utils.plot_correlation_heatmap(df, METRICS)
    utils.save_fig(fig, OUTPUT_DIR / 'correlation_heatmap.png')
    
    # Age vs metrics scatter plots
    for metric in ['Goals', 'Assists', '% Passing']:
        print(f"   - Age vs {metric} scatter plot")
        fig = utils.plot_age_vs_metric(df, metric)
        filename = f"age_vs_{metric.lower().replace(' ', '_').replace('%', 'pct')}.png"
        utils.save_fig(fig, OUTPUT_DIR / filename)
    
    # Performance by age groups
    print("   - Performance by age groups")
    fig = utils.plot_age_distribution_by_groups(df)
    utils.save_fig(fig, OUTPUT_DIR / 'performance_by_age_groups.png')
    
    # 7. Generate insights
    print("\n7. Generating insights...")
    insights = utils.generate_correlation_insights(df, METRICS)
    print("\n" + insights)
    
    # 8. Generate complete report
    print("\n8. Generating comprehensive report...")
    report_path = OUTPUT_DIR / 'eda_report.md'
    utils.generate_eda_report(df, METRICS, output_path=report_path)
    
    print("\n" + "=" * 70)
    print("✓ Analysis complete!")
    print("=" * 70)
    print(f"\nOutputs saved to: {OUTPUT_DIR.absolute()}")
    print("\nGenerated files:")
    print("  - age_distribution.png")
    print("  - correlation_heatmap.png")
    print("  - age_vs_goals.png")
    print("  - age_vs_assists.png")
    print("  - age_vs_pct_passing.png")
    print("  - performance_by_age_groups.png")
    print("  - eda_report.md")


if __name__ == "__main__":
    main()
