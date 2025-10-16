from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# === LOAD DATA ===
def load_data(path: str | Path) -> pd.DataFrame:
    """
    Load the dataset from the given path and apply minimal safe cleaning.

    - Strips whitespace from column names
    - Replaces dashes ('-' or '–') with NaN
    - Validates that the file exists
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    df = df.replace({"–": np.nan, "-": np.nan})
    return df


# === TYPE COERCION ===
def to_numeric_safe(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """
    Convert selected columns to numeric, ignoring non-numeric values.
    Removes commas and percentage signs first.
    """
    for c in cols:
        if c in df.columns:
            df[c] = (
                df[c]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.replace("%", "", regex=False)
            )
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


# === SAVE CHARTS ===
def save_fig(fig: plt.Figure, path: str | Path) -> None:
    """
    Save a matplotlib figure to the given path, creating parent dirs if needed.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches="tight", dpi=300)
    plt.close(fig)


# === QUICK CHECK ===

def quick_summary(df: pd.DataFrame, n: int = 5) -> None:
    """
    Print a quick summary of dataset structure and the first few rows.
    """
    print(f"Shape: {df.shape}")
    print("Columns:", list(df.columns))
    print(df.head(n))


# === CORRELATION CHECK ===
def show_correlations(df: pd.DataFrame, cols: list[str]) -> None:
    """
    Print the correlation matrix for selected columns.
    """
    print("Correlation matrix:")
    print(df[cols].corr())


# === VISUALIZATION FUNCTIONS ===
def plot_correlation_heatmap(df: pd.DataFrame, cols: list[str], figsize=(10, 8)) -> plt.Figure:
    """
    Create a correlation heatmap for selected columns.
    
    Args:
        df: DataFrame containing the data
        cols: List of column names to include in correlation analysis
        figsize: Figure size tuple (width, height)
    
    Returns:
        matplotlib Figure object
    """
    import seaborn as sns
    
    fig, ax = plt.subplots(figsize=figsize)
    corr_matrix = df[cols].corr()
    
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt='.3f',
        cmap='coolwarm',
        center=0,
        square=True,
        linewidths=1,
        cbar_kws={"shrink": 0.8},
        ax=ax
    )
    ax.set_title('Correlation Heatmap: Age vs Performance Metrics', fontsize=14, pad=20)
    plt.tight_layout()
    
    return fig


