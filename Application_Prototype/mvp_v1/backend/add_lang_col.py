import sqlite3

def add_lang_column():
    conn = sqlite3.connect('sql_app.db')
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE responses ADD COLUMN lang VARCHAR DEFAULT 'en';")
        conn.commit()
        print("Successfully added 'lang' column to 'responses' table.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("Column 'lang' already exists.")
        else:
            print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    add_lang_column()
