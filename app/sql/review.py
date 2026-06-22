def review_sql(sql: str):

    review = []

    sql_upper = sql.upper()

    if "SELECT" in sql_upper:
        review.append("✓ Valid SELECT Query")

    if "JOIN" in sql_upper:
        review.append("✓ Join Detected")

    if "WHERE" in sql_upper:
        review.append("✓ Filter Applied")

    if any(
        keyword in sql_upper
        for keyword in [
            "DELETE",
            "UPDATE",
            "DROP",
            "TRUNCATE"
        ]
    ):
        review.append("⚠ Dangerous Statement Found")
    else:
        review.append("✓ Read Only Query")

    return review