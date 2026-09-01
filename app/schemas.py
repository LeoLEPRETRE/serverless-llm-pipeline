from pydantic import BaseModel, Field


class ReviewRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=8000)
    language: str | None = Field(default=None, max_length=30, examples=["python"])


class ReviewResponse(BaseModel):
    review: str
    model: str