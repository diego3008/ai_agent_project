from fastapi import FastAPI
from app.agent.main import AgentRouter

app = FastAPI()

agent_router = AgentRouter()
app.include_router(agent_router.router, prefix="/api/agent", tags=["Agent"])