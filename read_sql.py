import requests

LOW_KEYWORDS = ['select', 'rename', 'as']
MEDIUM_KEYWORDS = ['group by', 'count', 'sum', 'case', 'substring', 'length', 'union', 'concat', 'replace']
HIGH_KEYWORDS = ['over', 'row_number', 'rank', 'dense_rank', 'lead', 'lag', 'ntile']


def classify_query(query: str) -> str:
    query_lower = query.lower()

    if any(k in query_lower for k in HIGH_KEYWORDS):
        return 'High'
    if any(k in query_lower for k in MEDIUM_KEYWORDS):
        return 'Medium'
    return 'Low'


def read_sql_from_github(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print("Error fetching file")
        return ""


if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/aswinkumarpalani24/Learn/main/test.sql"

    sql_content = read_sql_from_github(url)

    if sql_content:
        queries = [q.strip() for q in sql_content.split('\n\n') if q.strip()]

        for i, query in enumerate(queries, start=1):
            complexity = classify_query(query)
            print(f"Query {i}: {complexity}\n{query}\n{'-'*50}")
