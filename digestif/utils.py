from digestif.model import FeedConfig
import yaml


def parse_feed_config(path: str) -> FeedConfig:
    with open(path, "r") as f:
        content = yaml.safe_load(f)
        urls = content.get("urls")
        prompt = content.get("prompt")
        name = content.get("name")

        return FeedConfig(urls=urls, prompt=prompt, name=name)
