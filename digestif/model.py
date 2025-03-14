from pydantic import BaseModel

class FeedConfig(BaseModel):
    urls: list[str]
    prompt: str
