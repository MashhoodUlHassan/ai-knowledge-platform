def validate_query(query: str) -> str:
    query = query.strip()

    if not query:
        raise ValueError("Query cannot be empty.")

    if len(query) > 2000:
        raise ValueError("Query is too long. Maximum length is 2000 characters.")

    return query