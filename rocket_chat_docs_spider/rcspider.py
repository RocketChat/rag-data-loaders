import scrapy
import re

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://docs.rocket.chat/docs', 'https://developer.rocket.chat/docs']
    visited_urls = set()

    custom_settings = {
        'CONCURRENT_REQUESTS': 1,           # One request at a time
        'DOWNLOAD_DELAY': 5,               # 5 seconds between requests
        'ROBOTSTXT_OBEY': True,
        'RETRY_TIMES': 3,                  # Retry failed requests
        'RETRY_HTTP_CODES': [403, 429, 500, 502, 503, 504],
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive'
        },
        'FEEDS': {
            'data/output.jsonl': {
                'format': 'jsonlines',
                'encoding': 'utf8'
            }
        }
    }

    def start_requests(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        # Extract all links on the page
        links = response.css('a::attr(href)').getall()
        filtered_links = [
            response.urljoin(link) for link in links 
            if ('docs.rocket.chat' in response.urljoin(link) or 'developer.rocket.chat' in response.urljoin(link))
            and response.urljoin(link) not in self.visited_urls
        ]
        # Follow links
        for link in filtered_links:
            if link not in self.visited_urls:
                self.visited_urls.add(link)
                yield scrapy.Request(response.urljoin(link), callback=self.parse)

        content = [c.strip() for c in response.css('.content_block div p::text').getall() if c.strip()]
        h2_headers = [h.strip() for h in response.css('.content_block div h2::text').getall() if h.strip()]
        page_title = response.css('.content_block div h1::text').get('').strip() 

        yield {
            "page_title": page_title or None,
            "content": content,
            "h2_headers": h2_headers,
            "url": response.url
        }
