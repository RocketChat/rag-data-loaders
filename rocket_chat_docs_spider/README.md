# Rocket.Chat Documentation Spider

A web scraping tool built with Scrapy to extract documentation content from Rocket.Chat's official documentation websites.

## Overview

This spider crawls both the main Rocket.Chat documentation (`docs.rocket.chat/docs`) and developer documentation (`developer.rocket.chat/docs`) to extract:

- Page titles
- Main content
- H2 headers
- URLs

## Prerequisites

Install the required dependencies
:
## Create virtual environment
```sh
python -m venv .venv
```

## Activate virtual environment
```sh
source .venv/bin/activate
```

## Install dependencies
```sh
pip install -r requirements.txt
```

## Configuration
The spider is configured with the following settings:

- Rate limiting:The spider is configured with a 5-second delay between requests to avoid overwhelming the server and to follow polite crawling practices.

- Single concurrent request
- Respects robots.txt(The spider respects the `robots.txt` file, which means it will only crawl the pages allowed by Rocket.Chat's robots.txt rules.
)
- Automatic retry (3 times) for common error codes
- Custom user agent and headers for reliability

## Output
The spider generates a JSONL (JSON Lines) file with the following structure:
```
{
    "page_title": "Page Title",
    "content": ["Paragraph 1", "Paragraph 2", ...],
    "h2_headers": ["Header 1", "Header 2", ...],
    "url": "https://docs.rocket.chat/..."
}
```
sample 1:
{
    "page_title": "Introduction to Rocket.Chat",
    "content": ["Rocket.Chat is an open-source team communication platform.", "You can integrate Rocket.Chat with various services..."],
    "h2_headers": ["Overview", "Features", "Getting Started"],
    "url": "https://docs.rocket.chat/introduction"
}

## Usage
To run the spider, execute the following command:

```sh
scrapy runspider rcspider.py -o rocket_chat_docs.jsonl
```

The spider will crawl the Rocket.Chat documentation websites and save the extracted content to `rocket_chat_docs.jsonl`.

To send the output to a different file, change the filename in the `-o` argument.

For reading and processing the JSONL file, you can use the following Python code:

 # read_and_send.py
This script reads the `rocket_chat_docs.jsonl` file, processes the content, and sends it to a defined endpoint. By default, it uses the endpoint in the `DocumentProcessor` class, but this can be customized.



By default, the script reads the `rocket_chat_docs.jsonl` file and sends the extracted content to an edpoint defined in the `DocumentProcessor` class. However, you can change the endpoint or write your own custom callback function.
The spider generates a JSONL (JSON Lines) file, where each line contains a single JSON object with the following structure:`rocket_chat_docs.jsonl`


## Important Notes
- The spider implements polite crawling with a 5-second delay between requests
- Only URLs from `docs.rocket.chat` and `developer.rocket.chat` domains are crawled
- Already visited URLs are tracked to prevent duplicate crawling
