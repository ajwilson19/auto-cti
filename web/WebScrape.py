import re
from urllib.request import urlopen
import web.gen_config as config

def scrape_link(link):
    if link.__contains__("cisa"):
        config.switch_cisa()
    elif link.__contains__("paloaltonetworks"):
        config.switch_palo_alto()
    page = urlopen(link)
    articles = get_article_links(page) #ARTICLE LINKS!!!!
    return get_formatted(articles)

def scrape_title(link):
    parsed = link.split("/")
    if parsed[-1] == '':
        return parsed[-2]
    return parsed[-1]

def get_article_links(page):
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
    links = []
    for article in articles:
        links.append(format_article_string(article))
    return links

def get_formatted(links):
    formatted = []
    for link in links:
        formatted.append([link, scrape_article(link)])
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
    article = urlopen(article_link)
    return read_article(article)

def format_article_string(article_string):
    sidx = article_string.find(config.LINK_STRIP_START) + len(config.LINK_STRIP_START)
    eidx = article_string.find(config.LINK_STRIP_END)
    return config.LINK_PREPEND + article_string[sidx:eidx]