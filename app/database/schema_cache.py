from sqlalchemy import text

from app.database.database import SessionLocal


def load_schema():

    db = SessionLocal()

    schema = {}

    # Get every table and column
    rows = db.execute(
        text("""
            SELECT
                table_name,
                column_name
            FROM information_schema.columns
            WHERE table_schema='public'
            ORDER BY table_name
        """)
    ).fetchall()

    db.close()

    for table_name, column_name in rows:

        if table_name not in schema:

            schema[table_name] = set()

        schema[table_name].add(column_name)

    return schema


# Load once when application starts
SCHEMA = load_schema()