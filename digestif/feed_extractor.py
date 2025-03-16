import feedparser
import requests
from datetime import datetime, timedelta
import time


def format_article(articles) -> str:
    return f"  <item>\n    <title>{articles.title}</title>\n    <link>{articles.link}</link>\n    <description>{articles.description}</description>\n    <pubDate>{articles.published}</pubDate>\n  </item>"


def download_feed(url: str) -> str:
    raw_data = requests.get(url).text
    print(raw_data)
    parsed_feed = feedparser.parse(raw_data)
    articles = parsed_feed.entries

    # Get only daily articles
    articles = [
        a
        for a in articles
        if a.published_parsed
        and isinstance(a.published_parsed, time.struct_time)
        and datetime(*a.published_parsed[:6])
        > (datetime.now() - timedelta(days=1))
    ]

    try:
        return (
            f"<channel>\n  <title>{parsed_feed.feed.title}</title>\n"
            + "\n".join([format_article(a) for a in articles])
            + "\n</channel>"
        )
    except AttributeError:
        return ""
