from os import getenv, listdir
from os.path import join
from time import sleep

from openai import OpenAI

from digestif.feed_extractor import download_feed
from digestif.model import FeedConfig
from digestif.nlp.llm_processor import LLMProcessor
from digestif.utils import parse_feed_config

FEEDS_PATH = getenv("FEEDS_PATH", "")
OUTPUT_PATH = getenv("OUTPUT_PATH", "")


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
        base_digest = ""
        for url in f.urls:
            print(f"Processing {url}")
            feed_content = download_feed(url)

            base_digest += LLMProcessor(openai_client, f.prompt)(feed_content) + "\n\n"
            print(base_digest)
            sleep(5)
        merged_feed_digest = LLMProcessor(
            openai_client,
            "Your role is to merge provided digests. You need to keep the same common structure.",
        )(base_digest)
        final_digest += merged_feed_digest + "\n\n"

    with open(join(OUTPUT_PATH, "daily_digest.md"), "w") as f:
        f.write(final_digest)
    return final_digest
