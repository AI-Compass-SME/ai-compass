from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from database import get_db
from models import Question, Answer
from schemas import questionnaire as schemas

router = APIRouter()

@router.get("/", response_model=schemas.Questionnaire)
def get_questionnaire(db: Session = Depends(get_db)):
    """
    Fetch the full questionnaire with all questions, answers, and dimensions.
    """
    # Use joinedload to ensure the `dimension` relation is loaded,
    # so the @property access for dimension_name_de works during Pydantic serialization.
    questions = db.query(Question)\
                  .options(joinedload(Question.dimension), joinedload(Question.answers))\
                  .order_by(Question.question_id)\
                  .all()
    
    return {"questions": questions}
