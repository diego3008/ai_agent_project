
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.schemas.question import Question
from .tools import build_graph, data_visualization_tool

# --- Basic Agent Definition ---
# ----- THIS IS WERE YOU CAN BUILD WHAT YOU WANT ------

class BasicAgent:
    """Langgraph Agent"""

    def __init__(self):
        print("BasicAgent initialized.")
        try:
            self.graph = build_graph(provider="groq")
        except Exception as ex:
            print(f"Error building graph: {ex}")
            self.graph = None

    def __call__(self, question: str) -> str:
        try:
            if self.graph is None:
                raise ValueError("Agent not initialized properly.")

            messages = [HumanMessage(content=question)]
            result = self.graph.invoke({"messages": messages})
            if result and 'messages' in result and result["messages"]:
                answer = result['messages'][-1].content
            # Limpiar la respuesta si tiene prefijos no deseados
                if answer.startswith("Assistant: "):
                    answer = answer[11:]  # Remover "Assistant: "
                elif len(answer) > 14 and answer[:14].lower().startswith(("the result is", "the answer is")):
                    answer = answer[14:]  # Remover prefijos explicativos

                print(f"Agent returning answer: {answer[:100]}...")
                return answer.strip()
            else:
                print("Error: No response generated")
        except Exception as ex:
            error_msg = f"Error in agent execution: {str(ex)}"
            print(error_msg)
            return error_msg


class AgentRouter:

    def __init__(self):
        self.router = APIRouter()
        self.addRoutes()

    def addRoutes(self):
        
        @self.router.post("/question")
        async def makeQuestion(question: Question) -> str:
            try:
                agent = BasicAgent()
            except HTTPException as ex:
                print(f"There was an error: #{ex}")
            
            try:
                answer = agent(question=question.question_text)
                return answer
            except HTTPException as ex:
                print(f"There was an error retrieving the question: #{ex}")
                return ex