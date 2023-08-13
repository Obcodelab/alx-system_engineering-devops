#!/usr/bin/python3
"""
Query Reddit API recursively for all hot articles of a given subreddit
"""
import requests


def recurse(subreddit, hot_list=None, after=None):
    """
    Fetches hot subreddit article titles via recursive Reddit API queries.

    Args:
        subreddit (str): The name of the subreddit to query.
        hot_list (list, optional): Stores hot article titles. Default: None.
        after (str, optional): Reddit API marker for navigation. Default: None.

    Returns:
        List or None: Holds hot article titles if valid subreddit; else, None.
    """
    if hot_list is None:
        hot_list = []

    base_url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    params = {"limit": 100, "after": after}

    response = requests.get(
        base_url, headers={"User-Agent": "YOUR_USER_AGENT"}, params=params
    )

    # Check if the subreddit is valid
    if response.status_code == 404:
        return None

    data = response.json()

    # Add titles to the hot_list
    hot_list.extend([article["data"]["title"]
                     for article in data["data"]["children"]])

    # Check for pagination
    if data["data"]["after"]:
        return recurse(subreddit, hot_list, after=data["data"]["after"])
    else:
        return hot_list


# Call the function with the subreddit name
subreddit_name = "python"
hot_titles = recurse(subreddit_name)

if hot_titles is None:
    print(f"Subreddit '{subreddit_name}' is not valid.")
else:
    for i, title in enumerate(hot_titles, start=1):
        print(f"{i}. {title}")
