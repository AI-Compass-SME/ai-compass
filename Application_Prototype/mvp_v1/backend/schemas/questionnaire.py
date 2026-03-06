from pydantic import BaseModel
from typing import List, Optional

class AnswerSchema(BaseModel):
    answer_id: int
    answer_text: str
    answer_text_de: Optional[str] = None
    answer_level: int
    answer_weight: float

    class Config:
        from_attributes = True

class QuestionSchema(BaseModel):
    question_id: int
    dimension_id: int
    dimension_name: Optional[str] = None
    dimension_name_de: Optional[str] = None
    header: Optional[str] = None
    header_de: Optional[str] = None
    question_text: str
    question_text_de: Optional[str] = None
    type: str
    weight: float
    optional: bool
    answers: List[AnswerSchema] = []

    class Config:
        from_attributes = True

class Questionnaire(BaseModel):
    questions: List[QuestionSchema]
