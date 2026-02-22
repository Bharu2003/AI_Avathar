import streamlit as st

st.set_page_config(
    page_title="Lightweight AI Coach Orchestrator",
    page_icon="🎯",
    layout="wide",
)

CUSTOM_CSS = """
<style>
.main {
    background: linear-gradient(180deg, #f5f7ff 0%, #ffffff 35%, #f8fbff 100%);
}
.hero {
    padding: 2rem 2.2rem;
    border-radius: 20px;
    background: linear-gradient(120deg, #1d4ed8 0%, #2563eb 35%, #4f46e5 100%);
    color: white;
    box-shadow: 0 15px 45px rgba(37, 99, 235, 0.25);
    margin-bottom: 1.2rem;
}
.hero h1 {
    margin-bottom: 0.5rem;
}
.card {
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    background: white;
    padding: 1rem;
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
    margin-bottom: 1rem;
}
.metric {
    border-radius: 14px;
    padding: 0.8rem;
    text-align: center;
    background: #eff6ff;
    border: 1px solid #dbeafe;
}
.badge {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
    background: #eef2ff;
    color: #3730a3;
    font-size: 0.75rem;
    font-weight: 700;
    margin-right: 0.4rem;
}
.small {
    color: #475569;
    font-size: 0.9rem;
}
.footer {
    margin-top: 2rem;
    text-align: center;
    color: #64748b;
    font-size: 0.85rem;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.markdown(
    """
<div class="hero">
  <h1>🎯 Lightweight AI Coach Orchestrator</h1>
  <p>Personalized mentoring for students through coach personas, multilingual guidance,
  and text/audio interactions — powered by FastAPI + Streamlit + Qdrant.</p>
</div>
""",
    unsafe_allow_html=True,
)

left, right = st.columns([1.1, 0.9], gap="large")

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Start a Coaching Session")

    age_group = st.selectbox("Age group", ["Grade 6–8", "Grade 9–12"])
    role = st.selectbox(
        "Mentor role",
        [
            "Study Planner",
            "Motivation Coach",
            "Exam Strategist",
            "Emotional Support Guide",
        ],
    )
    tone = st.select_slider("Tone", ["Calm", "Supportive", "Balanced", "Energetic"])
    language = st.selectbox("Language", ["English", "Hindi", "Tamil", "Kannada", "Bilingual"])
    goal = st.text_area("Student Goal", "I want to build a 2-week math revision plan.")

    coach = "Coach Tara" if age_group == "Grade 6–8" and role in ["Motivation Coach", "Emotional Support Guide"] else "Coach Ravi"

    if st.button("Start Session", use_container_width=True, type="primary"):
        st.success(f"Session created with **{coach}** in **{language}** using a **{tone}** tone.")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Live Chat Preview")
    user_msg = st.text_input("Type a message", "I get distracted while studying. Help me focus.")
    if st.button("Send Message", use_container_width=True):
        st.info(f"You: {user_msg}")
        st.success(
            f"{coach}: Great honesty! Let's create a short focus sprint with breaks so you can stay consistent."
        )
    st.caption("Audio chat can be connected to `/audio_chat` using OpenAI Whisper transcription.")
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Why this experience works")
    st.markdown(
        """
- **Persona-routing** selects the right coach based on age + role.
- **Adaptive tone and language** make responses relatable.
- **Session memory (Qdrant)** stores goals and context.
- **Text + audio** interactions support diverse learning styles.
"""
    )
    st.markdown("<span class='badge'>FastAPI</span><span class='badge'>Streamlit</span><span class='badge'>Qdrant</span><span class='badge'>Whisper</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("System Endpoints")
    st.code(
        """POST /start_session
POST /set_goal
POST /chat
POST /switch_coach
POST /audio_chat""",
        language="bash",
    )
    st.markdown("<p class='small'>Designed for modular upgrades: text-to-speech, avatars, and analytics can be added later.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    c1.markdown("<div class='metric'><h3>2</h3><p>Coach Personas</p></div>", unsafe_allow_html=True)
    c2.markdown("<div class='metric'><h3>5</h3><p>Core API Routes</p></div>", unsafe_allow_html=True)

st.markdown('<p class="footer">Built for student-first, low-friction AI coaching journeys.</p>', unsafe_allow_html=True)
