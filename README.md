# Chatbot Widget Assignment

A full-stack take-home implementation for a floating chatbot widget with:
- React + Vite frontend
- FastAPI backend
- Gemini API integration
- In-memory session history
- Optional RAG over a fixed OWASP CSV dataset

This structure is aligned with the assignment requirements for a bottom-right chatbot widget, Gemini integration, session management, OWASP CSV retrieval, deployment readiness, and basic security practices. The assignment also explicitly allows a simple backend framework and a basic retrieval mechanism over the fixed OWASP dataset.

## Project Structure

```bash
chatbot-widget-assignment/
├── frontend/
├── backend/
└── README.md
```

## Features

### Frontend
- Floating chatbot launcher at the bottom-right
- Open/close widget interaction
- Chat bubble UI
- Typing indicator
- Mobile-friendly layout
- Smooth open animation

### Backend
- `POST /chat` endpoint
- `GET /health` endpoint
- In-memory conversation session history
- Gemini API response generation
- OWASP CSV retrieval using `rapidfuzz`
- RAG citations returned to frontend
- CORS configuration and input validation

## Why this implementation fits the assignment

The assignment asks for:
- a floating chatbot widget
- a backend that integrates Gemini
- session management for simple conversational context
- optional retrieval from a fixed OWASP Q&A CSV
- secure API key handling via environment variables
- production-readiness with logging/error handling and deployment support


## Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows PowerShell
pip install -r requirements.txt
cp .env.example .env
```

Add your Gemini API key to `.env`:

```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash
ALLOWED_ORIGINS=http://localhost:5173
```

Run the backend:

```bash
uvicorn main:app --reload --port 8000
```

## Frontend Setup

```bash
cd frontend
npm install
```

Create `.env` in `frontend/` if needed:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Run the frontend:

```bash
npm run dev
```

Open:

```text
http://localhost:5173
```

## How RAG works

1. User sends a message.
2. Backend searches the OWASP CSV for the most relevant `Question` / `Answer` rows.
3. Top results are formatted into a retrieval context block.
4. Gemini receives:
   - conversation history
   - retrieved OWASP context
   - current user message
5. Gemini returns a grounded response.

### Retrieval approach
- Dataset: `backend/dataset.csv`
- Matching: `rapidfuzz` scoring against both question and answer
- Default top-k: 3
- Minimum score threshold: 55


## Testing

Run backend tests:

```bash
cd backend
pytest
```

### Environment variables for backend
- `GEMINI_API_KEY`
- `GEMINI_MODEL`
- `ALLOWED_ORIGINS`
- `MAX_HISTORY_MESSAGES`
- `TOP_K_RAG_RESULTS`

### Production notes
- Replace in-memory sessions with Redis or a database for real production use.
- Add request logging and rate limiting.
- Tighten allowed CORS origins.
- Consider Docker for repeatable deployment.

## Recommended demo prompts
- `What is Broken Object Level Authorization?`
- `Can you recommend 3 measures to prevent XSS attacks?`
- `Explain SSRF in simple terms.`
- `Tell me a fun fact about Singapore.`

## Notes on Gemini SDK
This project uses the current official Google GenAI Python SDK (`google-genai`) and the `Client().models.generate_content(...)` pattern recommended in Google's current Gemini API docs.
