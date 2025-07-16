from fastapi import FastAPI
from app.agent.main import AgentRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
agent_router = AgentRouter()
app.include_router(agent_router.router, prefix="/api/agent", tags=["Agent"])