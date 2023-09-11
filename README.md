## CrawlMeMaybe

### Overview

This is an asynchronous web crawler built in Python, using the aiohttp and BeautifulSoup4 libraries. The crawler fetches URLs from a given website up to a specified depth, and has options to include or exclude external links.

The crawler is designed to be fast and efficient, capable of fetching multiple URLs concurrently. It saves the fetched URLs in a text file, sorted in alphabetical order.
Features

- Asynchronous crawling using aiohttp
- URL parsing using BeautifulSoup4
- Fetches URLs up to a given depth
- Option to include or exclude external links
- Saves crawled URLs in alphabetical order to a text file

### Requirements

- Python 3.6+
- aiohttp
- BeautifulSoup4

### Installation

1. First, clone the repository:
``` bash
git clone https://github.com/PluggeRo/CrawlMeMaybe.git
```
2. Activate virtual env:
``` bash
cd CrawlMeMaybe
python -m venv venv
source venv/bin/activate
```
3. Then install the required packages:
``` bash
pip install -r requirements.txt
```

### Usage

``` bash
python crawlmemaybe.py -h
```

Run the crawler with the following command-line arguments:
- --url : The starting URL (required)
- --output : Output file to save the URLs (required)
- --depth : Maximum depth to search (required)
- --include-external : Flag to include external links (optional)

``` bash
python crawlmemaybe.py --url https://example.com --output urls.txt --depth 3 --include_external
```

>This will crawl https://example.com up to a depth of 3, including external links, and save the URLs to urls.txt.

### Contributing

If you'd like to contribute, please fork the repository and make changes as you'd like. Pull requests are warmly welcome.

### License

MIT

### Disclaimer

Please make sure to respect website terms, robots.txt, and any rate limitations when running the crawler.
