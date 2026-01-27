from fastapi import APIRouter
from pydantic import BaseModel
from kpi_intel.app.services.talk_to_data import agent

router = APIRouter()

class AskRequest(BaseModel):
    question: str

@router.post("/")
def ask_data(req: AskRequest):
    return agent.query(req.question)
