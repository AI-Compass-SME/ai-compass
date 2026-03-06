from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Question(Base):
    __tablename__ = "questions"

    question_id = Column(Integer, primary_key=True, index=True)
    dimension_id = Column(Integer, ForeignKey("dimensions.dimension_id"))
    header = Column(String)
    header_de = Column(String)
    question_text = Column(String)
    question_text_de = Column(String)
    type = Column(String)
    weight = Column(Float)
    optional = Column(Boolean)

    # Relationship
    dimension = relationship("Dimension")
    answers = relationship("Answer", back_populates="question")

    @property
    def dimension_name(self):
        return self.dimension.dimension_name if self.dimension else None

    @property
    def dimension_name_de(self):
        return self.dimension.dimension_name_de if self.dimension else None

class Answer(Base):
    __tablename__ = "answers"

    answer_id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.question_id"))
    answer_text = Column(String)
    answer_text_de = Column(String)
    answer_level = Column(Integer)
    answer_weight = Column(Float)

    # Relationship
    question = relationship("Question", back_populates="answers")
