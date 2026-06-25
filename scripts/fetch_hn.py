#!/usr/bin/env python3
"""Fetch Hacker News data using only the Python standard library.

Two modes:

  python3 fetch_hn.py [N]
      Print the top N front-page stories (default 30) in HN rank order.

  python3 fetch_hn.py --comments ID [--max M]
      Print the top M (default 12) top-level comments for story ID, for drill-down.

No API key, no third-party packages. Talks to the public HN Firebase API.
"""

import sys
import re
import json
import html
import urllib.request
from concurrent.futures import ThreadPoolExecutor

API = "https://hacker-news.firebaseio.com/v0"
ITEM_URL = "https://news.ycombinator.com/item?id={}"
TIMEOUT = 15


def get(url):
    with urllib.request.urlopen(url, timeout=TIMEOUT) as r:
        return json.load(r)


def get_item(item_id):
    try:
        return get(f"{API}/item/{item_id}.json")
    except Exception as e:  # noqa: BLE001 - one bad item shouldn't kill the run
        return {"id": item_id, "error": str(e)}


def strip_html(text):
    """Turn HN's HTML comment text into plain readable text."""
    if not text:
        return ""
    text = text.replace("<p>", "\n").replace("</p>", "")
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(text).strip()


def shorten(text, limit=280):
    text = " ".join(text.split())
    return text if len(text) <= limit else text[:limit].rstrip() + "…"


def list_top(n):
    ids = get(f"{API}/topstories.json")[:n]
    with ThreadPoolExecutor(max_workers=12) as pool:
        stories = list(pool.map(get_item, ids))

    print(f"# Hacker News — top {len(stories)} (rank order)\n")
    for rank, s in enumerate(stories, 1):
        if s.get("error"):
            print(f"{rank}. [could not load story {s.get('id')}]")
            continue
        title = s.get("title", "(no title)")
        points = s.get("score", 0)
        comments = s.get("descendants", 0)
        article = s.get("url", "")  # context only; may be empty for Ask/Show HN self-posts
        hn = ITEM_URL.format(s.get("id"))
        print(f"{rank}. {title}")
        print(f"   points: {points} | comments: {comments}")
        if article:
            print(f"   article: {article}")
        print(f"   hn: {hn}")
        body = strip_html(s.get("text", ""))
        if body:
            print(f"   text: {shorten(body)}")
        print()


def list_comments(story_id, max_comments):
    story = get_item(story_id)
    if story.get("error"):
        print(f"Could not load story {story_id}: {story['error']}")
        return
    print(f"# Comments on: {story.get('title', story_id)}")
    print(f"# {ITEM_URL.format(story_id)}\n")
    kids = story.get("kids", [])[:max_comments]
    with ThreadPoolExecutor(max_workers=12) as pool:
        comments = list(pool.map(get_item, kids))
    for i, c in enumerate(comments, 1):
        if c.get("error") or c.get("deleted") or c.get("dead"):
            continue
        author = c.get("by", "someone")
        body = strip_html(c.get("text", ""))
        if not body:
            continue
        print(f"--- comment {i} (by {author}) ---")
        print(shorten(body, 700))
        print()


def main():
    args = sys.argv[1:]
    if args and args[0] == "--comments":
        if len(args) < 2:
            print("usage: fetch_hn.py --comments ID [--max M]")
            sys.exit(1)
        story_id = int(args[1])
        max_comments = 12
        if "--max" in args:
            max_comments = int(args[args.index("--max") + 1])
        list_comments(story_id, max_comments)
    else:
        n = int(args[0]) if args else 30
        list_top(n)


if __name__ == "__main__":
    main()
