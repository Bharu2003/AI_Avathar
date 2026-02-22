import unittest

from backend.models import AgeGroup, CoachName
from backend.orchestrator import pick_coach


class TestOrchestrator(unittest.TestCase):
    def test_tara_for_supportive_middle_school(self):
        coach = pick_coach(AgeGroup.GRADE_6_8, "Motivation Coach")
        self.assertEqual(coach.name, CoachName.TARA)

    def test_ravi_for_exam_roles(self):
        coach = pick_coach(AgeGroup.GRADE_9_12, "Exam Strategist")
        self.assertEqual(coach.name, CoachName.RAVI)


if __name__ == "__main__":
    unittest.main()
