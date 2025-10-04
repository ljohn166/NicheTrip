import praw
from dotenv import load_dotenv
import os

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

# Initialize PRAW with your Reddit instance
# (client_id, client_secret, user_agent, etc.)
reddit = praw.Reddit(
    client_id= REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

subreddit = reddit.subreddit("Rome") # Replace "python" with your desired subreddit
search_results = subreddit.search("restaurant recommendations", sort="Top", limit=10)

with open("output.txt", "w", encoding="utf-8", errors="ignore") as file:
    for search_result in search_results:
        file.write(search_result.selftext + "\n")