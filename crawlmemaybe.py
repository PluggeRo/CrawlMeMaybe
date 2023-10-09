import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse
from asyncio import Queue

# Worker coroutine for crawling URLs up to a specified depth
async def worker(session, queue, visited, lock, sorted_output, max_depth, include_external, root_domain):
    while True:
        # Dequeue a URL and its depth from the central task queue
        depth, url = await queue.get()

        # Skip if depth exceeds maximum
        if depth > max_depth:
            queue.task_done()
            continue

        # Check if the URL is an external link
        domain = urlparse(url).netloc
        if not include_external and domain != root_domain:
            queue.task_done()
            continue

        # Atomically check and update the 'visited' set
        async with lock:
            if url in visited:
                queue.task_done()
                continue
            visited.add(url)

        # Fetch the URL content
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    text = await response.text()
                else:
                    print(f"HTTP error {response.status} when fetching {url}")
                    queue.task_done()
                    continue
        except aiohttp.ClientError as e:
            print(f"HTTP Error for URL {url}: {e}")
            queue.task_done()
            continue
        except Exception as e:
            print(f"Unexpected Error for URL {url}: {e}")
            queue.task_done()
            continue

        # Append the URL to the sorted_output list and print it
        async with lock:
            sorted_output.append(url)
        print(url)

        # Parse the page content and enqueue new URLs
        soup = BeautifulSoup(text, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                full_url = urljoin(url, href)
                await queue.put((depth + 1, full_url))

        # Mark the task as done
        queue.task_done()

# Main coroutine for managing the crawler
async def main(args):
    visited = set()
    lock = asyncio.Lock()
    queue = Queue()
    await queue.put((0, args.url))

    # Extract the root domain of the starting URL
    root_domain = urlparse(args.url).netloc

    # Create an HTTP session and an empty list to hold the URLs
    sorted_output = []
    async with aiohttp.ClientSession() as session:
        # Launch worker tasks
        workers = [asyncio.create_task(worker(session, queue, visited, lock, sorted_output, args.depth, args.include_external, root_domain)) for _ in range(10)]
        # Wait for all URLs to be processed
        await queue.join()

        # Cancel the workers
        for w in workers:
            w.cancel()

    # Sort and write the URLs to the output file
    sorted_output.sort()
    with open(args.output, 'w') as output_file:
        for url in sorted_output:
            output_file.write(url + "\n")

# Entry point of the script
if __name__ == "__main__":
    # Command-line argument parsing
    parser = argparse.ArgumentParser(description='Asynchronous Web Crawler')
    parser.add_argument('--url', type=str, required=True, help='Starting URL')
    parser.add_argument('--output', type=str, required=True, help='Output file')
    parser.add_argument('--depth', type=int, default=1, help='Maximum depth to search')
    parser.add_argument('--include-external', action='store_true', help='Whether to include external links')
    args = parser.parse_args()

    # Run the main coroutine
    asyncio.run(main(args))
