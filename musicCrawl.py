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
    url_list = set()

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
        url_list.add("https://musicbrainz.org" + result)

    # At the base url to the list.
    url_list.add(url)

    # Return the result.
    return list(url_list)


def musicCrawl(url, xpaths):
    def crawl_page(url, crawled_urls, url_occurrences, result_list):
        if len(crawled_urls) >= 50:
            return  # Stop crawling when 50 unique URLs are reached.

        # Add the current url to the crawled_urls.
        crawled_urls.add(url)

        # Get the web page from the base URL.
        response = requests.get(url)

        if response.status_code == 200:
            # Convert the response content to a string.
            page_content = response.content.decode('utf-8')

            # Use musicExpand to get expanded URLs.
            url_artist_list = set(musicExpand(url, page_content))

            # Update the occurrences count for each URL
            for u in url_artist_list:
                url_occurrences[u] = url_occurrences.get(u, 0) + 1

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
                    # Create the full url.
                    full_url = "https://musicbrainz.org" + result
                    # Add the count of the url.
                    url_occurrences[full_url] = url_occurrences.get(full_url, 0) + 1
                    # Add the url to the crawled urls.
                    xpath_crawled_urls.add(full_url)

            # Combine the URLs from musicExpand and XPaths into a set.
            url_artist_list.update(xpath_crawled_urls)

            # Add the url to the result list.
            for u in url_artist_list:
                # Check for same pair (supposed to be  only 1).
                if u == url:
                    continue
                # Add the src and des elements to the list.
                result_list.append([url, u])
            # Sort the list
            result_list.sort(key=lambda x: (-url_occurrences.get(x[1], 0), x[1]))

            # Wait before crawling the next page.
            time.sleep(1)

            # Recursively crawl the expanded URLs.
            for u in result_list:
                if u[1] not in crawled_urls:
                    crawl_page(u[1], crawled_urls, url_occurrences, result_list)

    # Initialize the data structures
    crawled_urls = set()
    url_occurrences = {}
    result_list = []

    # Start crawling from the initial URL
    crawl_page(url, crawled_urls, url_occurrences, result_list)

    # Sort the result list based on the specified criteria
    result_list.sort(key=lambda x: (url_occurrences.get(x[0], 0), x[0]))

    # Return the final result list (up to 50 unique URLs)
    return result_list


def check_pairs(lst):
    seen_pairs = set()
    identical_pairs = set()
    same_source_destination_pair = None

    for pair in lst:
        source, destination = pair
        current_pair = (source, destination)

        if current_pair in seen_pairs:
            identical_pairs.add(current_pair)

        seen_pairs.add(current_pair)

        if same_source_destination_pair is None and source == destination:
            same_source_destination_pair = current_pair

    return identical_pairs, same_source_destination_pair


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

    # An artist url starting point
    artist_url = "https://musicbrainz.org/artist/eab76c9f-ff91-4431-b6dd-3b976c598020"

    listUrls = musicCrawl(artist_url, xpaths)

    identical_pairs, same_source_destination_pair = check_pairs(listUrls)

    print("Identical Pairs:", identical_pairs)
    print("Same Source and Destination Pair:", same_source_destination_pair)
