import requests

# Your repo details
OWNER = "aswinkumarpalani24"
REPO = "Learn"
PATH = "sql"   # folder inside repo
BRANCH = "main"

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


def get_sql_files():
    """
    Get list of SQL files from GitHub folder using API
    """
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{PATH}?ref={BRANCH}"
    response = requests.get(url)

    files = []
    if response.status_code == 200:
        data = response.json()
        for item in data:
            if item['name'].endswith('.sql'):
                files.append(item['download_url'])  # RAW URL
    else:
        print("Error fetching file list")

    return files


def read_sql_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return ""


if __name__ == "__main__":
    sql_files = get_sql_files()

    for file_url in sql_files:
        print(f"\n📄 Processing: {file_url}\n")

        content = read_sql_from_url(file_url)

        # Split queries (by semicolon OR blank line)
        queries = [q.strip() for q in content.split(';') if q.strip()]

        for i, query in enumerate(queries, start=1):
            complexity = classify_query(query)
            print(f"Query {i}: {complexity}")
        print("-" * 60)
