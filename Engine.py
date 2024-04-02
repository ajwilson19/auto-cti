# heart of the program to run the webscraping

import WebScrape

def run():
    all_articles=[]
    links = read_links()
    for link in links:
        scraped_articles = scrape(link)
        for article in scraped_articles:
            all_articles.append(article)
    return all_articles

def read_links():
    file = open("cti-links.txt")
    links = []
    for row in file:
        links.append(row[:-1])
    return links


def scrape(link):
    return WebScrape.scrape_link(link)