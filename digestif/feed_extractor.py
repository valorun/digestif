import time
from datetime import datetime, timedelta

import feedparser
import requests



def format_article(articles) -> str:
    return f"  <item>\n    <title>{articles.title}</title>\n    <link>{articles.link}</link>\n    <description>{articles.description}</description>\n    <pubDate>{articles.published}</pubDate>\n  </item>"


def download_feed(url) -> feedparser.FeedParserDict:
    raw_data = requests.get(url).text
    parsed_feed = feedparser.parse(raw_data)

    # Get only daily articles
    parsed_feed.entries = [
        a
        for a in parsed_feed.entries
        if a.published_parsed
        and isinstance(a.published_parsed, time.struct_time)
        and datetime(*a.published_parsed[:6]) > (datetime.now() - timedelta(days=1))
    ]
    return parsed_feed


def format_feed(parsed_feed: feedparser.FeedParserDict) -> str:
    articles = parsed_feed.entries

    try:
        return (
            f"<channel>\n  <title>{parsed_feed.feed.title}</title>\n"
            + "\n".join([format_article(a) for a in articles])
            + "\n</channel>"
        )
    except AttributeError:
        return ""


def format_feed_markdown(
    parsed_feed: feedparser.FeedParserDict,
) -> str:
    articles = parsed_feed.entries

    return "\n".join([f"- [{a.title}]({a.link})" for a in articles])
