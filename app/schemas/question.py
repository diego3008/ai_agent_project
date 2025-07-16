from pydantic import BaseModel

class Question(BaseModel):
    question_text: str

