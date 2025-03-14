# Digestif: your custom digest

This project addresses a simple personal need: How can I stay up to date with new technologies and scientific papers without having to sift through Hacker News or my RSS subscriptions?

Nowadays, the answer is simple: LLMs!

Digestif allows you to customize your daily digest by linking each of your RSS feeds (or multiple feeds) with a specific prompt.
Once your feeds are configured, a markdown digest will be generated every day at the same time.

## Getting started

The easiest way is to run the project with docker compose. You first need to set you `OPENAI_API_KEY` in `default.env` file. 
Then, simply run the following command:
```bash
docker compose up -d
```
