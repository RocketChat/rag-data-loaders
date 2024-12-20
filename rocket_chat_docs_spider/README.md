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

- Rate limiting: 5 seconds between requests
- Single concurrent request
- Respects robots.txt
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

## Usage
To run the spider, execute the following command:

```sh
scrapy runspider rcspider.py -o rocket_chat_docs.jsonl
```

The spider will crawl the Rocket.Chat documentation websites and save the extracted content to `rocket_chat_docs.jsonl`.

To send the output to a different file, change the filename in the `-o` argument.

For reading and processing the JSONL file, you can use the following Python code:

```python
python read_and_send.py
```

By default, the script reads the `rocket_chat_docs.jsonl` file and sends the extracted content to an edpoint defined in the `DocumentProcessor` class. However, you can change the endpoint or write your own custom callback function.


## Important Notes
- The spider implements polite crawling with a 5-second delay between requests
- Only URLs from `docs.rocket.chat` and `developer.rocket.chat` domains are crawled
- Already visited URLs are tracked to prevent duplicate crawling
