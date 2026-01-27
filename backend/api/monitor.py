from fastapi import APIRouter
from typing import List, Dict, Any
from datetime import datetime, timedelta
import random

router = APIRouter()

@router.post("", response_model=Dict[str, Any])
def monitor() -> Dict[str, Any]:
    trend = []
    base = 10000

    for i in range(14):
        trend.append({
            "date": (datetime.now() - timedelta(days=13 - i)).strftime("%Y-%m-%d"),
            "revenue": base + random.randint(-2000, 2000),
        })

    total_revenue = sum(item["revenue"] for item in trend)
    avg_daily = total_revenue // len(trend)

    return {
        "total_revenue": total_revenue,
        "avg_daily_revenue": avg_daily,
        "alerts": [
            {
                "date": trend[6]["date"],
                "drop": "-17%",
            }
        ],
        "trend": trend,
    }
