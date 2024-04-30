"""
* Author: Dbog
* Date: 4/19/2024
* Description: A general configuration file built to change the configuration
                during runtime based on the links that are sent into the web scraper.
                Configurations fit into the web scraper for different pieces to splice
                the article at to get the unstructured article to a structured point
"""

TYPE=""
SPLICE=""
ARTICLE_START=""
ARTICLE_END=""
LINK_START=""
LINK_END=""
LINK_PREPEND=""
LINK_STRIP_START=""
LINK_STRIP_END=""
CONTENT_START=""
CONTENT_END=""
PARAGRAPH_START=""
PARAGRAPH_END=""
IGNORE=None

"""
    Switches the Config class global variables to the desired values based on 
        the input values. 
    Input: Current link to be scraped 
    Output: No Output
"""
def switch(link) -> None:
    if link.__contains__("cisa"):
        switch_cisa()
    elif link.__contains__("paloaltonetworks"):
        switch_palo_alto()
    elif link.__contains__("bleeping"):
        switch_bleeping_computer()
    elif link.__contains__("talosintel"):
        switch_bleeping_computer()
    elif link.__contains__("thehackernews"):
        switch_hacker_news()
    else:
        print("Invalid Link:", link)

"""
    Changes the current global variables of the file to be the correct parsing values
        for Web Scraping of CISA Web Pages
    Input: No Function Input
    Output: No Function Output
"""
def switch_cisa() -> None:
    # Global Variable Declaration to ensure changes
    global TYPE,ARTICLE_START,ARTICLE_END,LINK_START,LINK_END,LINK_PREPEND,LINK_STRIP_START,\
        LINK_STRIP_END,CONTENT_START,CONTENT_END,PARAGRAPH_END,PARAGRAPH_START

    # Values to be changed for current type of link.
    # Only values that need to be changed are imported.
    TYPE="CISA"
    ARTICLE_START = "<div  class=\"c-view__row\">"
    ARTICLE_END = "</article>"
    LINK_START = "<a href=\""
    LINK_END = "</a>"
    LINK_PREPEND = "https://www.cisa.gov"
    LINK_STRIP_START = "<a href=\""
    LINK_STRIP_END = "\" "
    CONTENT_START = "<main id=\"main"
    CONTENT_END = "<div class=\"l-constrain l-page-section--rich-text\">"
    PARAGRAPH_START = "<h1 class=\"c-page-title__title\">"
    PARAGRAPH_END = "<div class=\"l-constrain l-page-section--rich-text\">"

"""
    Changes the current global variables of the file to be the correct parsing values
        for Web Scraping of Palo Alto Unit 42 Web Pages
    Input: No Function Input
    Output: No Function Output
"""
def switch_palo_alto() -> None:
    # Global Variable Declaration to ensure changes
    global TYPE, ARTICLE_START, ARTICLE_END, LINK_START, LINK_END, LINK_STRIP_START, \
        LINK_STRIP_END, CONTENT_START, CONTENT_END, PARAGRAPH_END, PARAGRAPH_START

    # Values to be changed for current type of link.
    # Only values that need to be changed are imported.
    TYPE = "PaloAlto"
    ARTICLE_START = "<article"
    ARTICLE_END = "</article>"
    LINK_START = "<h3 class=\"h5 news__title mb-15\">"
    LINK_END = "</h3>"
    LINK_STRIP_START = "<h3 class=\"h5 news__title mb-15\"><a href=\""
    LINK_STRIP_END = "\" data-page-track="
    CONTENT_START = "<div class=\"article__content"
    CONTENT_END = "</article>"
    PARAGRAPH_START = "<p"
    PARAGRAPH_END = "</p>"

"""
    Changes the current global variables of the file to be the correct parsing values
        for Web Scraping of Bleeping Computer Web Pages
    Input: No Function Input
    Output: No Function Output
"""
def switch_bleeping_computer() -> None:
    # Global Variable Declaration to ensure changes
    global TYPE, ARTICLE_START, ARTICLE_END, LINK_START, LINK_END, LINK_STRIP_START, \
        LINK_STRIP_END, CONTENT_START, CONTENT_END, PARAGRAPH_END, PARAGRAPH_START, SPLICE, IGNORE

    # Values to be changed for current type of link.
    # Only values that need to be changed are imported.
    TYPE = "BleepingComputer"
    SPLICE = "<ul id=\"bc-home-news-main-wrap\""
    ARTICLE_START = "<li"
    ARTICLE_END = "</ul></div>"
    LINK_START = "<h4><a href"
    LINK_END = "</a></h4>"
    LINK_STRIP_START = "<h4><a href=\""
    LINK_STRIP_END = "\">"
    CONTENT_START = "<article"
    CONTENT_END = "<div class=\"cz-related-article-wrapp"
    PARAGRAPH_START = "<p"
    PARAGRAPH_END = "</p>"
    IGNORE = ["/deals/","rel=\"sponsored"]

"""
    Changes the current global variables of the file to be the correct parsing values
        for Web Scraping of Talos Intelligence Web Pages
    Input: No Function Input
    Output: No Function Output
"""
def switch_talos() -> None:
    # Global Variable Declaration to ensure changes
    global TYPE, ARTICLE_START, ARTICLE_END, LINK_START, LINK_END, LINK_PREPEND, LINK_STRIP_START, \
        LINK_STRIP_END, CONTENT_START, CONTENT_END, PARAGRAPH_END, PARAGRAPH_START

    # Values to be changed for current type of link.
    # Only values that need to be changed are imported.
    TYPE = "Talos"
    ARTICLE_START = "<tr class="
    ARTICLE_END = "</tr>"
    LINK_START = "<a href="
    LINK_END = "</a>"
    LINK_PREPEND = "https://talosintelligence.com"
    LINK_STRIP_START = "<a href=\""
    LINK_STRIP_END = "\">"
    CONTENT_START = "<div class=\"row\">"
    CONTENT_END = "<div class=\"text-center button_area\">"
    PARAGRAPH_START = "<p"
    PARAGRAPH_END = "</p>"

"""
    Changes the current global variables of the file to be the correct parsing values
        for Web Scraping of HackerNews Web Pages
    Input: No Function Input
    Output: No Function Output
"""
def switch_hacker_news() -> None:
    # Global Variable Declaration to ensure changes
    global TYPE, ARTICLE_START, ARTICLE_END, LINK_START, LINK_END, LINK_STRIP_START, \
        LINK_STRIP_END, CONTENT_START, CONTENT_END, PARAGRAPH_END, PARAGRAPH_START, SPLICE, IGNORE

    # Values to be changed for current type of link.
    # Only values that need to be changed are imported.
    TYPE = "HackerNews"
    SPLICE = "<div class=\'body-post"
    ARTICLE_START = "<a class=\'story-link"
    ARTICLE_END = "</a>"
    LINK_START = "<a class=\'story-link"
    LINK_END = "</div>"
    LINK_STRIP_START = "href="
    LINK_STRIP_END = ">"
    CONTENT_START = "<main class="
    CONTENT_END = "</main>"
    PARAGRAPH_START = "<p"
    PARAGRAPH_END = "</p>"
    IGNORE = ["https://thehackernews.uk"]
