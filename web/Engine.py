# heart of the program to run the webscraping

import web.WebScrape as WebScrape

def run():
    all_articles=[]
    links = read_links()
    for link in links:
        scraped_articles = scrape(link)
        for article in scraped_articles:
            all_articles.append(article)
    return all_articles

def read_links():
    links = open("cti-links.txt").readlines()
    return [link.replace("\n", "") for link in links]


def scrape(link):
    return WebScrape.scrape_link(link)