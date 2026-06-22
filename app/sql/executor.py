from sqlalchemy import text

from app.database.database import SessionLocal


def execute_sql(sql):

    db = SessionLocal()

    try:

        result = db.execute(
            text(sql)
        )

        rows = result.fetchall()

        columns = result.keys()

        output = []

        for row in rows:

            row_dict = {}

            for col, value in zip(columns, row):

                if hasattr(value, "isoformat"):

                    row_dict[col] = value.isoformat()

                else:

                    row_dict[col] = value

            output.append(row_dict)

        return output

    finally:

        db.close()