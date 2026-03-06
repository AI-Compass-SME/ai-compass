import uuid
from sqlalchemy import text
from database import engine

def migrate():
    try:
        with engine.begin() as conn:
            # 1. Add Column
            print("Adding result_hash column if not exists...")
            conn.execute(text("ALTER TABLE responses ADD COLUMN IF NOT EXISTS result_hash VARCHAR(36);"))
            
            # 2. Backfill existing without a hash
            print("Backfilling existing rows with secure UUIDs...")
            res = conn.execute(text("SELECT response_id FROM responses WHERE result_hash IS NULL"))
            rows_updated = 0
            for row in res.mappings():
                conn.execute(text("UPDATE responses SET result_hash = :hash WHERE response_id = :id"), {"hash": str(uuid.uuid4()), "id": row["response_id"]})
                rows_updated += 1
            print(f"Backfilled {rows_updated} rows.")
            
            # 3. Add constraint (ignore if it already exists)
            try:
                print("Adding UNIQUE constraint...")
                conn.execute(text("ALTER TABLE responses ADD CONSTRAINT uq_result_hash UNIQUE (result_hash);"))
            except Exception as e:
                print(f"Constraint might already exist: {e}")
                
        print("Migration complete successfully.")
    except Exception as e:
        print(f"Migration error: {e}")

if __name__ == "__main__":
    migrate()
