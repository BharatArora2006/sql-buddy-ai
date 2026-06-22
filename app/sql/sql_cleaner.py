import re


def clean_sql(sql_text):

    sql_text = re.sub(
        r"```sql",
        "",
        sql_text,
        flags=re.IGNORECASE
    )

    sql_text = re.sub(
        r"```",
        "",
        sql_text
    )

    return sql_text.strip()