"""Day 5: parse nested JSON, write it back out, and load it into pandas."""
import json
import requests
import pandas as pd


def fetch_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    # Note: this returned an empty list on Day 5 because the repo was still
    # private at the time (this endpoint only lists PUBLIC repos for an
    # unauthenticated request) - that's why day6/day7 first used "octocat"
    # as a stand-in. Now that fde-roadmap is public, this works directly.
    raw = fetch_repos("mtls1976-ux")

    # 1. Pull 3 specific fields out of nested JSON.
    # "owner" is itself a nested dict inside each repo dict - that's the nesting.
    summary = []
    for repo in raw:
        summary.append({
            "name": repo["full_name"],
            "owner_login": repo["owner"]["login"],   # nested field
            "created_at": repo["created_at"],
        })

    print("Extracted fields:")
    for row in summary:
        print(f"  {row}")

    # 2. Write the extracted (smaller, cleaner) result back out as its own .json file.
    with open("day5_repos_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print("\nWrote day5_repos_summary.json")

    # 3. Convert the ORIGINAL nested JSON straight into a pandas DataFrame.
    # json_normalize flattens nested dicts into dotted column names, e.g. owner.login
    df = pd.json_normalize(raw)
    print(f"\nDataFrame shape: {df.shape}")
    print(df[["full_name", "owner.login", "created_at", "stargazers_count"]])
