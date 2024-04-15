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

The MusicBrains Web Crawler is a Python program designed to crawl musicbrains.org, a database of music information. It specifically targets artist pages to retrieve URLs of related artists. The program employs web crawling techniques, utilizing XPath expressions to locate and extract relevant links from HTML content.

## Implementation

The program consists of two Python scripts:
- **musicrawl.py**: This script defines functions for expanding URLs and crawling web pages. It utilizes the `requests` library to fetch web pages and the `lxml` library to parse HTML content. The `musicExpand` function expands relative artist URLs to full URLs and filters out irrelevant pages. The `musicCrawl` function recursively crawls through artist pages, collecting related artist URLs.
- **q1.py**: This script demonstrates the usage of XPath expressions to extract related artist URLs from a given artist page. It defines a function `get_related_artists_urls` which takes an artist URL as input and applies a set of predefined XPath expressions to locate related artist links.

## Dependencies

The program requires the following dependencies:
- Python 3.x
- requests library
- lxml library

## Installing And Executing

To install and run the program you can click on the [release](https://github.com/TalMizrahii/Encryption-Box/releases/tag/v1.0) button in this repository.
  
You can also use [Git](https://git-scm.com). From your command line:

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
