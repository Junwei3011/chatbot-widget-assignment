from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from gemini_service import GeminiService
from models import ChatRequest, ChatResponse, Citation, HealthResponse
from rag_search import build_rag_context, search_owasp
from session_store import SessionStore

settings = get_settings()
store = SessionStore(max_history_messages=settings.max_history_messages)
gemini_service = GeminiService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="Chatbot Widget Backend", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok", model=settings.gemini_model)


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    message = request.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    history = store.get_history(request.session_id)
    matches = search_owasp(message)
    rag_context = build_rag_context(matches)

    response_text = gemini_service.generate_reply(
        message=message,
        history=history,
        rag_context=rag_context,
    )
    store.append_turn(request.session_id, message, response_text)

    citations = [Citation(question=item.question, score=item.score) for item in matches]
    return ChatResponse(
        response=response_text,
        citations=citations,
        used_rag=bool(matches),
        session_id=request.session_id,
    )
