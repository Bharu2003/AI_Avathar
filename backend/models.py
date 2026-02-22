from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional


class AgeGroup(str, Enum):
    GRADE_6_8 = "Grade 6–8"
    GRADE_9_12 = "Grade 9–12"


class CoachName(str, Enum):
    TARA = "Coach Tara"
    RAVI = "Coach Ravi"


@dataclass(slots=True)
class ChatTurn:
    role: str
    text: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(slots=True)
class SessionState:
    session_id: str
    age_group: AgeGroup
    mentor_role: str
    tone: str
    language: str
    coach: CoachName
    goal: Optional[str] = None
    turns: List[ChatTurn] = field(default_factory=list)
