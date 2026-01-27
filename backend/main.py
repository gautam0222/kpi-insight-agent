from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.monitor import router as monitor_router
from api.ask import router as ask_router
from api.causal import router as causal_router
from api.recommend import router as recommend_router
from api.agent import router as agent_router


app = FastAPI(
    title="KPI Insight Agent",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(monitor_router, prefix="/monitor", tags=["Monitor"])
app.include_router(ask_router, prefix="/ask", tags=["Ask Data"])
app.include_router(causal_router, prefix="/causal", tags=["Causal Analysis"])
app.include_router(recommend_router, prefix="/recommend", tags=["Recommendations"])
app.include_router(agent_router, prefix="/agent", tags=["Agent"])

@app.get("/")
def root():
    return {"status": "KPI Insight Agent running"}
