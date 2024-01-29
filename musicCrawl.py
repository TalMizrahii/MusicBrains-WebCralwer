import time
import requests
from lxml import html


def musicExpand(url, pageContents):
    # Convert the content of the page from a string to html object.
    page_html = html.fromstring(pageContents)

    # XPath's expression to select artist URLs on the MusicBrainz page.
    xpath = "//li/a[starts-with(@href, '/artist/')]/@href"

    # Extract artist URLs from the HTML content using XPath
    xpath_results = page_html.xpath(xpath)
    # Set an empty list to store the results.
    url_list = []

    # Expand relative URLs to full URLs.
    for result in xpath_results:
        # Split the URL based on the '?' character to remove parameters.
        url_parts = result.split('?')
        # Take only the first part, which contains the base URL.
        result = url_parts[0]
        # Check for valid artist pages.
        url_parts = result.split('/')
        # Check for valid artist pages.
        if url_parts[-1] == 'subscribers' or \
                url_parts[-1] == 'tags' or \
                url_parts[-1] == 'ratings' or \
                url_parts[-1] == 'details' or \
                url_parts[-1] == 'ratings' or \
                url_parts[-1] == 'edit':
            continue

        # Add the musicbrainz address.
        url_list.append("https://musicbrainz.org" + result)

    # At the base url to the list.
    url_list.append(url)

    # Remove duplicates by converting the list to a set and then back to a list.
    unique_urls = list(set(url_list))

    # Return the result.
    return unique_urls


def musicCrawl(url, xpaths):
    def crawl_page(url, crawled_urls, url_occurrences, result_list):
        if len(result_list) >= 50:
            return  # Stop crawling when 50 unique URLs are reached.

        # If the url we got has been crawled before, return.
        if url in crawled_urls:
            return

        # Get the web page from the base URL.
        response = requests.get(url)

        if response.status_code == 200:
            # Convert the response content to a string.
            page_content = response.content.decode('utf-8')

            # Use musicExpand to get expanded URLs.
            url_artist_list = set(musicExpand(url, page_content))

            # Exploring the urls in the crawled page using XPaths.
            page_html = html.fromstring(response.content)

            # Create a set to store URLs obtained from XPaths
            xpath_crawled_urls = set()

            # Apply each XPath expression.
            for xpath in xpaths:
                xpath_results = page_html.xpath(xpath)
                for result in xpath_results:
                    # Split the URL based on the '?' character to remove parameters.
                    url_parts = result.split('?')
                    # Take only the first part, which contains the base URL.
                    result = url_parts[0]
                    # Check for valid artist pages.
                    url_parts = result.split('/')
                    if url_parts[-1] == 'subscribers' or \
                            url_parts[-1] == 'tags' or \
                            url_parts[-1] == 'ratings' or \
                            url_parts[-1] == 'details' or \
                            url_parts[-1] == 'ratings' or \
                            url_parts[-1] == 'edit':
                        continue

                    full_url = "https://musicbrainz.org" + result
                    xpath_crawled_urls.add(full_url)

            # Combine the URLs from musicExpand and XPaths into a set
            url_artist_list.update(xpath_crawled_urls)

            # Update the occurrences count for each URL
            for u in url_artist_list:
                url_occurrences[u] = url_occurrences.get(u, 0) + 1

            # Add the result to the final list
            result_list.append([url] + list(url_artist_list))

            # Wait for 3 seconds before crawling the next page
            time.sleep(3)

            # Recursively crawl the expanded URLs
            for u in url_artist_list:
                crawl_page(u, crawled_urls, url_occurrences, result_list)

    # Initialize the data structures
    crawled_urls = set()
    url_occurrences = {}
    result_list = []

    # Start crawling from the initial URL
    crawl_page(url, crawled_urls, url_occurrences, result_list)

    # Sort the result list based on the specified criteria
    result_list.sort(key=lambda x: (url_occurrences.get(x[0], 0), x[0]))

    # Return the final result list (up to 50 unique URLs)
    return result_list[:50]


if __name__ == '__main__':
    xpaths = [
        "//a[starts-with(@href, '/artist/')]/@href",
        "//tr/td/a[starts-with(@href, '/artist/')]/@href",
        "//td[@role='cell']/a[starts-with(@href, '/artist/')][2]/@href",
        "//table/tbody/tr/td/span/a[starts-with(@href, '/artist/')]/@href",
        "//td[@role='cell']/a[starts-with(@href, '/artist/')][2]/@href",
        "//*[@id='content']/form/table[3]/tbody/tr/td/a[starts-with(@href, '/artist/')][2]/@href",
        "//*[contains(., ' / ')]/a[starts-with(@href, '/artist/')]/@href",
        "//bdi/../..//a[starts-with(@href, '/artist/')]/@href",
        "//*[@id='sidebar']/ul/li/a[starts-with(@href, '/artist/')]/@href"
    ]

    # # An artist url starting point
    artist_url = "https://musicbrainz.org/artist/b10bbbfc-cf9e-42e0-be17-e2c3e1d2600d"

    listUrls = musicCrawl(artist_url, xpaths)
    print(listUrls)
