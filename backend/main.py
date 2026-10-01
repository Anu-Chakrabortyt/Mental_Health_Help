from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from backend.AI_agents import process_query


app = FastAPI()


class Query(BaseModel):
    message: str


@app.post("/ask")
async def ask(query: Query):

    final_response, tool_called = process_query(query.message)

    return {
        "response": final_response,
        "tool_called": tool_called
    }


if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )