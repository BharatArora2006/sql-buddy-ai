import re


def detect_hallucination(sql, metadata_docs):
    """
    Detects whether the generated SQL references
    tables or columns that are not present
    in the retrieved metadata.
    """

    sql = sql.lower()

    import re

    valid_tables = set()
    valid_columns = set()

    for doc in metadata_docs:

        text = doc.lower()

        # -------- TABLE NAME --------

        table_matches = re.findall(
            r'table(?:\s+name)?\s*:\s*([a-zA-Z_][a-zA-Z0-9_]*)',
            text
        )

        for table in table_matches:
            valid_tables.add(table)

        # -------- COLUMN NAMES --------

        column_matches = re.findall(
            r'([a-zA-Z_][a-zA-Z0-9_]*)\s*:',
            text
        )

        for col in column_matches:

            if col not in ["table", "name", "business", "description"]:

                valid_columns.add(col)

    hallucinated_objects = []

    # -------- TABLES USED --------

    tables_used = re.findall(
        r'from\s+([a-zA-Z_][a-zA-Z0-9_]*)',
        sql
    )

    tables_used += re.findall(
        r'join\s+([a-zA-Z_][a-zA-Z0-9_]*)',
        sql
    )

    for table in tables_used:

        if table not in valid_tables:

            hallucinated_objects.append(
                f"Table: {table}"
            )

    # -------- COLUMNS USED --------

    columns_used = re.findall(
        r'select\s+(.*?)\s+from',
        sql,
        re.IGNORECASE | re.DOTALL
    )

    if columns_used:

        cols = columns_used[0].split(",")

        for col in cols:

            col = col.strip()

            # Remove aliases
            col = re.sub(r'\s+as\s+\w+$', '', col, flags=re.IGNORECASE)

            # Extract identifier from SQL functions
            match = re.search(r'([a-zA-Z_][a-zA-Z0-9_]*)\)?$', col)

            if match:
                col = match.group(1)

            # Remove table alias
            if "." in col:
                col = col.split(".")[-1]

            if col == "*":
                continue

            if col.lower() not in valid_columns:

                hallucinated_objects.append(
                    f"Column: {col}"
                )

    hallucination_score = len(hallucinated_objects)
    print("VALID TABLES:", valid_tables)
    print("VALID COLUMNS:", valid_columns)
    print("TABLES USED:", tables_used)
    print("HALLUCINATED:", hallucinated_objects)

    return {
        "hallucination": hallucination_score > 0,
        "objects": hallucinated_objects,
        "score": hallucination_score
    }