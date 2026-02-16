from database import SessionLocal, engine
from models.response import Response, ResponseItem
from models.company import Company
from services.scoring_service import get_score_breakdown, determine_cluster

def debug_503():
    db = SessionLocal()
    try:
        # Print DB Path
        from sqlalchemy import inspect
        print(f"Connecting to database: {engine.url}", flush=True)

        print("Listing last 5 responses in DB:", flush=True)
        last_responses = db.query(Response).order_by(Response.response_id.desc()).limit(5).all()
        for r in last_responses:
            print(f" - ID: {r.response_id}, CompanyID: {r.company_id}, Created: {r.created_at}", flush=True)
        
        print("Checking Response 503...", flush=True)
        response = db.query(Response).filter(Response.response_id == 503).first()
        
        if not response:
            print("Response 503 NOT FOUND in database.", flush=True)
            return

        print(f"Response Found: ID={response.response_id}, CompanyID={response.company_id}", flush=True)
        
        if response.company:
            print(f"Company: {response.company.company_name} (ID: {response.company.company_id})", flush=True)
        else:
            print("Company: NOT FOUND (Orphaned Response?)", flush=True)

        items = db.query(ResponseItem).filter(ResponseItem.response_id == 503).all()
        print(f"Response Items (Answers): {len(items)}", flush=True)
        
        if len(items) == 0:
            print("WARNING: No answers found for this response. Scoring might fail or return 0.", flush=True)

        print("Attempting to calculate score...", flush=True)
        try:
            items_data = [{"question_id": item.question_id, "answers": item.answers} for item in items]
            score_data = get_score_breakdown(items_data, db)
            print("Score Calculation: SUCCESS", flush=True)
            print(score_data, flush=True)
        except Exception as e:
            print(f"Score Calculation FAILED: {e}", flush=True)

    finally:
        db.close()

if __name__ == "__main__":
    debug_503()
