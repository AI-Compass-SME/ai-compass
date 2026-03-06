import os
import datetime
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:aicompass-pass@db.vxlbohrtynivparbdahm.supabase.co:5432/postgres"

engine = create_engine(DATABASE_URL)
metadata = MetaData()
metadata.reflect(bind=engine)

def value_to_sql(value, col_type):
    if value is None:
        return 'NULL'
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, bool):
        return 'TRUE' if value else 'FALSE'
    if isinstance(value, datetime.datetime):
        return f"'{value.strftime('%Y-%m-%d %H:%M:%S%z')}'"
    if isinstance(value, str):
        # Escape single quotes
        escaped = value.replace("'", "''")
        return f"'{escaped}'"
    if isinstance(value, list):
        # Array type
        items = ",".join(str(v) for v in value)
        return f"ARRAY[{items}]"
    return f"'{str(value)}'"

def generate_dump():
    dump_file = "postgres_backup.sql"
    with open(dump_file, "w", encoding="utf-8") as f:
        f.write("-- AI Compass DB Backup\n")
        f.write(f"-- Generated on {datetime.datetime.now()}\n\n")

        # Iterate over all tables in a safe order (tables without FKs first)
        for table_name in metadata.tables:
            table = metadata.tables[table_name]
            f.write(f"-- Data for table: {table_name}\n")
            
            with engine.connect() as conn:
                try:
                    result = conn.execute(table.select())
                    rows = result.fetchall()
                    if not rows:
                        continue
                    
                    columns = [col.name for col in table.columns]
                    col_types = [col.type for col in table.columns]
                    
                    col_names_str = ", ".join(f'"{col}"' for col in columns)
                    
                    for row in rows:
                        vals = []
                        for val, c_type in zip(row, col_types):
                            vals.append(value_to_sql(val, c_type))
                        
                        vals_str = ", ".join(vals)
                        insert_stmt = f'INSERT INTO "{table_name}" ({col_names_str}) VALUES ({vals_str});\n'
                        f.write(insert_stmt)
                except Exception as e:
                    print(f"Error dumping table {table_name}: {e}")
                    f.write(f"-- Error dumping table {table_name}: {e}\n")
            f.write("\n")
    print(f"Database successfully backed up to {os.path.abspath(dump_file)}")

if __name__ == "__main__":
    generate_dump()
