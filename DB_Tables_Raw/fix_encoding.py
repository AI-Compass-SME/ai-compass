
import sys
import os
import csv
from datetime import datetime

# Add backend to path so we can import database/models
# Adjust this path if necessary relative to DB_Tables_Raw
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Application_Prototype", "mvp_v1", "backend"))
sys.path.append(BACKEND_DIR)

from database import SessionLocal
from models.question import Answer

def fix_encoding():
    db = SessionLocal()
    try:
        answers = db.query(Answer).all()
        print(f"Loaded {len(answers)} answers.")
        
        # 1. CREATE BACKUP
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(os.path.dirname(__file__), f"answers_backup_{timestamp}.csv")
        
        print(f"Creating backup at: {backup_file}")
        with open(backup_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['answer_id', 'question_id', 'answer_text', 'answer_level', 'answer_weight'])
            for ans in answers:
                writer.writerow([ans.answer_id, ans.question_id, ans.answer_text, ans.answer_level, ans.answer_weight])
        print("Backup complete.")
        
        # 2. PERFORM MIGRATION
        print("Starting encoding fix...")
        fixed_count = 0
        
        for ans in answers:
            if not ans.answer_text:
                continue
                
            # Check for Replacement Character \uFFFD
            if '\ufffd' in ans.answer_text:
                original_text = ans.answer_text
                # Replace with " - " or just "-" depending on context, usually it's a separator
                # "Text  Text" -> "Text - Text"
                cleaned_text = original_text.replace('\ufffd', ' - ')
                
                # Cleanup double spaces if any created
                cleaned_text = cleaned_text.replace("  -  ", " - ")
                
                ans.answer_text = cleaned_text
                fixed_count += 1
                print(f"Fixed ID {ans.answer_id}:")
                print(f"  Old: {original_text}")
                print(f"  New: {cleaned_text}")
        
        if fixed_count > 0:
            db.commit()
            print(f"Successfully fixed {fixed_count} rows.")
        else:
            print("No issues found to fix.")
            
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_encoding()
