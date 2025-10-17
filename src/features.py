"""
Feature definitions and utility functions for right-back recruitment analysis.
"""

# Pillar metric lists
BUILD_UP = ["% Passing","Progressive Carries per90","Ball Prog. by Carrying per90",
            "Pass Receipts in Space Completed","% Passing Under Pressure"]
CREATION = ["Expected Assists per90","Open Play Key Passes per90",
            "Completed Crosses per90","Cross Efficiency","xT Passing per90"]
DEFENDING = ["Successful Tackles per90","Interceptions per90",
             "Tackles/Was Dribbled","% Aerial Wins"]

def available(df, cols):
    """
    Return list of columns from `cols` that are present in DataFrame `df`.
    """
    return [c for c in cols if c in df.columns]
