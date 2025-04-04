import requests
import json
import os
from dotenv import load_dotenv

load_dotenv() # to load variables from .env
def fetch_public_rules(subreddit):
    """
    Query the public endpoint for a subreddit's rules:
    https://www.reddit.com/r/<subreddit>/about/rules.json
    
    Returns either:
    - A list of rule dictionaries if successful
    - A string containing an error message if something goes wrong
    """
    url = f"https://www.reddit.com/r/{subreddit}/about/rules.json"
    # Always provide a descriptive User-Agent
    user_agent = os.getenv("REDDIT_USER_AGENT", "DefaultScraper/1.0")

    # Build headers using the environment variable
    headers = {
        "User-Agent": user_agent
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return f"HTTP {response.status_code} - Could not retrieve rules"
        
        data = response.json()
        if "rules" not in data:
            return "No 'rules' key found in response"
        
        # data["rules"] should be a list of rule objects
        return data["rules"]
    except Exception as e:
        return str(e)


def main():
    # List the subreddits you want to process
    subreddits = ["datascience", "MachineLearning", "Python"]

    # Create 'Rules' folder if not existing
    os.makedirs("Rules", exist_ok=True)

    for sub in subreddits:
        result = fetch_public_rules(sub)

        if isinstance(result, str):
            # If 'result' is a string, it's an error message
            print(f"Error fetching rules from r/{sub}: {result}")
            to_save = {"error": result}
        else:
            # result is a list of rule objects
            print(f"Fetched {len(result)} rule(s) from r/{sub}")
            
            # Keep only short_name, description, and kind
            minimal_rules = []
            for rule in result:
                minimal_rules.append({
                    "Rule_title": rule.get("short_name", ""),
                    "description": rule.get("description", ""),
                    "kind": rule.get("kind", "")
                })
            
            to_save = {
                "subreddit": sub,
                "rules": minimal_rules
            }

        # Write the data to "Rules/<subreddit>.json"
        file_path = os.path.join("Rules", f"{sub}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(to_save, f, indent=4, ensure_ascii=False)

    print("\nDone! Each subreddit's rules are saved in the 'Rules' folder.")

if __name__ == "__main__":
    main()
