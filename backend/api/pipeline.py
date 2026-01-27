from fastapi import APIRouter
from kpi_intel.app.services.monitor import monitor
from kpi_intel.app.services.causal import analyzer
from kpi_intel.app.services.recommend import recommender

router = APIRouter()

@router.post("/")
def run_pipeline():
    alerts = monitor.detect_changes()["alerts"]
    results = []

    for alert in alerts[:3]:
        cause = analyzer.analyze_cause(alert)
        recs = recommender.generate_recommendations(cause)
        results.append({
            "alert": alert,
            "causal": cause,
            "recommendations": recs
        })

    return results
