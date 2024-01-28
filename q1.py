import requests
from lxml import html


def get_related_artists_urls(artist_url_start):

    response = requests.get(artist_url_start)
    if response.status_code == 200:
        tree = html.fromstring(response.content)

        # Example XPath expressions
        xpaths = [
            "//a[starts-with(@href, '/artist/')]/@href",
            "//tr/td/a[starts-with(@href, '/artist/')]/@href",
            "//td[@role='cell']/a[starts-with(@href, '/artist/')][2]/@href",
            "//table/tbody/tr/td/span/a[starts-with(@href, '/artist/')]/@href",
            "//td[@role='cell']/a[starts-with(@href, '/artist/')][2]/@href",
            "//*[@id='content']/form/table[3]/tbody/tr/td/a[starts-with(@href, '/artist/')][2]/@href",
            "//*[contains(., ' / ')]/a[starts-with(@href, '/artist/')]/@href",
            "//li/ a[starts-with(@href, '/artist/')]/@href",
            "//bdi/../..//a[starts-with(@href, '/artist/')]/@href",
            "//*[@id='sidebar']/ul/li/a[starts-with(@href, '/artist/')]/@href"
        ]

        # Apply each XPath expression
        for xpath in xpaths:
            related_artists = tree.xpath(xpath)
            print(f"\nXPath: {xpath}")
            print(f"Found {len(related_artists)} results.")
            print(f"Found related artists: {related_artists}\n")


if __name__ == '__main__':
    # An artist url starting point
    artist_url = "https://musicbrainz.org/artist/b10bbbfc-cf9e-42e0-be17-e2c3e1d2600d"
    get_related_artists_urls(artist_url)
