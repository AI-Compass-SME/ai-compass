from typing import Dict, List, Optional
from schemas.company import CompanyCreate
from schemas.response import ResponseCreate
from database import SessionLocal
from models.company import Company
from models.response import Response
from sqlalchemy import func
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class SessionStore:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionStore, cls).__new__(cls)
            cls._instance.companies: Dict[int, dict] = {}
            cls._instance.responses: Dict[int, dict] = {}
            cls._instance.response_values: Dict[int, List[dict]] = {} # response_id -> list of answers
            
            # Initialize counters from DB
            cls._instance._init_counters()
            
        return cls._instance

    def _init_counters(self):
        db = SessionLocal()
        try:
            # Get max IDs from DB to avoid collision
            max_c = db.query(func.max(Company.company_id)).scalar() or 0
            max_r = db.query(func.max(Response.response_id)).scalar() or 0
            
            self.company_counter = max_c
            self.response_counter = max_r
            logger.info(f"Initialized SessionStore counters - Company: {max_c}, Response: {max_r}")
        except Exception as e:
            logger.error(f"Error initializing session counters, defaulting to 1000: {e}")
            self.company_counter = 1000
            self.response_counter = 1000
        finally:
            db.close()

    def create_company(self, company: CompanyCreate) -> dict:
        self.company_counter += 1
        new_company = company.model_dump()
        new_company["company_id"] = self.company_counter
        self.companies[self.company_counter] = new_company
        return new_company

    def get_company(self, company_id: int) -> Optional[dict]:
        return self.companies.get(company_id)

    def update_company(self, company_id: int, company_data: CompanyCreate) -> Optional[dict]:
        if company_id in self.companies:
            updated_data = company_data.model_dump()
            updated_data["company_id"] = company_id
            self.companies[company_id] = updated_data
            return self.companies[company_id]
        return None

    def create_response(self, response: ResponseCreate) -> dict:
        self.response_counter += 1
        # Create a dict representation
        new_response = {
            "response_id": self.response_counter,
            "company_id": response.company_id,
            "total_score": None,
            "created_at": datetime.utcnow(), 
            "cluster_id": None
        }
        self.responses[self.response_counter] = new_response
        return new_response

    def get_response(self, response_id: int) -> Optional[dict]:
        return self.responses.get(response_id)
        
    def save_answer(self, response_id: int, question_id: int, answer_ids: List[int]):
        if response_id not in self.response_values:
            self.response_values[response_id] = []
        
        # Remove existing answer for this question
        self.response_values[response_id] = [
            x for x in self.response_values[response_id] 
            if x["question_id"] != question_id
        ]
        
        # Add new answer
        new_item = {
            "item_id": 0, # Dummy ID
            "response_id": response_id,
            "question_id": question_id,
            "answers": answer_ids
        }
        self.response_values[response_id].append(new_item)
        return new_item

    def get_response_items(self, response_id: int) -> List[dict]:
        return self.response_values.get(response_id, [])

    def get_full_session(self, response_id: int) -> Optional[dict]:
        response = self.get_response(response_id)
        if not response:
            return None
        
        company = self.get_company(response["company_id"])
        items = self.get_response_items(response_id)
        
        return {
            "company": company,
            "response": response,
            "items": items
        }

session_store = SessionStore()
