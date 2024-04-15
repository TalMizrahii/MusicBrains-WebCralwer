<h1 align="center">
  
  ![python-logo-glassy](https://user-images.githubusercontent.com/103560553/204082228-92a30920-ca99-4517-9b9d-c3ab44d42a0b.png)

  MusicBrains Web Crawler
  <br>
</h1>

<h4 align="center"> A web crawler designed to crawl musicbrains.org, retrieving artist URLs starting from an artist page.
</h4>

<p align="center">
  <a href="#description">Description</a> •
  <a href="#implementation">Implementation</a> •
  <a href="#dependencies">Dependencies</a> •
  <a href="#installing-and-executing">Installing And Executing</a> •
  <a href="#author">Author</a> 
</p>

## Description
  
### About The Program

![download](https://github.com/TalMizrahii/MusicBrains-WebCralwer/assets/103560553/195b8887-82aa-4e4d-8b7c-23c924a35471)


The MusicBrains Web Crawler is a Python program designed to systematically traverse the MusicBrainz database, focusing on artist pages to gather URLs of related artists. It accomplishes this through two primary functions:

musicExpand: This function takes a URL of an artist's MusicBrainz page and the corresponding webpage contents as input. Its purpose is to expand the initial URL into a list of URLs representing pages related to the same artist. Using a combination of XPath expressions and URL manipulation in Python, it ensures that only relevant pages within the musicbrainz.org domain and belonging to the same artist are included. For instance, it may return URLs such as https://musicbrainz.org/artist/eab76c9f-ff91-4431-b6dd-3b976c598020/relationships or https://musicbrainz.org/artist/eab76c9f-ff91-4431-b6dd-3b976c598020/recordings.

musicCrawl: This function is responsible for crawling the expanded URLs obtained from the musicExpand function. It takes the initial artist URL and a list of XPath expressions as input. The function utilizes the expanded URLs and XPath expressions to extract a set of URLs matching the given expressions. These URLs are then prioritized based on their occurrence count in the crawled web pages, with ties being resolved alphabetically. The function adheres to crawling ethics, waiting at least 3 seconds between page reads. It ensures that at most 50 unique URLs of musicbrainz.org are crawled, and each URL is crawled only once. The function returns a list of lists, where each inner list contains a source URL that has been crawled and URLs of related pages detected by the XPath expressions, converted to full URLs.

![featured_image_musicbrainz](https://github.com/TalMizrahii/MusicBrains-WebCralwer/assets/103560553/af2522e2-4a39-40d6-a4eb-a35cb140c0cd)


These functions collectively form the core of the MusicBrains Web Crawler, enabling systematic exploration of artist pages on MusicBrainz to uncover related artists and their associated information. The program utilizes Python's requests library for web requests and the lxml library for parsing HTML content, offering a robust and efficient solution for gathering music-related data from the web.

## Implementation

The program consists of two Python scripts:
- **musicrawl.py**: This script defines functions for expanding URLs and crawling web pages. It utilizes the `requests` library to fetch web pages and the `lxml` library to parse HTML content. The `musicExpand` function expands relative artist URLs to full URLs and filters out irrelevant pages. The `musicCrawl` function recursively crawls through artist pages, collecting related artist URLs.
- **q1.py**: This script demonstrates the usage of XPath expressions to extract related artist URLs from a given artist page. It defines a function `get_related_artists_urls` which takes an artist URL as input and applies a set of predefined XPath expressions to locate related artist links.

  <img width="368" alt="1" src="https://github.com/TalMizrahii/MusicBrains-WebCralwer/assets/103560553/b5b84d9b-261a-48f6-9028-daa331214df9.PNG">
### Important
The program expands only 50 different URLs (but you can always change it if you like). It also takes into consideration crawling ethics, so between each HTTP request to the site, there is a 3-second waiting time.

## Dependencies

The program requires the following dependencies:
- Python 3.x
- requests library
- lxml library

## Installing And Executing

To install and run the program you use [Git](https://git-scm.com). From your command line:

```bash
# Clone this repository.
$ git clone https://github.com/TalMizrahii/MusicBrains-WebCralwer

# Navigate to the repository directory:
$ cd MusicBrains-WebCrawler

# Run the program
$ python musicrawl.py
```
## Author

* [@Tal Mizrahi](https://github.com/TalMizrahii)
* Taltalon1927@gmail.com
