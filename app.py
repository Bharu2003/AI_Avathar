from __future__ import annotations

import os
from typing import Any, Dict

import requests
import streamlit as st

API_BASE_URL = os.getenv("COACH_API_URL", "http://localhost:8000")

st.set_page_config(page_title="Lightweight AI Coach Orchestrator", page_icon="🎯", layout="wide")

if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "coach" not in st.session_state:
    st.session_state.coach = "-"


CUSTOM_CSS = """
<style>
.hero {padding: 1.5rem 1.8rem; border-radius: 14px; background: linear-gradient(120deg,#1d4ed8,#4338ca); color: white; margin-bottom: 1rem;}
.card {border-radius: 12px; border: 1px solid #e2e8f0; background: white; padding: 1rem; margin-bottom: .9rem;}
.small {font-size:.86rem; color:#475569;}
</style>
"""


st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
st.markdown(
    """
<div class='hero'>
<h2>🎯 Lightweight AI Coach Orchestrator</h2>
<p>Real backend-connected demo for student coaching across personas, tone, language, and goals.</p>
</div>
""",
    unsafe_allow_html=True,
)


def call_api(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.post(f"{API_BASE_URL}{path}", json=payload, timeout=15)
    response.raise_for_status()
    return response.json()


left, right = st.columns([1.1, 0.9], gap="large")

with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("1) Start Session")
    age_group = st.selectbox("Age group", ["Grade 6–8", "Grade 9–12"])
    role = st.selectbox("Mentor role", ["Study Planner", "Motivation Coach", "Exam Strategist", "Emotional Support Guide"])
    tone = st.select_slider("Tone", ["Calm", "Supportive", "Balanced", "Energetic"])
    language = st.selectbox("Language", ["English", "Hindi", "Tamil", "Kannada", "Bilingual"])
    if st.button("Start Session", type="primary", use_container_width=True):
        try:
            res = call_api(
                "/start_session",
                {"age_group": age_group, "mentor_role": role, "tone": tone, "language": language},
            )
            st.session_state.session_id = res["session_id"]
            st.session_state.coach = res["coach"]
            st.success(f"Session: {res['session_id']} | Active coach: {res['coach']}")
        except Exception as exc:
            st.error(f"Could not start session: {exc}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("2) Set Goal")
    goal = st.text_area("Goal", "Complete a 2-week science revision plan")
    if st.button("Save Goal", use_container_width=True, disabled=not st.session_state.session_id):
        try:
            call_api("/set_goal", {"session_id": st.session_state.session_id, "goal": goal})
            st.success("Goal saved")
        except Exception as exc:
            st.error(f"Could not save goal: {exc}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("3) Chat")
    message = st.text_input("Message", "I get distracted while studying.")
    if st.button("Send", use_container_width=True, disabled=not st.session_state.session_id):
        try:
            res = call_api("/chat", {"session_id": st.session_state.session_id, "message": message})
            st.info(f"Coach response: {res['reply']}")
        except Exception as exc:
            st.error(f"Chat failed: {exc}")
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Session Status")
    st.write(f"**API:** {API_BASE_URL}")
    st.write(f"**Session ID:** {st.session_state.session_id or '-'}")
    st.write(f"**Current Coach:** {st.session_state.coach}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Switch Coach")
    switch_role = st.selectbox("New mentor role", ["Study Planner", "Motivation Coach", "Exam Strategist", "Emotional Support Guide"])
    if st.button("Switch", use_container_width=True, disabled=not st.session_state.session_id):
        try:
            res = call_api("/switch_coach", {"session_id": st.session_state.session_id, "mentor_role": switch_role})
            st.session_state.coach = res["coach"]
            st.success(f"Switched to {res['coach']}")
        except Exception as exc:
            st.error(f"Switch failed: {exc}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("API endpoints")
    st.code("""POST /start_session
POST /set_goal
POST /chat
POST /switch_coach
GET  /health""")
    st.markdown("<p class='small'>Audio endpoint can be added at /audio_chat using Whisper transcription.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
