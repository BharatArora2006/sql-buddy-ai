import re

from app.database.schema_cache import SCHEMA


def validate_schema(sql: str):

    """
    Validates whether all tables and columns
    used in SQL exist in PostgreSQL schema.
    """

    sql = sql.lower()

    hallucinated = []

    # -----------------------------
    # TABLES
    # -----------------------------

    tables = []

    tables += re.findall(
        r'from\s+([a-zA-Z_][a-zA-Z0-9_]*)',
        sql
    )

    tables += re.findall(
        r'join\s+([a-zA-Z_][a-zA-Z0-9_]*)',
        sql
    )

    valid_columns = set()

    for table in tables:

        if table not in SCHEMA:

            hallucinated.append(
                f"Table: {table}"
            )

        else:

            valid_columns.update(
                SCHEMA[table]
            )

    # -----------------------------
    # COLUMNS
    # -----------------------------

    select_match = re.search(
        r"select(.*?)from",
        sql,
        re.IGNORECASE | re.DOTALL
    )

    if select_match:

        select_part = select_match.group(1)

        expressions = select_part.split(",")

        for expr in expressions:

            expr = expr.strip()

            if expr == "*":
                continue

            # remove alias
            expr = re.sub(
                r"\s+as\s+\w+$",
                "",
                expr,
                flags=re.IGNORECASE
            )

            # remove table alias
            if "." in expr:
                expr = expr.split(".")[-1]

            # SQL functions
            identifiers = re.findall(
                r"[a-zA-Z_][a-zA-Z0-9_]*",
                expr
            )

            keywords = {
                "count",
                "sum",
                "avg",
                "min",
                "max",
                "distinct",

                "case",
                "when",
                "then",
                "else",
                "end",

                "current_date",

                "null",
                "is",
                "and",
                "or",
                "not",

                "as",

                "true",
                "false"
            }

            for word in identifiers:
                # print(f"WORD = [{word}]")
                if word.lower() in keywords:
                    continue
                
                # Ignore single-letter literals like A, T, Y, N
                if len(word) == 1:
                    continue

                if word not in valid_columns:

                    hallucinated.append(
                        f"Column: {word}"
                    )

    return {

        "hallucination": len(hallucinated) > 0,

        "objects": hallucinated,

        "score": len(hallucinated)
    }