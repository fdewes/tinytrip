# tinytrip

tinytrip is an easy to use/modify recursive text webscraper 

## Usage

`./tinytrip.py https://www.projekt-gutenberg.org/kafka/amerika/amerika.html -w kafka/amerika`

## Help

`$ ./tinytrip.py -h
usage: tinytrip.py [-h] [-w WHITELIST [WHITELIST ...]] [-b BLACKLIST [BLACKLIST ...]] [-f FILE_TYPES] [-o OUT_FILE [OUT_FILE ...]] [--version] url

tinytrip - easy to use text web scraper

positional arguments:
  url                   url to retreive links from

optional arguments:
  -h, --help            show this help message and exit
  -w WHITELIST [WHITELIST ...]
                        (list of) regex(es) that must appear in url
  -b BLACKLIST [BLACKLIST ...]
                        (list of) regex(es) that must not appear in url
  -f FILE_TYPES         regex for file types to crawl. default: html?$
  -o OUT_FILE [OUT_FILE ...]
                        Output file
  --version             show program's version number and exit
`


