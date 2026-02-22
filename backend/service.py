from __future__ import annotations

import uuid
from dataclasses import asdict

from .memory import InMemorySessionStore, SessionMemory
from .models import AgeGroup, ChatTurn, SessionState
from .orchestrator import pick_coach


class CoachService:
    def __init__(self, memory: SessionMemory | None = None) -> None:
        self.memory = memory or InMemorySessionStore()

    def start_session(self, age_group: str, mentor_role: str, tone: str, language: str) -> dict:
        age = AgeGroup(age_group)
        coach = pick_coach(age, mentor_role)
        state = SessionState(
            session_id=str(uuid.uuid4()),
            age_group=age,
            mentor_role=mentor_role,
            tone=tone,
            language=language,
            coach=coach.name,
        )
        self.memory.save(state)
        response = asdict(state)
        response["age_group"] = state.age_group.value
        response["coach"] = state.coach.value
        response["turns"] = []
        return response

    def set_goal(self, session_id: str, goal: str) -> dict:
        state = self._require_session(session_id)
        state.goal = goal
        self.memory.save(state)
        return {"session_id": session_id, "goal": goal}

    def chat(self, session_id: str, message: str) -> dict:
        state = self._require_session(session_id)
        state.turns.append(ChatTurn(role="user", text=message))
        reply = self._mock_llm_reply(state, message)
        state.turns.append(ChatTurn(role="assistant", text=reply))
        self.memory.save(state)
        return {"coach": state.coach.value, "reply": reply, "turns": len(state.turns)}

    def switch_coach(self, session_id: str, mentor_role: str) -> dict:
        state = self._require_session(session_id)
        coach = pick_coach(state.age_group, mentor_role)
        state.mentor_role = mentor_role
        state.coach = coach.name
        self.memory.save(state)
        return {"session_id": session_id, "coach": state.coach.value}

    def _require_session(self, session_id: str) -> SessionState:
        state = self.memory.get(session_id)
        if state is None:
            raise ValueError(f"Session not found: {session_id}")
        return state

    @staticmethod
    def _mock_llm_reply(state: SessionState, message: str) -> str:
        base = (
            "Great effort. Let's break this into 3 tiny actions for today."
            if state.coach.value == "Coach Tara"
            else "Nice ambition. Here's a focused exam plan with clear milestones."
        )
        goal_part = f" Goal: {state.goal}." if state.goal else ""
        return f"{base}{goal_part} You said: {message}"
