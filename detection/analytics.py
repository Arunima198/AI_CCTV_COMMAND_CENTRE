import numpy as np
import pandas as pd

def make_synthetic_data(rows=200, seed=42):
    rng = np.random.default_rng(seed)
    start = pd.Timestamp.now().floor("min") - pd.Timedelta(minutes=rows - 1)
    timestamps = pd.date_range(start=start, periods=rows, freq="min")
    zones = np.array(["Main Gate", "Central Plaza", "Queue Area", "Exit"])
    # Create plausible changing values with random variation; these are simulated only.
    wave = 22 + 13 * np.sin(np.linspace(0, 4 * np.pi, rows))
    counts = np.clip(np.round(wave + rng.normal(0, 7, rows)), 0, 150).astype(int)
    return pd.DataFrame({
        "timestamp": timestamps,
        "zone": rng.choice(zones, size=rows),
        "people_count": counts
    })

def load_csv(file):
    df = pd.read_csv(file)
    if "people_count" not in df.columns:
        raise ValueError("CSV must include a 'people_count' column.")
    df["people_count"] = pd.to_numeric(df["people_count"], errors="raise")
    if (df["people_count"] < 0).any():
        raise ValueError("'people_count' cannot contain negative values.")
    if "timestamp" not in df.columns:
        df["timestamp"] = pd.date_range("2025-01-01", periods=len(df), freq="min")
    else:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        if df["timestamp"].isna().any():
            raise ValueError("Some timestamps could not be parsed.")
    if "zone" not in df.columns:
        df["zone"] = "Unspecified"
    df["zone"] = df["zone"].fillna("Unspecified").astype(str)
    return df[["timestamp", "zone", "people_count"]].sort_values("timestamp")

def analyze_records(df, threshold):
    grouped = (df.groupby("zone", as_index=False)
        .agg(record_count=("people_count", "size"),
             average_people=("people_count", "mean"),
             peak_people=("people_count", "max"),
             alert_records=("people_count", lambda x: int((x >= threshold).sum()))))
    grouped["average_people"] = grouped["average_people"].round(1)
    grouped["alert"] = grouped["peak_people"] >= threshold
    grouped["alert_level"] = np.where(grouped["peak_people"] >= threshold * 1.5, "HIGH",
                               np.where(grouped["peak_people"] >= threshold, "MEDIUM", "NORMAL"))
    return grouped.sort_values("peak_people", ascending=False)
