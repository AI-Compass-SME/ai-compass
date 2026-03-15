import json
from sqlalchemy import create_engine, text
import sys

DATABASE_URL = "postgresql://postgres:aicompass-pass@db.vxlbohrtynivparbdahm.supabase.co:5432/postgres"

def run_migration(dry_run=True):
    engine = create_engine(DATABASE_URL)
    
    print("Loading extracted overrides...")
    with open("extracted_overrides.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    answers = data.get("answers", [])
    questions = data.get("questions", [])
    
    print(f"\n--- Processing {len(questions)} Question Updates ---")
    question_updates = []
    with engine.connect() as conn:
        for q in questions:
            q_id = q["question_id"]
            new_text = q["text"]
            
            # Fetch current to verify existence
            row = conn.execute(text("SELECT question_text_de FROM questions WHERE question_id = :id"), {"id": q_id}).fetchone()
            if row:
                old_text = row.question_text_de
                question_updates.append({
                    "id": q_id,
                    "old": old_text,
                    "new": new_text
                })
            else:
                print(f"Warning: Question ID {q_id} not found in DB!")
                
    print(f"\n--- Processing {len(answers)} Answer Updates ---")
    answer_updates = []
    with engine.connect() as conn:
        for a in answers:
            q_id = a["question_id"]
            a_level = a["answer_level"]
            new_text = a["text"]
            
            # Find exact answer_id where question_id = X AND answer_level = Y
            row = conn.execute(
                text("SELECT answer_id, answer_text_de FROM answers WHERE question_id = :qid AND answer_level = :lvl"),
                {"qid": q_id, "lvl": a_level}
            ).fetchone()
            
            if row:
                ans_id = row.answer_id
                old_text = row.answer_text_de
                answer_updates.append({
                    "id": ans_id,
                    "q_id": q_id,
                    "level": a_level,
                    "old": old_text,
                    "new": new_text
                })
            else:
                print(f"Warning: Answer not found for Q{q_id} Level{a_level}!")
                
    if dry_run:
        print("\n=== DRY RUN VERIFICATION ===")
        print(f"Found {len(question_updates)} valid questions to update.")
        print(f"Found {len(answer_updates)} valid answers to update.")
        
        # Save mapping for user review if requested, or just print a few
        with open("dry_run_mapping.txt", "w", encoding="utf-8") as f:
            f.write("=== QUESTIONS ===\n")
            for q in question_updates:
                f.write(f"ID {q['id']}:\n  Old: {q['old']}\n  New: {q['new']}\n")
            f.write("\n=== ANSWERS ===\n")
            for a in answer_updates:
                f.write(f"ID {a['id']} (Q{a['q_id']} L{a['level']}):\n  Old: {a['old']}\n  New: {a['new']}\n")
                
        print("Detailed mapping saved to 'dry_run_mapping.txt'.")
        print("Run with argument 'execute' to perform the actual update.")
        return
        
    print("\n=== EXECUTING DATABASE UPDATE ===")
    with engine.begin() as conn:
        print("Updating Questions...")
        for q in question_updates:
            conn.execute(
                text("UPDATE questions SET question_text_de = :text WHERE question_id = :id"),
                {"text": q["new"], "id": q["id"]}
            )
            
        print("Updating Answers...")
        for a in answer_updates:
            conn.execute(
                text("UPDATE answers SET answer_text_de = :text WHERE answer_id = :id"),
                {"text": a["new"], "id": a["id"]}
            )
            
    print("Database sync complete!")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "dry"
    run_migration(dry_run=(mode != "execute"))
