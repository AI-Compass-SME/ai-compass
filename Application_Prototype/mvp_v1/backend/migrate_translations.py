import json
import time
from deep_translator import GoogleTranslator
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres:aicompass-pass@db.vxlbohrtynivparbdahm.supabase.co:5432/postgres"

def main():
    print("Loading extracted texts...")
    with open("temp_trans.json", "r") as f:
        data = json.load(f)

    translator = GoogleTranslator(source='en', target='de')

    def translate_text(text):
        if not text or not text.strip():
            return ""
        try:
            return translator.translate(text)
        except Exception as e:
            print(f"Error translating '{text}': {e}")
            return text

    print("Translating Dimensions...")
    for dim_id, dim in data["dimensions"].items():
        if not dim.get("de"):
            dim["de"] = translate_text(dim["name"])
            time.sleep(0.1)

    print("Translating Questions (Headers and Text)...")
    for q_id, q in data["questions"].items():
        if not q.get("header_de") and q.get("header"):
            q["header_de"] = translate_text(q["header"])
            time.sleep(0.1)
        if not q.get("text_de") and q.get("text"):
            q["text_de"] = translate_text(q["text"])
            time.sleep(0.1)

    print("Translating Answers...")
    for ans_id, ans in data["answers"].items():
        if not ans.get("de") and ans.get("text"):
            ans["de"] = translate_text(ans["text"])
            time.sleep(0.1)

    with open("temp_trans_done.json", "w") as f:
        json.dump(data, f, indent=2)

    print("Executing Database Migration...")
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        with conn.begin():
            # Add Columns
            print("Adding _de columns to tables...")
            conn.execute(text("ALTER TABLE dimensions ADD COLUMN IF NOT EXISTS dimension_name_de VARCHAR;"))
            conn.execute(text("ALTER TABLE questions ADD COLUMN IF NOT EXISTS header_de VARCHAR;"))
            conn.execute(text("ALTER TABLE questions ADD COLUMN IF NOT EXISTS question_text_de VARCHAR;"))
            conn.execute(text("ALTER TABLE answers ADD COLUMN IF NOT EXISTS answer_text_de VARCHAR;"))
            
            # Update Dimensions
            print("Updating Dimensions...")
            for dim_id, dim in data["dimensions"].items():
                conn.execute(
                    text("UPDATE dimensions SET dimension_name_de = :val WHERE dimension_id = :id"),
                    {"val": dim["de"], "id": int(dim_id)}
                )

            # Update Questions
            print("Updating Questions...")
            for q_id, q in data["questions"].items():
                conn.execute(
                    text("UPDATE questions SET header_de = :hd_val, question_text_de = :tx_val WHERE question_id = :id"),
                    {"hd_val": q["header_de"], "tx_val": q["text_de"], "id": int(q_id)}
                )

            # Update Answers
            print("Updating Answers...")
            for ans_id, ans in data["answers"].items():
                conn.execute(
                    text("UPDATE answers SET answer_text_de = :val WHERE answer_id = :id"),
                    {"val": ans["de"], "id": int(ans_id)}
                )

    print("Migration completed successfully!")

if __name__ == "__main__":
    main()
