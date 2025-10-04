import praw

# Initialize PRAW with your Reddit instance
# (client_id, client_secret, user_agent, etc.)
reddit = praw.Reddit(
    client_id="5zFp4nf-ktp9nrxhvdy1OQ",
    client_secret="DXWkC3PyIPYct2Q2MwJooCtfEKERXA",
    user_agent="Niche Trip"
)

subreddit = reddit.subreddit("Rome") # Replace "python" with your desired subreddit
search_results = subreddit.search("restaurants", sort="relevance", limit=10)

with open("output.txt", "w", encoding="utf-8", errors="ignore") as file:
    for search_result in search_results:
        file.write(search_result.selftext + "\n")