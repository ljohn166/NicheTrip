import praw
from dotenv import load_dotenv
import os

class DataCollector:
    @staticmethod
    async def collect_data(query: str) -> str:
        load_dotenv()

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

        subreddits = ["solotravel", "travel"]

        with open("output.txt", "w", encoding="utf-8", errors="ignore") as file:
            for subreddit in subreddits:
                for submission in reddit.subreddit(subreddit).top

        subreddit = reddit.subreddit("India")
        search_results = subreddit.search("restaurants", sort="Top", limit=1000)

        with open("output.txt", "w", encoding="utf-8", errors="ignore") as file:
            for search_result in search_results:
                file.write(search_result.selftext + "\n") 
                return 