def plot_age_vs_metric(df: pd.DataFrame, metric: str, figsize=(10, 6)) -> plt.Figure:
    """
    Create a scatter plot showing age vs a specific performance metric.
    
    Args:
        df: DataFrame containing the data
        metric: Column name for the performance metric
        figsize: Figure size tuple (width, height)
    
    Returns:
        matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Filter out NaN values
    plot_data = df[['Age', metric]].dropna()
    
    ax.scatter(plot_data['Age'], plot_data[metric], alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
    
    # Add trend line
    if len(plot_data) > 1:
        z = np.polyfit(plot_data['Age'], plot_data[metric], 1)
        p = np.poly1d(z)
        ax.plot(plot_data['Age'].sort_values(), p(plot_data['Age'].sort_values()), 
                "r--", alpha=0.8, linewidth=2, label=f'Trend line')
    
    ax.set_xlabel('Age', fontsize=12)
    ax.set_ylabel(metric, fontsize=12)
    ax.set_title(f'Age vs {metric}', fontsize=14, pad=20)
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()
    
    return fig


def plot_age_distribution_by_groups(df: pd.DataFrame, bins=[18, 23, 28, 33, 40], 
                                   labels=['18-22', '23-27', '28-32', '33+'],
                                   figsize=(12, 6)) -> plt.Figure:
    """
    Create visualizations showing performance metrics by age groups.
    
    Args:
        df: DataFrame containing the data
        bins: Age bin edges
        labels: Labels for age groups
        figsize: Figure size tuple (width, height)
    
    Returns:
        matplotlib Figure object
    """
    # Create age groups
    df_copy = df.copy()
    df_copy['Age_Group'] = pd.cut(df_copy['Age'], bins=bins, labels=labels, include_lowest=True)
    
    fig, axes = plt.subplots(1, 3, figsize=figsize)
    
    metrics = ['Goals', 'Assists', '% Passing']
    for idx, metric in enumerate(metrics):
        ax = axes[idx]
        data_by_group = [df_copy[df_copy['Age_Group'] == group][metric].dropna() 
                        for group in labels]
        
        bp = ax.boxplot(data_by_group, labels=labels, patch_artist=True)
        
        # Color the boxes
        for patch in bp['boxes']:
            patch.set_facecolor('skyblue')
            patch.set_alpha(0.7)
        
        ax.set_xlabel('Age Group', fontsize=11)
        ax.set_ylabel(metric, fontsize=11)
        ax.set_title(f'{metric} by Age Group', fontsize=12)
        ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    return fig


# === INSIGHTS GENERATION ===
def generate_correlation_insights(df: pd.DataFrame, cols: list[str]) -> str:
    """
    Generate textual insights based on correlation analysis.
    
    Args:
        df: DataFrame containing the data
        cols: List of column names to analyze
    
    Returns:
        Formatted string with insights
    """
    corr_matrix = df[cols].corr()
    insights = []
    
    insights.append("# Correlation Analysis Insights\n")
    insights.append("## Key Findings:\n")
    
    # Age correlations
    age_corrs = corr_matrix.loc['Age'].drop('Age')
    insights.append("### Age vs Performance Metrics:\n")
    
    for metric, corr_value in age_corrs.items():
        strength = "weak" if abs(corr_value) < 0.3 else ("moderate" if abs(corr_value) < 0.7 else "strong")
        direction = "positive" if corr_value > 0 else "negative"
        
        insights.append(f"- **Age vs {metric}**: {direction} correlation ({corr_value:.3f}) - {strength} relationship\n")
    
    # Goals and Assists correlation
    if 'Goals' in cols and 'Assists' in cols:
        goals_assists_corr = corr_matrix.loc['Goals', 'Assists']
        insights.append(f"\n### Goals vs Assists:\n")
        insights.append(f"- Moderate positive correlation ({goals_assists_corr:.3f})\n")
        insights.append(f"- Players who score more tend to also provide more assists\n")
    
    return ''.join(insights)


def generate_eda_report(df: pd.DataFrame, cols: list[str], output_path: str | Path = None) -> str:
    """
    Generate a comprehensive EDA report with insights and recommendations.
    
    Args:
        df: DataFrame containing the data
        cols: List of column names to analyze (should include 'Age' and performance metrics)
        output_path: Optional path to save the report as markdown
    
    Returns:
        Report as a string
    """
    report_lines = []
    
    # Header
    report_lines.append("# Exploratory Data Analysis Report\n")
    report_lines.append("## Sheffield United Right-Back Analysis\n\n")
    report_lines.append(f"**Date**: {pd.Timestamp.now().strftime('%Y-%m-%d')}\n\n")
    
    # Dataset Overview
    report_lines.append("---\n\n")
    report_lines.append("## 1. Dataset Overview\n\n")
    report_lines.append(f"- **Total Players**: {len(df)}\n")
    report_lines.append(f"- **Total Features**: {len(df.columns)}\n")
    report_lines.append(f"- **Analysis Focus**: Age and Performance Metrics Correlation\n\n")
    
    # Age statistics
    if 'Age' in df.columns:
        age_stats = df['Age'].describe()
        report_lines.append("### Age Distribution:\n")
        report_lines.append(f"- **Mean Age**: {age_stats['mean']:.1f} years\n")
        report_lines.append(f"- **Median Age**: {age_stats['50%']:.1f} years\n")
        report_lines.append(f"- **Age Range**: {age_stats['min']:.0f} - {age_stats['max']:.0f} years\n")
        report_lines.append(f"- **Standard Deviation**: {age_stats['std']:.1f} years\n\n")
    
    # Correlation Analysis
    report_lines.append("---\n\n")
    report_lines.append("## 2. Correlation Analysis\n\n")
    
    corr_matrix = df[cols].corr()
    report_lines.append("### Correlation Matrix:\n\n")
    report_lines.append("```\n")
    report_lines.append(corr_matrix.to_string())
    report_lines.append("\n```\n\n")
    
    # Add insights
    insights = generate_correlation_insights(df, cols)
    report_lines.append(insights)
    report_lines.append("\n")
    
    # Key Observations
    report_lines.append("---\n\n")
    report_lines.append("## 3. Key Observations\n\n")
    
    age_corrs = corr_matrix.loc['Age'].drop('Age')
    
    if age_corrs['Goals'] < 0:
        report_lines.append("1. **Age vs Goals**: Slight negative correlation suggests younger players may have marginally higher goal-scoring output, though the relationship is weak.\n\n")
    
    if age_corrs['% Passing'] > 0:
        report_lines.append("2. **Age vs Passing Accuracy**: Positive correlation indicates that older, more experienced players tend to have better passing accuracy.\n\n")
    
    if 'Goals' in cols and 'Assists' in cols:
        goals_assists_corr = corr_matrix.loc['Goals', 'Assists']
        if goals_assists_corr > 0.4:
            report_lines.append("3. **Goals vs Assists**: Strong positive correlation shows that attacking-minded right-backs contribute to both goals and assists.\n\n")
    
    # Recommendations
    report_lines.append("---\n\n")
    report_lines.append("## 4. Recommendations for Sheffield United\n\n")
    
    report_lines.append("### Recruitment Strategy:\n\n")
    report_lines.append("1. **Balance Youth and Experience**:\n")
    report_lines.append("   - Younger players (< 25) may offer attacking output\n")
    report_lines.append("   - Experienced players (28+) provide reliability in passing and build-up play\n\n")
    
    report_lines.append("2. **Target Profile**:\n")
    report_lines.append("   - Look for players aged 25-28 who combine both attributes\n")
    report_lines.append("   - Prioritize passing accuracy for possession-based play\n")
    report_lines.append("   - Consider attacking metrics for more offensive roles\n\n")
    
    report_lines.append("3. **Data-Driven Insights**:\n")
    report_lines.append("   - Age alone is not a strong predictor of performance\n")
    report_lines.append("   - Evaluate players on multiple metrics rather than single attributes\n")
    report_lines.append("   - Consider tactical fit alongside statistical performance\n\n")
    
    # Conclusion
    report_lines.append("---\n\n")
    report_lines.append("## 5. Conclusion\n\n")
    report_lines.append("The analysis reveals that while age has some correlation with specific performance metrics, ")
    report_lines.append("it is not a dominant factor. The weak correlations suggest that individual player quality, ")
    report_lines.append("tactical system, and playing style are likely more important than age alone. ")
    report_lines.append("Sheffield United should adopt a holistic approach to recruitment, considering multiple ")
    report_lines.append("factors beyond age when evaluating right-back candidates.\n\n")
    
    report_lines.append("---\n\n")
    report_lines.append("*This report was generated using exploratory data analysis techniques on right-back player data.*\n")
    
    report_text = ''.join(report_lines)
    
    # Save to file if path provided
    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(report_text)
        print(f"Report saved to: {output_path}")
    
    return report_text