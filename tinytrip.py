#!/usr/bin/env python3
"""
tinytrip - an easy to use text/html webscraper
"""

__author__ = "Florian Dewes"
__version__ = "0.1aleph"
__license__ = "GPLv3"

from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from urllib.error import URLError
import re
import socket
import json
from time import time
from urllib.parse import urljoin
import argparse
from logzero import logger


def get_html(url, timeout=10):
    """
    downloads the html file and catches various exceptions that can occur
    when crawling the web
    """

    try:
        html = urlopen(Request(url, headers={"User-Agent": "Mozilla"}),
                       timeout=timeout)
    except HTTPError as e:
        logger.warning(url, "HTTPError exception:", e)
        return None
    except URLError as e:
        logger.warning(url, "URLError exception: ", e)
        return None
    except socket.timeout as e:
        logger.warning(url, "socket.timeout exception: ", e)
        return None
    else:
        return html


def soupit(html, parser="html.parser"):
    """
    converts the raw html to BeautifulSoup and catches exceptions.
    """

    try:
        page = BeautifulSoup(html.read(), "html.parser", from_encoding="utf-8")
    except socket.timeout as e:
        logger.warning("Timeout: ", e)
        return None
    except AttributeError as e:
        logger.warning("AttributeError: ", e)
        return None
    return page


def get_links(url):
    """
    extracts all links from a web page and returns them as a unique list.
    """

    links = []

    html = get_html(url)
    soup = soupit(html)

    for link in soup.findAll("a"):
        links.append((link.get("href")))

    return(list(set(links)))


def create_abs_link(url, links):
    """
    converts all links found in url to absolute paths.
    """

    if links == [None]:
        return []

    abs_links = []

    for link in links:
        if link is None:
            continue
        else:
            abs_links.append(urljoin(url, link))
    return abs_links


def crawl(url=None, level=0):
    """
    recursive crawl function, which calls itself on all links that come appear
    on current page. filters out non-whitelisted (=unwanted) urls.
    returns a sorted list of urls that have been scraped and
    saves html as string to a global dictionary with the urls as keys.
    """

    start_time = time()

    html = get_html(url)
    soup = soupit(html)

    crawled_html[url] = str(soup)

    if soup is None:
        return []

    links = get_links(url)
    links = create_abs_link(url, links)

    site_whitelist = re.compile("|".join(url_whitelist))
    file_whitelist = re.compile("|".join(file_types))
    site_blacklist = re.compile("|".join(url_blacklist))

    links = [l for l in links if site_blacklist.search(l) is None
             and site_whitelist.search(l) is not None
             and file_whitelist.search(l) is not None]

    return_links = [url]

    level += 1

    for link in links:
        if link not in crawled_html.keys():
            return_links = return_links + crawl(url=link,
                                                level=level)

    return_links.sort()

    url_log = "url: {0} (scraped {1} link(s) in {2:1.2f} secs. distance: {3:1d})".format(url,
                              len(return_links),
                              time()-start_time,
                              level-1)

    logger.info(url_log)

    return return_links


def main(args):
    """
    making text corpora uncool again
    calls the recursive crawler function and stores the content of the scraped
    web pages to a single json file (for now. more options to come.)
    """

    start_time = time()

    global crawled_html
    global url_blacklist
    global url_whitelist
    global file_types

    crawled_html = dict()
    url_blacklist = args.blacklist + [" "]
    url_whitelist = args.whitelist
    file_types = args.file_types

    crawled_sites = crawl(url=args.url)

    out_file = re.sub(r"[:|/|\.|]", "_", args.url) + ".json"
    out_file = re.sub("_+", "_", out_file)

    with open(out_file, "w") as f:
        json.dump(crawled_html, f)

    logger.info("crawled {0} urls in {1:1.2f} secs.".
                format(len(crawled_sites), round(time()-start_time, 2)))


if __name__ == "__main__":
    """
    parse command line arguments
    """

    description = "tinytrip - easy to use sloth web scraper"


    parser = (argparse.ArgumentParser(description=description))

    parser.add_argument("url", help="start url")

    parser.add_argument("-f", default=["html?$"],
                        action="store", dest="file_types",
                        help="regex for file types to crawl. default: html?$")

    parser.add_argument("-w", default=[""], nargs='+', 
                        action="store", dest="whitelist",
                        help="(list of) regex(es) that must appear in url to be considered")

    parser.add_argument("-b", default=[], nargs='+',
                        action="store", dest="blacklist",
                        help="(list of) regex(es) that must not appear in url to be considered")

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()

    main(args)
