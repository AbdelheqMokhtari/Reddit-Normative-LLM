import praw
import os
from dotenv import load_dotenv
# this script just to test the access to reddit 
# Create your reddit app from here : https://www.reddit.com/prefs/apps

def main():

    load_dotenv() # to load variables from .env
    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")
    user_agent = os.environ.get("USER_AGENT")
    
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

    # Choose a subreddit to test (e.g., "python")
    test_subreddit = reddit.subreddit("python")

    # Fetch 5 hot posts and print their titles
    try:
        print("Fetching top 5 hot posts in r/python:\n")
        for submission in test_subreddit.hot(limit=5):
            print("- ", submission.title)
        print("\nSuccess! Your API credentials work.")
    except Exception as e:
        print(f"Something went wrong: {e}")

if __name__ == "__main__":
    main()