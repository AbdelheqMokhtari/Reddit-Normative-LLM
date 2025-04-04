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

    Returns:
      - A list of rule dicts if successful
      - A string (error message) if something goes wrong
    """
    url = f"https://www.reddit.com/r/{subreddit_name}/about/rules.json"
    user_agent = os.getenv("REDDIT_USER_AGENT", "ManualRulesFetcher/1.0")

    headers = {"User-Agent": user_agent}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return f"HTTP {response.status_code} - Could not retrieve rules for r/{subreddit_name}"

        data = response.json()
        if "rules" not in data:
            return f"No 'rules' key found in the response for r/{subreddit_name}"

        return data["rules"]  # List of rule objects
    except Exception as e:
        return str(e)

def main():
    # Initialize PRAW if you want to retrieve subscribers count
    reddit = praw.Reddit(
        client_id = os.environ.get("CLIENT_ID"),
        client_secret = os.environ.get("CLIENT_SECRET"),
        user_agent = os.environ.get("USER_AGENT")
    )

    subreddits = ["datascience", "MachineLearning", "Python"]

    # 2. Read or create the file that tracks already-explored subreddits
    explored_file = "explored_subreddits.txt"
    if os.path.exists(explored_file):
        with open(explored_file, "r", encoding="utf-8") as f:
            explored_subs = set(line.strip() for line in f if line.strip())
    else:
        explored_subs = set()

    # 3. Create 'Rules' folder if not existing
    os.makedirs("Rules", exist_ok=True)

    for sub_name in subreddits:
        # 4. Check if it's already explored
        if sub_name in explored_subs:
            print(f"Already explored r/{sub_name}, skipping.")
            continue

        # 5. Get the subreddit object via PRAW to retrieve subscriber count
        try:
            subreddit_obj = reddit.subreddit(sub_name)
            subscribers_count = subreddit_obj.subscribers
        except Exception as e:
            # If PRAW fails (e.g., invalid subreddit name), skip
            print(f"Error accessing r/{sub_name} via PRAW: {e}")
            continue

        # 6. Fetch the rules from the public endpoint
        result = fetch_public_rules(sub_name)
        if isinstance(result, str):
            # 'result' is an error message, just print and skip
            print(f"Error fetching r/{sub_name}: {result}")
            continue

        # 7. We have a list of rule objects
        print(f"Fetched {len(result)} rule(s) from r/{sub_name}")

        # Keep only short_name, description, and kind
        minimal_rules = []
        for rule in result:
            minimal_rules.append({
                "Rule_title": rule.get("short_name", ""),
                "description": rule.get("description", ""),
                "kind": rule.get("kind", "")
            })

        # 8. Create the final object to save
        to_save = {
            "subreddit": sub_name,
            "subscribers": subscribers_count,
            "rules": minimal_rules
        }

        # 9. Write the data to "Rules/<subreddit>.json"
        file_path = os.path.join("Rules", f"{sub_name}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(to_save, f, indent=4, ensure_ascii=False)

        # 10. Mark this subreddit as explored only after success
        explored_subs.add(sub_name)
        with open(explored_file, "a", encoding="utf-8") as ef:
            ef.write(sub_name + "\n")

    print("\nDone! Check the 'Rules' folder for JSON files.")

if __name__ == "__main__":
    main()