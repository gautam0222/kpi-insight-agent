from fastapi import APIRouter
import pandas as pd
from kpi_intel.app.core.data_loader import data_loader

router = APIRouter()

@router.post("")
def causal_analysis():
    df = data_loader.df.copy()

    # --- Clean data ---
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Overall_Revenue"] = pd.to_numeric(df["Overall_Revenue"], errors="coerce")
    df = df.dropna(subset=["Date", "Overall_Revenue"])

    df = df.sort_values("Date")

    # --- Window split ---
    recent = df.tail(7)
    previous = df.iloc[-14:-7]

    recent_total = recent["Overall_Revenue"].sum()
    previous_total = previous["Overall_Revenue"].sum()

    change_pct = round(
        ((recent_total - previous_total) / previous_total) * 100, 2
    )

    causes = []

    # --- Category level contribution ---
    if "Category" in df.columns:
        recent_cat = recent.groupby("Category")["Overall_Revenue"].sum()
        previous_cat = previous.groupby("Category")["Overall_Revenue"].sum()

        delta = (recent_cat - previous_cat).dropna()

        for cat, value in delta.items():
            if value < 0:
                causes.append({
                    "factor": cat,
                    "impact": round(value, 2),
                    "type": "Category Decline",
                    "explanation": f"Revenue from {cat} decreased compared to previous period"
                })

    # Sort causes by absolute impact
    causes = sorted(causes, key=lambda x: abs(x["impact"]), reverse=True)

    return {
        "kpi": "Overall Revenue",
        "window": "Last 7 days vs Previous 7 days",
        "change_percent": change_pct,
        "direction": "decrease" if change_pct < 0 else "increase",
        "top_causes": causes[:5]
    }
