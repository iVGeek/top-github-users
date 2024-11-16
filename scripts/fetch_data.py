import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# GitHub GraphQL API endpoint
GRAPHQL_URL = "https://api.github.com/graphql"

# Headers with authorization token
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json",
}

# Query template for fetching users from a specific country
def fetch_github_users(country_code):
    query = f"""
    query {{
        search(query: "location:{country_code}", type: USER, first: 10) {{
            edges {{
                node {{
                    ... on User {{
                        login
                        name
                        followers {{
                            totalCount
                        }}
                        contributionsCollection {{
                            totalCommitContributions
                        }}
                    }}
                }}
            }}
        }}
    }}
    """

    # Send request to GitHub GraphQL API
    response = requests.post(GRAPHQL_URL, headers=headers, json={"query": query})
    data = response.json()

    users = []
    for user_data in data['data']['search']['edges']:
        user = user_data['node']
        users.append({
            'username': user['login'],
            'name': user.get('name', 'N/A'),
            'followers': user['followers']['totalCount'],
            'contributions': user['contributionsCollection']['totalCommitContributions'],
            'top_language': 'Python'  # Placeholder for the most used language
        })
    
    return users

# Fetch user data for multiple countries
countries = ['india', 'usa', 'germany', 'france']  # You can add more countries here
all_data = {}

for country in countries:
    all_data[country] = fetch_github_users(country)

# Save the data to a single JSON file
output_path = 'frontend/data/countries.json'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w') as f:
    json.dump(all_data, f, indent=4)

print("Data fetched and saved successfully.")
