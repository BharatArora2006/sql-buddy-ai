def build_prompt(question, documents):

    with open(
        "metadata/business_rules.txt",
        "r",
        encoding="utf-8"
    ) as f:

        business_rules = f.read()

    metadata = "\n\n".join(documents)

    prompt = f"""
You are a senior PostgreSQL developer specializing in pension administration systems.

Use ONLY the metadata provided below.

====================
BUSINESS RULES
====================

{business_rules}

====================
METADATA
====================

{metadata}

====================
RULES
====================

1. Return ONLY valid PostgreSQL SQL.
2. Do NOT use markdown.
3. Do NOT use ```sql blocks.
4. Output must start with SELECT.
4. Do not provide explanations.
5. Use table joins when required.
6. Join tables using employee_id.
7. Use business meanings from metadata.
8. Use exact column names from metadata.
9. Never invent tables or columns.

====================
QUESTION
====================

{question}

====================
SQL
====================
"""

    return prompt