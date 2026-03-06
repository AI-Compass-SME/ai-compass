import csv
import json
import os
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres:aicompass-pass@db.vxlbohrtynivparbdahm.supabase.co:5432/postgres"
engine = create_engine(DATABASE_URL)

def extract_for_translation():
    with engine.connect() as conn:
        dims = conn.execute(text("SELECT dimension_id, dimension_name FROM dimensions")).fetchall()
        qs = conn.execute(text("SELECT question_id, header, question_text FROM questions")).fetchall()
        ans = conn.execute(text("SELECT answer_id, answer_text FROM answers")).fetchall()
        
    out = {
        "dimensions": {r.dimension_id: {"name": r.dimension_name, "de": ""} for r in dims},
        "questions": {r.question_id: {"header": r.header, "text": r.question_text, "header_de": "", "text_de": ""} for r in qs},
        "answers": {r.answer_id: {"text": r.answer_text, "de": ""} for r in ans}
    }
    with open("temp_trans.json", "w") as f:
        json.dump(out, f, indent=2)
    print("Exported to temp_trans.json")

if __name__ == "__main__":
    extract_for_translation()
