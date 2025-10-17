"""
Scoring and ranking functions for RB recruitment.
"""
import numpy as np
import pandas as pd
from datetime import datetime

# --- helpers ---
def _as_numeric(series: pd.Series) -> pd.Series:
    """Best-effort conversion of mixed/string series to numeric.
    Strips non-numeric characters (%, commas, currency) before coercion.
    """
    if pd.api.types.is_numeric_dtype(series):
        return pd.to_numeric(series, errors="coerce")
    cleaned = series.astype(str).str.replace(r"[^0-9eE+\-\.]", "", regex=True)
    return pd.to_numeric(cleaned, errors="coerce")

def _z(s):
    mu, sd = s.mean(), s.std(ddof=0)
    if not np.isfinite(sd) or sd == 0:
        return pd.Series(0.0, index=s.index)
    return ((s - mu) / sd).clip(-3, 3)

def _norm01(s):
    s = pd.to_numeric(s, errors="coerce")
    lo, hi = s.min(), s.max()
    if not np.isfinite(lo) or not np.isfinite(hi) or hi == lo:
        return pd.Series(0.5, index=s.index)
    return (s - lo) / (hi - lo)

def _months_to_expiry(contract_str, ref=None):
    ref = ref or datetime.today()
    try:
        dt = datetime.strptime(str(contract_str), "%b-%y")
        if dt.year < 2000: dt = dt.replace(year=dt.year + 2000)
        months = (dt.year - ref.year)*12 + (dt.month - ref.month)
        return max(0, months)
    except Exception:
        return np.nan

# --- per90 ---
def make_per90(df, cols, minutes_col="Minutes"):
    out = df.copy()
    mins = pd.to_numeric(out.get(minutes_col), errors="coerce").fillna(0)
    factor = mins.replace(0, np.nan) / 90.0
    for c in cols:
        if c in out.columns and not c.endswith(" per90") and not c.endswith("per90"):
            values = pd.to_numeric(out[c], errors="coerce")
            out[c + " per90"] = values / factor
    return out

# --- standardise ---
def zscore_by_group(df, cols, group_col="League", clip=3.0):
    out = df.copy()
    if group_col in out.columns:
        g = out.groupby(group_col, dropna=False)
        for c in cols:
            if c in out.columns:
                tmp = f"__num__{c}__"
                out[tmp] = _as_numeric(out[c])
                out[c + "_z"] = g[tmp].transform(lambda s: _z(s).clip(-clip, clip))
                out.drop(columns=[tmp], inplace=True)
    else:
        for c in cols:
            if c in out.columns:
                tmp = _as_numeric(out[c])
                out[c + "_z"] = _z(tmp).clip(-clip, clip)
    return out

# --- pillars ---
def pillar_score(df, cols):
    use = [c for c in cols if c in df.columns]
    zcols = [c if c.endswith("_z") else c + "_z" for c in use]
    zcols = [c for c in zcols if c in df.columns]
    if not zcols:
        return pd.Series(0.0, index=df.index)
    return df[zcols].mean(axis=1).fillna(0.0)

def overall_score(df, weights):
    score = np.zeros(len(df))
    for k, w in weights.items():
        score += w * df.get(k, 0)
    return pd.Series(score, index=df.index)

def apply_bonuses(df, age_col="Age", minutes_col="Minutes",
                  age_range=(20,27), min_minutes=1800,
                  age_bonus=0.10, min_bonus=0.05):
    age = pd.to_numeric(df.get(age_col), errors="coerce")
    mins = pd.to_numeric(df.get(minutes_col), errors="coerce")
    age_ok = age.between(age_range[0], age_range[1], inclusive="both").fillna(False)
    min_ok = (mins >= min_minutes).fillna(False)
    return age_ok.astype(float)*age_bonus + min_ok.astype(float)*min_bonus

def feasibility(df, value_col="(€) Market Value", contract_col="Contract End", gbe_col="GBE", weights=None):
    weights = weights or {"value": 0.6, "contract": 0.3, "gbe": 0.1}
    vals = pd.to_numeric(df.get(value_col), errors="coerce").clip(lower=0)
    feas_value = 1 - _norm01(np.log1p(vals))
    if contract_col in df.columns:
        months = df[contract_col].apply(_months_to_expiry)
        feas_contract = 1 - _norm01(months)
    else:
        feas_contract = pd.Series(1.0, index=df.index)
    if gbe_col in df.columns:
        gbe_ok = df[gbe_col].astype(str).str.lower().isin(["yes","y","true","eligible"])
        feas_gbe = gbe_ok.astype(float)*1.0 + (~gbe_ok).astype(float)*0.7
    else:
        feas_gbe = pd.Series(1.0, index=df.index)
    score = (
        weights.get("value", 0.6) * feas_value
        + weights.get("contract", 0.3) * feas_contract
        + weights.get("gbe", 0.1) * feas_gbe
    )
    return score.clip(0, 1)

def make_flags(df):
    flags = []
    for _, row in df.iterrows():
        f = []
        # Cross volume vs efficiency
        try:
            crosses = float(row.get("Completed Crosses per90", np.nan))
            cross_eff = float(row.get("Cross Efficiency", np.nan))
            if np.isfinite(crosses) and np.isfinite(cross_eff):
                if crosses > df.get("Completed Crosses per90", pd.Series()).median(skipna=True) and cross_eff < df.get("Cross Efficiency", pd.Series()).median(skipna=True):
                    f.append("High cross volume; low efficiency")
        except Exception:
            pass
        if row.get("Successful Tackles per90_z",0) > 1 and row.get("Progressive Carries per90_z",0) < -1:
            f.append("Defensive profile; low progression")
        if row.get("Progressive Carries per90_z",0) > 1 and row.get("Tackles/Was Dribbled_z",0) < -0.5:
            f.append("Progressive; 1v1 risk")
        if row.get("Minutes",0) < 1200:
            f.append("Low minutes")
        flags.append("; ".join(f))
    return pd.Series(flags, index=df.index)