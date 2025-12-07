import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "databases" / "database.db"
SCHEMA_MAIN = BASE_DIR / "instance" / "schema.sql"
SCHEMA_IOT = BASE_DIR / "instance" / "schema_iot.sql"

def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    try:
        # chạy schema chính
        conn.executescript(SCHEMA_MAIN.read_text(encoding="utf-8-sig"))
        # chạy schema IoT (nếu có)
        if SCHEMA_IOT.exists():
            conn.executescript(SCHEMA_IOT.read_text(encoding="utf-8-sig"))
        conn.commit()
        print(f"✅ Init DB OK: {DB_PATH}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
