from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ResponseItemBase(BaseModel):
    question_id: int
    answer_ids: List[int]

class ResponseCreate(BaseModel):
    company_id: int

from schemas.company import CompanyCreate

class ResponseUpdate(BaseModel):
    question_id: int
    answer_ids: List[int]

class ResponseComplete(BaseModel):
    company_details: CompanyCreate

class ResponseDetail(BaseModel):
    response_id: int
    company_id: int
    total_score: Optional[str] = None
    created_at: datetime
    cluster_id: Optional[int] = None
    
    class Config:
        from_attributes = True

class ClusterInfo(BaseModel):
    cluster_id: int
    cluster_name: str
    cluster_description: Optional[str] = None
    characteristics: List[str] = []

class DimensionScore(BaseModel):
    dimension_id: int
    dimension_name: str
    score: float
    max_score: float = 5.0
    
class ResponseResult(BaseModel):
    response_id: int
    company: CompanyCreate # Reusing CompanyCreate base for simplicity, contains industry etc.
    overall_score: float
    dimension_scores: List[DimensionScore]
    cluster: Optional[ClusterInfo] = None
    percentile: Optional[dict] = None
    roadmap: Optional[List[dict]] = None
    
    class Config:
        from_attributes = True
