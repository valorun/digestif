from os import getenv, listdir
from os.path import join
from time import sleep

from openai import OpenAI

from digestif.feed_extractor import download_feed, format_feed, format_feed_markdown
from digestif.model import FeedConfig
from digestif.nlp.llm_processor import LLMProcessor
from digestif.utils import parse_feed_config

FEEDS_PATH = getenv("FEEDS_PATH", "./feeds")
OUTPUT_PATH = getenv("OUTPUT_PATH", "./")


def get_feeds() -> list[FeedConfig]:
    feeds = []
    for file in listdir(FEEDS_PATH):
        if file.endswith((".yaml", ".yml")):
            feeds.append(parse_feed_config(join(FEEDS_PATH, file)))
    return feeds


def create_digest() -> str:
    feeds = get_feeds()
    openai_client = OpenAI()

    final_digest = ""
    for f in feeds:
        if f.name is not None and f.prompt is None:
            final_digest += f"# {f.name}\n"

        temp_llm_digest = ""
        for url in f.urls:
            print(f"Processing {url}")
            feed_content = download_feed(url)

            if f.prompt is not None:
                feed_content = format_feed(feed_content)
                temp_llm_digest += (
                    LLMProcessor(openai_client, f.prompt)(feed_content) + "\n\n"
                )
            else:
                feed_content = format_feed_markdown(feed_content)
                final_digest += feed_content
            print(temp_llm_digest)
            sleep(15)
        if f.prompt is not None:
            merged_feed_digest = LLMProcessor(
                openai_client,
                "Your role is to merge provided digests. You need to keep the same common structure.",
            )(temp_llm_digest)
            final_digest += merged_feed_digest

        final_digest += "\n\n"

        # If no prompt provided, display news under name, and with collapsible description

    with open(join(OUTPUT_PATH, "daily_digest.md"), "w") as f:
        f.write(final_digest)
    return final_digest
