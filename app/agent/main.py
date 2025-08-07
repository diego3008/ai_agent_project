
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from app.schemas.question import Question
from .tools import build_graph, data_visualization_tool
from typing import Optional

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
                
        @self.router.post("/question-form")
        async def makeQuestionFromForm(
            question_text: str = Form(...),
            additional_context: Optional[str] = Form(None),
            file: Optional[UploadFile] = File(None)
        ) -> str:
            """Handle FormData from Next.js frontend with optional file upload"""
            try:
                # Combine question text with additional context if provided
                full_question = question_text
                if additional_context:
                    full_question = f"{question_text}\n\nAdditional Context: {additional_context}"
                
                # Process uploaded file if present
                if file and file.filename:
                    # Read file content
                    file_content = await file.read()
                    # Add file info to the question
                    full_question += f"\n\nFile uploaded: {file.filename} (Content type: {file.content_type})"
                    # You can process the file content here if needed
                    # For example, if it's a text file, you could include its content:
                    if file.content_type and 'text' in file.content_type:
                        full_question += f"\nFile content: {file_content.decode('utf-8')[:500]}..."  # First 500 chars
                
                agent = BasicAgent()
                answer = agent(question=full_question)
                return answer
            except Exception as ex:
                error_msg = f"Error processing form data: {str(ex)}"
                print(error_msg)
                raise HTTPException(status_code=500, detail=error_msg)