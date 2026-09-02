import logging

from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException

from app.config import Settings, get_settings
from app.llm_client import LLMError, review_code
from app.schemas import ReviewRequest, ReviewResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    get_settings()
    yield

app = FastAPI(title="Serverless LLM Pipeline", version="0.1.0", lifespan=lifespan)

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/v1/review", response_model=ReviewResponse)
async def review(request: ReviewRequest, settings: Settings = Depends(get_settings)):
    try:
        result = await review_code(request.code, request.language, settings)
    except LLMError as exc:
        logger.error("Échec de l'appel LLM : %s", exc)
        raise HTTPException(status_code=502, detail="Le service LLM est indisponible") from exc
    return ReviewResponse(review=result, model=settings.groq_model)