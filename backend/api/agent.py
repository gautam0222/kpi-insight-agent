from fastapi import APIRouter
from api.monitor import monitor
from api.causal import causal_analysis
from api.recommend import recommend_actions

router = APIRouter()

@router.post("/run")
def run_agent():
    # 1. Monitor KPIs
    monitor_data = monitor()

    alerts = monitor_data.get("alerts", [])

    # 2. Decide if agent should act
    if not alerts:
        return {
            "status": "stable",
            "message": "No significant KPI deviations detected",
            "dashboard": monitor_data
        }

    # 3. Run causal analysis
    causal_data = causal_analysis()

    # 4. Generate recommendations
    recommendations = recommend_actions()

    return {
        "status": "action_required",
        "summary": "Revenue deviation detected. Agent performed analysis.",
        "monitor": monitor_data,
        "causal": causal_data,
        "recommendations": recommendations
    }
