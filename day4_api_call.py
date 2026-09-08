"""Day 4: talk to a real API with requests, and don't crash when it fails."""
import requests


def get_github_user(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    # Happy path: a username that actually exists.
    try:
        data = get_github_user("mtls1976-ux")
        print(f"Found user: {data['login']}")
        print(f"  Joined:     {data['created_at']}")
        print(f"  Public repos: {data['public_repos']}")
        print(f"  Profile URL: {data['html_url']}")
    except requests.exceptions.RequestException as e:
        print(f"Could not fetch profile: {e}")

    print()

    # Unhappy path: a username that doesn't exist, so the API returns a 404.
    try:
        data = get_github_user("this-user-almost-certainly-does-not-exist-12345")
        print(f"Found user: {data['login']}")
    except requests.exceptions.HTTPError as e:
        print(f"Handled gracefully -> GitHub says: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Handled gracefully -> network problem: {e}")
