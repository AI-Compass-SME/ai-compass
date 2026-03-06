import uuid
from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, BigInteger, ForeignKey, ARRAY, Boolean
from sqlalchemy.orm import relationship
from database import Base

class ClusterProfile(Base):
    __tablename__ = "cluster_profiles"

    cluster_id = Column(BigInteger, primary_key=True, index=True)
    cluster_name = Column(String)
    score_min = Column(Float)
    score_max = Column(Float)

class Response(Base):
    __tablename__ = "responses"

    response_id = Column(Integer, primary_key=True, index=True)
    result_hash = Column(String(36), unique=True, index=True, default=lambda: str(uuid.uuid4()))
    is_verified = Column(Boolean, default=False)
    company_id = Column(Integer, ForeignKey("companies.company_id"))
    total_score = Column(String)
    created_at = Column(TIMESTAMP(timezone=True))
    cluster_id = Column(BigInteger, ForeignKey("cluster_profiles.cluster_id"))
    lang = Column(String, default='en')

    # Relationships
    company = relationship("Company")
    cluster = relationship("ClusterProfile")
    items = relationship("ResponseItem", back_populates="response")

class ResponseItem(Base):
    __tablename__ = "response_items"

    item_id = Column(Integer, primary_key=True, index=True)
    response_id = Column(Integer, ForeignKey("responses.response_id"))
    question_id = Column(Integer, ForeignKey("questions.question_id"))
    answers = Column(ARRAY(Integer)) # PostgreSQL specific array type

    # Relationships
    response = relationship("Response", back_populates="items")
    question = relationship("Question")
