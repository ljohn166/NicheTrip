import praw
from prawcore.exceptions import NotFound, Redirect, Forbidden
from dotenv import load_dotenv
import os
import time


load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

def getRedditData(city):
    #Checks if r/city is a real subreddit
    try:
        subreddit = reddit.subreddit(city)
        # Attempt to fetch its id to confirm existence
        _ = subreddit.id
        subreddits = ["solotravel", "travel", city]
        
        KEYWORDS = ["restaurants", "food", "hidden gem", "secret", "club", "pub", "night life", "activity", "niche"]

        # Quote multi-word keywords for Lucene
        keywords_lucene = [f'"{k}"' if " " in k else k for k in KEYWORDS]
        # Combine with OR for keywords
        keywords_query = " OR ".join(keywords_lucene)
        # Full query: CITY AND (keywords)
        query = f'"{city}" AND ({keywords_query})'

    except (NotFound, Redirect, Forbidden):
        #Omits city from the keywords and subreddit lists
        KEYWORDS = ["restaurants", "food", "hidden gem", "secret", "club", "pub", "night life", "activity", "niche"]
        query = "(" + " OR ".join(KEYWORDS) + ")"
        subreddits = ["solotravel", "travel"]

    #Writes data to output.txt - Searches through "limit" posts per subreddit and compiles their comments if they ahve >= 100 upvotes.
    with open("output.txt", "w", encoding="utf-8", errors="ignore") as file:
        for subreddit in subreddits:
            searchResults = reddit.subreddit(subreddit).search(query, sort="best", syntax="lucene", limit=10)
            for submission in searchResults:
                file.write("Post Name: [" + submission.title + "]")
                submission.comments.replace_more(limit=0)
                filteredComments = [comment for comment in submission.comments.list() if comment.score >= 100]
                for comment in filteredComments:
                    file.write("Upvotes: [" + str(comment.score) + "]" + "Comment: [" + comment.body + "]")



#TESTING CODE

# start = time.time()
# getRedditData("Rome")   # your original function
# end = time.time()
# print("Old method time:", end - start)

# start = time.time()
# getRedditDataNew("Rome")   # optimized function
# end = time.time()
# print("New method time:", end - start)