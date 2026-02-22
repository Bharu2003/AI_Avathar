from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import asdict
from typing import Dict, Optional

from .models import SessionState


class SessionMemory(ABC):
    @abstractmethod
    def save(self, state: SessionState) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, session_id: str) -> Optional[SessionState]:
        raise NotImplementedError


class InMemorySessionStore(SessionMemory):
    """Simple dev-friendly store; replace with Qdrant-backed implementation in production."""

    def __init__(self) -> None:
        self._sessions: Dict[str, SessionState] = {}

    def save(self, state: SessionState) -> None:
        self._sessions[state.session_id] = state

    def get(self, session_id: str) -> Optional[SessionState]:
        return self._sessions.get(session_id)


class QdrantSessionStore(SessionMemory):
    """Optional adapter for Qdrant. Falls back gracefully if dependency is absent."""

    def __init__(self, url: str = "http://localhost:6333", collection: str = "coach_sessions") -> None:
        self.url = url
        self.collection = collection
        self._client = None
        try:
            from qdrant_client import QdrantClient

            self._client = QdrantClient(url=url)
        except Exception:
            self._client = None

    def save(self, state: SessionState) -> None:
        if self._client is None:
            return
        payload = asdict(state)
        payload["age_group"] = state.age_group.value
        payload["coach"] = state.coach.value
        payload["turns"] = [
            {"role": t.role, "text": t.text, "timestamp": t.timestamp.isoformat()} for t in state.turns
        ]
        self._client.upsert(
            collection_name=self.collection,
            points=[{"id": state.session_id, "vector": [0.0], "payload": payload}],
        )

    def get(self, session_id: str) -> Optional[SessionState]:
        if self._client is None:
            return None
        result = self._client.retrieve(collection_name=self.collection, ids=[session_id], with_payload=True)
        if not result:
            return None
        payload = result[0].payload
        # Lightweight reconstruction for demo use.
        from .models import AgeGroup, CoachName

        return SessionState(
            session_id=session_id,
            age_group=AgeGroup(payload["age_group"]),
            mentor_role=payload["mentor_role"],
            tone=payload["tone"],
            language=payload["language"],
            coach=CoachName(payload["coach"]),
            goal=payload.get("goal"),
            turns=[],
        )
