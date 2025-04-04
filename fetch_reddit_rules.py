import os
import json
import requests
import praw
from dotenv import load_dotenv

load_dotenv()  # Loads environment variables from .env

def fetch_public_rules(subreddit_name):
    """
    Fetch a subreddit's rules via the public endpoint:
    https://www.reddit.com/r/<subreddit>/about/rules.json

    Returns a list of rule dicts if successful,
    or a string (error message) if something goes wrong.
    """
    url = f"https://www.reddit.com/r/{subreddit_name}/about/rules.json"
    user_agent = os.getenv("REDDIT_USER_AGENT", "DefaultScraper/1.0")

    headers = {"User-Agent": user_agent}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return f"HTTP {response.status_code} - Could not retrieve rules for r/{subreddit_name}"

        data = response.json()
        if "rules" not in data:
            return f"No 'rules' key found in response for r/{subreddit_name}"

        return data["rules"]
    except Exception as e:
        return str(e)

def main():
    # Initialize PRAW with credentials from .env
    reddit = praw.Reddit(
        client_id = os.environ.get("CLIENT_ID"),
        client_secret = os.environ.get("CLIENT_SECRET"),
        user_agent = os.environ.get("USER_AGENT")
    )

    explored_file = "explored_subreddits.txt"
    if os.path.exists(explored_file):
        with open(explored_file, "r", encoding="utf-8") as f:
            explored_subs = set(line.strip() for line in f if line.strip())
    else:
        explored_subs = set()

    os.makedirs("Rules", exist_ok=True)

    count = 0
    for subreddit in reddit.subreddits.popular(limit=None):
        if subreddit.over18:
            continue  # Skip NSFW
        if subreddit.subscribers < 100_000:
            continue  # Skip if under 100k subscribers

        sub_name = subreddit.display_name
        if sub_name in explored_subs:
            continue  # Already explored

        result = fetch_public_rules(sub_name)
        if isinstance(result, str):
            # It's an error message – just print and skip
            print(f"Error: r/{sub_name} -> {result}")
            continue
        else:
            # We have a list of rule objects
            print(f"Fetched {len(result)} rule(s) from r/{sub_name}")
            minimal_rules = []
            for rule in result:
                minimal_rules.append({
                    "Rule_title": rule.get("short_name", ""),
                    "description": rule.get("description", ""),
                    "kind": rule.get("kind", "")
                })

            to_save = {
                "subreddit": sub_name,
                "subscribers": subreddit.subscribers,
                "rules": minimal_rules
            }

            out_path = os.path.join("Rules", f"{sub_name}.json")
            with open(out_path, "w", encoding="utf-8") as outfile:
                json.dump(to_save, outfile, indent=4, ensure_ascii=False)

            # saved rules only if there is no error 
            explored_subs.add(sub_name)
            with open(explored_file, "a", encoding="utf-8") as f:
                f.write(sub_name + "\n")

        count += 1
        if count >= 10:
            # Stop after 10 subreddits to avoid banning 
            break

    print("\nDone! Check the 'Rules' folder for JSON files.")

if __name__ == "__main__":
    main()
