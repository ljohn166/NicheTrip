import praw
from prawcore.exceptions import NotFound, Redirect, Forbidden
from dotenv import load_dotenv
import os
from fastapi.concurrency import run_in_threadpool


def getRedditData(city):
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

    CITY = city


    try:
        subreddit = reddit.subreddit(CITY)
        # Attempt to fetch its id to confirm existence
        _ = subreddit.id
        subreddits = ["solotravel", "travel", CITY]
        
        KEYWORDS = ["restaurants", "food", "hidden gem", "secret", "club", "pub", "night life", "activity", "niche"]

        # Quote multi-word keywords for Lucene
        keywords_lucene = [f'"{k}"' if " " in k else k for k in KEYWORDS]

        # Combine with OR for keywords
        keywords_query = " OR ".join(keywords_lucene)

        # Full query: CITY AND (keywords)
        query = f'"{CITY}" AND ({keywords_query})'
        print(f"Subreddit r/{CITY} exists!")
    except (NotFound, Redirect, Forbidden):
        KEYWORDS = ["restaurants", "food", "hidden gem", "secret", "club", "pub", "night life", "activity", "niche"]
        query = "(" + " OR ".join(KEYWORDS) + ")"
        subreddits = ["solotravel", "travel"]
        print(f"Subreddit r/{CITY} does NOT exist.")

    with open("output.txt", "w", encoding="utf-8", errors="ignore") as file:
        for subreddit in subreddits:
            searchResults = reddit.subreddit(subreddit).search(query, sort="best", syntax="lucene", limit=10)
            for submission in searchResults:
                file.write("Post Name: [" + submission.title + "]")
                submission.comments.replace_more(limit=0)
                filteredComments = [comment for comment in submission.comments.list() if comment.score >= 100]
                for comment in filteredComments:
                    file.write("Upvotes: [" + str(comment.score) + "]" + "Comment: [" + comment.body + "]")



