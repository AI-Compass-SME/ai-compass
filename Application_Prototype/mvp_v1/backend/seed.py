import csv
import os
from database import SessionLocal, engine, Base
import models # ensure models are loaded
from models.dimension import Dimension
from models.question import Question, Answer
from models.response import ClusterProfile
from models.company import Company
from sqlalchemy import text # correct import

def seed_data():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Paths to CSV files
    # seed.py is in backend/
    # DB_Tables_Raw is in ../../../DB_Tables_Raw/ relative to backend/
    base_path = os.path.dirname(os.path.abspath(__file__))
    raw_data_path = os.path.abspath(os.path.join(base_path, "../../../DB_Tables_Raw"))
    
    print(f"Reading data from: {raw_data_path}")

    try:
        # Clear existing data to avoid duplicates or partial updates
        print("Clearing existing data...")
        db.execute(text("DELETE FROM answers"))
        db.execute(text("DELETE FROM questions"))
        db.execute(text("DELETE FROM dimensions"))
        db.execute(text("DELETE FROM cluster_profiles"))
        db.commit()

        # 1. Dimensions
        print("Seeding Dimensions...")
        with open(os.path.join(raw_data_path, "dimensions.csv"), 'r', encoding='latin-1') as f:
            reader = csv.DictReader(f)
            for row in reader:
                dim = Dimension(
                    dimension_id=int(row['dimension_id']),
                    dimension_name=row['dimension_name'],
                    dimension_weight=float(row['dimension_weight'] or 0)
                )
                db.add(dim)
        db.commit()

        # 2. Questions
        print("Seeding Questions...")
        with open(os.path.join(raw_data_path, "questions.csv"), 'r', encoding='latin-1') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Assuming CSV columns based on partial view and standard naming
                # Adjust column names if they differ in the actual file
                # question_id,dimension_id,header,question_text,type,weight,optional
                q = Question(
                    question_id=int(row['question_id']),
                    dimension_id=int(row['dimension_id']),
                    header=row.get('header', ''),
                    question_text=row['question_text'],
                    type=row.get('type', 'Scale'),
                    weight=float(row.get('weight', 1.0) or 1.0),
                    optional=str(row.get('optional', 'FALSE')).upper() == 'TRUE'
                )
                db.add(q)
        db.commit()

        # 3. Answers
        print("Seeding Answers...")
        with open(os.path.join(raw_data_path, "answers.csv"), 'r', encoding='latin-1') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # answer_id,question_id,answer_text,answer_level,answer_weight
                ans = Answer(
                    answer_id=int(row['answer_id']),
                    question_id=int(row['question_id']),
                    answer_text=row['answer_text'],
                    answer_level=int(row.get('answer_level', 0) or 0),
                    answer_weight=float(row.get('answer_weight', 0.0) or 0.0)
                )
                db.add(ans)
        db.commit()

        # 4. Clusters
        print("Seeding Clusters...")
        with open(os.path.join(raw_data_path, "cluster_profiles.csv"), 'r', encoding='latin-1') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # cluster_id,cluster_name,score_min,score_max
                cluster = ClusterProfile(
                    cluster_id=int(row['cluster_id']),
                    cluster_name=row['cluster_name'],
                    score_min=float(row['score_min']),
                    score_max=float(row['score_max'])
                )
                db.add(cluster)
        db.commit()

        print("Seeding complete!")

    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
