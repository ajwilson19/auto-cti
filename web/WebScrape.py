import re
from urllib.request import urlopen
import web.gen_config as config

def scrape_link(link):
    if link.__contains__("cisa"):
        config.switch_cisa()
    elif link.__contains__("paloaltonetworks"):
        config.switch_palo_alto()
    page = url_open(link)
    return read_page(page)

def scrape_title(link):
    parsed = link.split("/")
    if parsed[-1] == '':
        return parsed[-2]
    return parsed[-1]

def url_open(link):
    page = urlopen(link)
    return page

def read_page(page):
    html = page.read().decode("utf-8")
    articles_left = True
    articles = []
    while articles_left:
        sidx = html.find(config.ARTICLE_START)
        eidx = html.find(config.ARTICLE_END) + len(config.ARTICLE_END)
        article = html[sidx:eidx]
        if article != "":
            articles.append(article[article.find(config.LINK_START):article.find(config.LINK_END)])
        else:
            articles_left = False
        html = html[eidx:]
    count = 1
    formatted = []
    for article in articles:
        format_link = format_article_string(article)
        formatted.append([config.TYPE + " Article " + count, scrape_article(format_link),format_link])
        count += 1
    return formatted

def read_article(article):
    html = article.read().decode("utf-8")
    html = html[html.find(config.CONTENT_START):html.find(config.CONTENT_END) + len(config.CONTENT_END)]
    p_left = True
    paragraphs = []
    html = html[html.find(config.CONTENT_START):]
    while p_left:
        sidx = html.find(config.CONTENT_START)
        eidx = html.find(config.CONTENT_END) + len(config.CONTENT_END)
        paragraph = html[sidx:eidx]
        if paragraph == "":
            p_left = False
        html = html[eidx:]
        paragraphs.append(paragraph)

    full_article = ""
    for paragraph in paragraphs:
        full_article += remove_html(paragraph)
    return full_article

def remove_html(paragraph):
    new_paragraph = re.sub(re.compile('<.*?>'), '', paragraph)
    return new_paragraph

def scrape_article(article_link):
    if article_link.__contains__("cisa"):
        config.switch_cisa()
    elif article_link.__contains__("paloaltonetworks"):
        config.switch_palo_alto()
    article = url_open(article_link)
    return read_article(article)

def format_return(filename, link):
    return "Scraped webpage at " + link + " saved at " + filename

def format_article_string(article_string):
    sidx = article_string.find(config.LINK_STRIP_START) + len(config.LINK_STRIP_START)
    eidx = article_string.find(config.LINK_STRIP_END)
    return config.LINK_PREPEND + article_string[sidx:eidx]

#scrape_link("https://www.cisa.gov/news-events/cybersecurity-advisories")
#scrape_link("https://unit42.paloaltonetworks.com/category/threat-briefs-assessments/")
