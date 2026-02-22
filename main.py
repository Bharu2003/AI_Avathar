from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.service import CoachService

app = FastAPI(title="Lightweight AI Coach Orchestrator", version="0.2.0")
service = CoachService()


class StartSessionRequest(BaseModel):
    age_group: str
    mentor_role: str
    tone: str
    language: str


class GoalRequest(BaseModel):
    session_id: str
    goal: str


class ChatRequest(BaseModel):
    session_id: str
    message: str


class SwitchCoachRequest(BaseModel):
    session_id: str
    mentor_role: str


@app.post("/start_session")
def start_session(payload: StartSessionRequest):
    return service.start_session(payload.age_group, payload.mentor_role, payload.tone, payload.language)


@app.post("/set_goal")
def set_goal(payload: GoalRequest):
    try:
        return service.set_goal(payload.session_id, payload.goal)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/chat")
def chat(payload: ChatRequest):
    try:
        return service.chat(payload.session_id, payload.message)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/switch_coach")
def switch_coach(payload: SwitchCoachRequest):
    try:
        return service.switch_coach(payload.session_id, payload.mentor_role)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/health")
def health():
    return {"status": "ok"}
