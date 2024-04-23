import re
from urllib.request import Request, urlopen
from chalicelib import gen_config as config

def scrape_link(link):
    switch(link)
    page = url_open(link)
    articles = get_article_links(page) #ARTICLE LINKS!!!!
    return articles

def url_open(link):
    req = Request(
        url=link,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    page = urlopen(req)
    return page

def scrape_title(link):
    parsed = link.split("/")
    if parsed[-1] == '':
        return parsed[-2]
    return parsed[-1]

def get_article_links(page):
    html = page.read().decode("utf-8")
    articles_left = True
    articles = []
    html = html[html.find(config.SPLICE):]
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
        link = check_ignore(format_article_string(article))
        if link is not None:
            links.append(link)
    return links

def check_ignore(link):
    if config.IGNORE is not None:
        for IGNORE in config.IGNORE:
            if link.__contains__(IGNORE):
                return None
    return link

def get_formatted(links):
    formatted = []
    for link in links:
        try:
            formatted.append([link, scrape_article(link)])
        except:
            pass
    return formatted

def read_article(article):
    html = article.read().decode("utf-8")
    html = html[html.find(config.CONTENT_START):html.find(config.CONTENT_END) + len(config.CONTENT_END)]
    p_left = True
    paragraphs = []
    html = html[html.find(config.CONTENT_START):]
    while p_left:
        sidx = html.find(config.PARAGRAPH_START)
        eidx = html.find(config.PARAGRAPH_END)
        paragraph = html[sidx:eidx]
        if paragraph == "":
            p_left = False
        html = html[eidx + len(config.PARAGRAPH_END):]
        paragraphs.append(paragraph)

    full_article = ""
    for paragraph in paragraphs:
        full_article += remove_html(paragraph)
    return full_article

def remove_html(paragraph):
    new_paragraph = re.sub(re.compile('<.*?>'), '', paragraph)
    return new_paragraph

def scrape_article(article_link):
    switch(article_link)
    article = url_open(article_link)
    return read_article(article)

def switch(link):
    if link.__contains__("cisa"):
        config.switch_cisa()
    elif link.__contains__("paloaltonetworks"):
        config.switch_palo_alto()
    elif link.__contains__("bleeping"):
        config.switch_bleeping_computer()
    elif link.__contains__("talosintel"):
        config.switch_bleeping_computer()
    elif link.__contains__("thehackernews"):
        config.switch_hacker_news()

def format_article_string(article_string):
    sidx = article_string.find(config.LINK_STRIP_START) + len(config.LINK_STRIP_START)
    eidx = article_string.find(config.LINK_STRIP_END)
    return format_link(config.LINK_PREPEND + article_string[sidx:eidx])

def format_link(link):
    if link.__contains__("\""):
        return link.strip("\"")
    elif link.__contains__("\'"):
        return link.strip("\'")
    return link
