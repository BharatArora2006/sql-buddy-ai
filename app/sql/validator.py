FORBIDDEN_KEYWORDS = [
    "DROP",
    "DELETE",
    "TRUNCATE",
    "ALTER",
    "UPDATE",
    "INSERT",
    "CREATE",
    "GRANT",
    "REVOKE"
]


def validate_sql(sql: str):

    sql_upper = sql.upper()

    for keyword in FORBIDDEN_KEYWORDS:

        if keyword in sql_upper:

            raise ValueError(
                f"Forbidden SQL detected: {keyword}"
            )

    return True