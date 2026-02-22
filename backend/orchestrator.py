from __future__ import annotations

from dataclasses import dataclass

from .models import AgeGroup, CoachName

SUPPORTIVE_ROLES = {"Motivation Coach", "Emotional Support Guide"}


@dataclass(slots=True)
class CoachProfile:
    name: CoachName
    system_prompt: str


COACH_PROMPTS = {
    CoachName.TARA: (
        "You are Coach Tara, calm, encouraging, and age-appropriate for Grades 6-8. "
        "Use short, warm explanations and confidence-building language."
    ),
    CoachName.RAVI: (
        "You are Coach Ravi, energetic and exam-focused for Grades 9-12. "
        "Give practical steps, accountability, and revision tactics."
    ),
}


def pick_coach(age_group: AgeGroup, mentor_role: str) -> CoachProfile:
    """Rule-based router for coach assignment."""
    if age_group == AgeGroup.GRADE_6_8 and mentor_role in SUPPORTIVE_ROLES:
        coach = CoachName.TARA
    else:
        coach = CoachName.RAVI
    return CoachProfile(name=coach, system_prompt=COACH_PROMPTS[coach])
