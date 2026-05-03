from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional, List
from sse_starlette.sse import EventSourceResponse

from src.safety import check
from src.classifier import classify
from src.core.router import route
from src.core.streaming import event_stream

# ============================================
# APP INIT
# ============================================

app = FastAPI(
    title="Valura AI - Financial Advisory API",
    description="AI-powered financial advisory system with streaming responses",
    version="1.0.0"
)

# ============================================
# MODELS
# ============================================

class Holding(BaseModel):
    ticker: str
    quantity: float
    avg_cost: float


class UserProfile(BaseModel):
    name: Optional[str] = None
    portfolio: Optional[List[Holding]] = None
    risk_tolerance: Optional[str] = None


class QueryRequest(BaseModel):
    query: str = Field(..., description="User query")
    user: Optional[UserProfile] = None


# ============================================
# HEALTH CHECK
# ============================================

@app.get("/health")
async def health():
    return {"status": "OK"}


# ============================================
# MAIN ENDPOINT
# ============================================

@app.post("/query")
async def query(request: QueryRequest):

    query_text = request.query

    # 🔥 FINAL FIX: normalize user + portfolio
    user = {}
    if request.user:
        # Convert Pydantic model to dict but KEEP portfolio even if it's empty
        user = request.user.model_dump(exclude_none=False)

        # Convert portfolio items to pure dict (VERY IMPORTANT)
        if "portfolio" in user and user["portfolio"]:
            user["portfolio"] = [
                p if isinstance(p, dict) else p.model_dump()
                for p in user["portfolio"]
            ]
        
        # Remove None values after portfolio is handled
        user = {k: v for k, v in user.items() if v is not None}

    print(f"DEBUG MAIN: user={user}")

    async def generator():
        try:
            # 1. Safety
            yield {"event": "status", "data": "Checking safety"}
            safety = check(query_text)

            if safety.blocked:
                yield {"event": "error", "data": safety.message}
                return

            # 2. Classifier
            yield {"event": "status", "data": "Classifying"}
            result = classify(query_text)

            # 3. Routing
            yield {"event": "status", "data": "Routing"}

            data = {
                "user": user,
                "entities": result.entities,
                "intent": result.agent
            }

            print(f"DEBUG ROUTER DATA: {data}")

            response = route(result.agent, data)

            # 4. Final response
            yield {
                "event": "data",
                "data": str(response)
            }

        except Exception as e:
            import traceback
            traceback.print_exc()
            yield {
                "event": "error",
                "data": f"Internal error: {str(e)}"
            }

    return EventSourceResponse(event_stream(generator()))


# ============================================
# ROOT
# ============================================

@app.get("/")
async def root():
    return {
        "message": "Valura AI API Running",
        "docs": "/docs"
    }