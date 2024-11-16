import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

# GraphQL query to fetch user data
QUERY = """
query ($location: String!) {
  search(query: $location, type: USER, first: 50) {
    edges {
      node {
        ... on User {
          login
          name
          followers {
            totalCount
          }
          contributionsCollection {
            totalCommitContributions
          }
          repositories(first: 5, orderBy: {field: STARGAZERS, direction: DESC}) {
            nodes {
              primaryLanguage {
                name
              }
            }
          }
        }
      }
    }
  }
}
"""

def fetch_users(location):
    """Fetch GitHub user data for a specific location."""
    variables = {"location": location}
    response = requests.post(
        GITHUB_GRAPHQL_URL,
        json={"query": QUERY, "variables": variables},
        headers=HEADERS
    )
    if response.status_code != 200:
        raise Exception(f"Query failed: {response.status_code} {response.text}")
    
    data = response.json()["data"]["search"]["edges"]
    users = []
    for edge in data:
        user = edge["node"]
        if user["followers"]["totalCount"] >= 20:
            languages = [
                repo["primaryLanguage"]["name"]
                for repo in user["repositories"]["nodes"]
                if repo["primaryLanguage"]
            ]
            top_language = max(set(languages), key=languages.count) if languages else None
            users.append({
                "username": user["login"],
                "name": user.get("name", ""),
                "followers": user["followers"]["totalCount"],
                "contributions": user["contributionsCollection"]["totalCommitContributions"],
                "top_language": top_language,
            })
    return users

def save_data(location, data):
    """Save fetched data to a JSON file."""
    filename = f"../data/{location.replace(' ', '_').lower()}.json"
    os.makedirs("../data", exist_ok=True)
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    locations = ["India", "United States", "Germany"]  # Example countries
    for location in locations:
        users = fetch_users(location)
        save_data(location, users)
