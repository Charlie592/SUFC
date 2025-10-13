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