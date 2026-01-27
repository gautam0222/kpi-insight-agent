from fastapi import APIRouter
from kpi_intel.app.core.data_loader import data_loader
import pandas as pd

router = APIRouter()

@router.post("")
def recommend_actions():
    df = data_loader.df.copy()

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Overall_Revenue"] = pd.to_numeric(df["Overall_Revenue"], errors="coerce")
    df = df.dropna(subset=["Date", "Overall_Revenue"])
    df = df.sort_values("Date")

    recent = df.tail(7)
    previous = df.iloc[-14:-7]

    recommendations = []

    # --- Category based recommendations ---
    if "Category" in df.columns:
        recent_cat = recent.groupby("Category")["Overall_Revenue"].sum()
        previous_cat = previous.groupby("Category")["Overall_Revenue"].sum()

        delta = (recent_cat - previous_cat).dropna()

        for cat, change in delta.items():
            if change < 0:
                recommendations.append({
                    "action": f"Increase promotions for {cat}",
                    "reason": f"{cat} revenue declined in the last 7 days",
                    "priority": "High" if abs(change) > 5000 else "Medium",
                    "expected_impact": "Revenue recovery in next cycle"
                })

    # --- Fallback ---
    if not recommendations:
        recommendations.append({
            "action": "Maintain current strategy",
            "reason": "No major negative revenue drivers detected",
            "priority": "Low",
            "expected_impact": "Stable performance"
        })

    return {
        "recommendations": recommendations
    }
