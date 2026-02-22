import unittest

from backend.service import CoachService


class TestCoachService(unittest.TestCase):
    def test_end_to_end_session(self):
        service = CoachService()
        session = service.start_session("Grade 6–8", "Motivation Coach", "Calm", "English")
        sid = session["session_id"]

        goal = service.set_goal(sid, "Improve focus")
        self.assertEqual(goal["goal"], "Improve focus")

        chat = service.chat(sid, "I procrastinate")
        self.assertIn("reply", chat)
        self.assertGreater(chat["turns"], 1)

        switched = service.switch_coach(sid, "Exam Strategist")
        self.assertEqual(switched["coach"], "Coach Ravi")


if __name__ == "__main__":
    unittest.main()
