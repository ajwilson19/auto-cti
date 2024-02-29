# heart of the program to run the webscraping

import WebScrape

def run():
    links = read_links()
    for link in links:
        print(scrape(link))

def read_links():
    file = open("cti-links.txt")
    links = []
    for row in file:
        links.append(row[:-1])
    return links


def scrape(link):
    return WebScrape.scrape_link(link)