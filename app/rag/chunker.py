def chunk_table_metadata(data):

    chunks = []

    table_name = data.get("table_name")

    business_name = data.get("business_name")

    description = data.get("description")

    chunks.append(
        f"""
        Table Name: {table_name}

        Business Name: {business_name}

        Description: {description}
        """
    )

    if "columns" in data:

        column_text = "\n".join(
            [
                f"{k}: {v}"
                for k, v in data["columns"].items()
            ]
        )

        chunks.append(
            f"""
            Table {table_name} Columns

            {column_text}
            """
        )

    if "code_mappings" in data:

        for code, meaning in data["code_mappings"].items():

            chunks.append(
                f"""
    Table: {table_name}

    Business Meaning:

    {meaning} employee means
    emp_status_code = '{code}'
    """
            )

    if "status_codes" in data:

        for code, meaning in data["status_codes"].items():

            chunks.append(
                f"""
    Table: {table_name}

    Business Meaning:

    {meaning} payment means
    payment_status = '{code}'
    """
            )

    return chunks