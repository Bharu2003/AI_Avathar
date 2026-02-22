# Lightweight AI Coach Orchestrator

A modular prototype with:
- **FastAPI backend** (`main.py`) for session orchestration APIs
- **Rule-based coach router** (Coach Tara / Coach Ravi)
- **Session memory layer** with in-memory + optional Qdrant adapter
- **Streamlit frontend** (`app.py`) wired to backend endpoints

## Project structure

- `main.py` — FastAPI entrypoint
- `backend/models.py` — domain models
- `backend/orchestrator.py` — coach routing + persona prompts
- `backend/memory.py` — memory abstractions (in-memory and Qdrant adapter)
- `backend/service.py` — orchestration service methods
- `app.py` — Streamlit web UI
- `tests/` — unit tests for router and service

## Run

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
streamlit run app.py
```

Set custom backend URL for Streamlit if needed:

```bash
export COACH_API_URL=http://localhost:8000
```

## API endpoints

- `POST /start_session`
- `POST /set_goal`
- `POST /chat`
- `POST /switch_coach`
- `GET /health`
