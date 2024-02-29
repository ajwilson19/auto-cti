import re
from urllib.request import urlopen

def scrape_link(link):
    page = url_open(link)
    read_page(page)

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
        sidx = html.find("<article")
        eidx = html.find("</article>") + len("</article>")
        article = html[sidx:eidx]
        if article != "":
            articles.append(article[article.find("<h3 class=\"h5 news__title mb-15\">"):article.find("</h3>")])
        else:
            articles_left = False
        html = html[eidx:]
    count = 1
    for article in articles:
        print("Article", count, scrape_article(format_article_string(article)))
        count += 1

def read_article(article):
    html = article.read().decode("utf-8")
    html = html[html.find("<div class=\"article__content"):html.find("</article>") + len("</article>")]
    #print(html)
    p_left = True
    #print(html)
    paragraphs = []
    html = html[html.find("<p>"):]
    while p_left:
        sidx = html.find("<p>")
        eidx = html.find("</p>") + len("</p>")
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
    article = url_open(article_link)
    return read_article(article)

def format_return(filename, link):
    return "Scraped webpage at " + link + " saved at " + filename

def format_article_string(article_string):
    sidx = article_string.find("<h3 class=\"h5 news__title mb-15\"><a href=\"") + len("<h3 class=\"h5 news__title mb-15\"><a href=\"")
    eidx = article_string.find("\" data-page-track=")
    return article_string[sidx:eidx]

scrape_link("https://unit42.paloaltonetworks.com/category/threat-briefs-assessments/")