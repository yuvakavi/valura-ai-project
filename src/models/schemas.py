from pydantic import BaseModel

class Query(BaseModel):
    query: str
    user: dict = {}

class Response(BaseModel):
    event: str
    data: str
