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
IGNORE=""


def switch_cisa():
    global TYPE,ARTICLE_START,ARTICLE_END,LINK_START,LINK_END,LINK_PREPEND,LINK_STRIP_START,\
        LINK_STRIP_END,CONTENT_START,CONTENT_END,PARAGRAPH_END,PARAGRAPH_START,SPLICE
    TYPE="CISA"
    ARTICLE_START = "<div  class=\"c-view__row\">"
    ARTICLE_END = "</article>"
    SPLICE=""
    LINK_START = "<a href=\""
    LINK_END = "</a>"
    LINK_PREPEND = "https://www.cisa.gov"
    LINK_STRIP_START = "<a href=\""
    LINK_STRIP_END = "\" "
    CONTENT_START = "<main id=\"main"
    CONTENT_END = "<div class=\"l-constrain l-page-section--rich-text\">"
    PARAGRAPH_START = "<h1 class=\"c-page-title__title\">"
    PARAGRAPH_END = "<div class=\"l-constrain l-page-section--rich-text\">"

def switch_palo_alto():
    global TYPE, ARTICLE_START, ARTICLE_END, LINK_START, LINK_END, LINK_PREPEND, LINK_STRIP_START, \
        LINK_STRIP_END, CONTENT_START, CONTENT_END, PARAGRAPH_END, PARAGRAPH_START, SPLICE
    TYPE = "PaloAlto"
    ARTICLE_START = "<article"
    ARTICLE_END = "</article>"
    SPLICE=""
    LINK_START = "<h3 class=\"h5 news__title mb-15\">"
    LINK_END = "</h3>"
    LINK_PREPEND = ""
    LINK_STRIP_START = "<h3 class=\"h5 news__title mb-15\"><a href=\""
    LINK_STRIP_END = "\" data-page-track="
    CONTENT_START = "<div class=\"article__content"
    CONTENT_END = "</article>"
    PARAGRAPH_START = "<p"
    PARAGRAPH_END = "</p>"

def switch_bleeping_computer():
    global TYPE, ARTICLE_START, ARTICLE_END, LINK_START, LINK_END, LINK_PREPEND, LINK_STRIP_START, \
        LINK_STRIP_END, CONTENT_START, CONTENT_END, PARAGRAPH_END, PARAGRAPH_START, SPLICE, IGNORE
    TYPE = "BleepingComputer"
    SPLICE = "<ul id=\"bc-home-news-main-wrap\""
    ARTICLE_START = "<li"
    ARTICLE_END = "</ul></div>"
    LINK_START = "<h4><a href"
    LINK_END = "</a></h4>"
    LINK_PREPEND = ""
    LINK_STRIP_START = "<h4><a href=\""
    LINK_STRIP_END = "\">"
    CONTENT_START = "<article"
    CONTENT_END = "<div class=\"cz-related-article-wrapp"
    PARAGRAPH_START = "<p"
    PARAGRAPH_END = "</p>"
    IGNORE = "/deals/"

def switch_talos():
    global TYPE, ARTICLE_START, ARTICLE_END, LINK_START, LINK_END, LINK_PREPEND, LINK_STRIP_START, \
        LINK_STRIP_END, CONTENT_START, CONTENT_END, PARAGRAPH_END, PARAGRAPH_START, SPLICE, IGNORE
    TYPE = "Talos"
    SPLICE = ""
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

def switch_hacker_news():
    global TYPE, ARTICLE_START, ARTICLE_END, LINK_START, LINK_END, LINK_PREPEND, LINK_STRIP_START, \
        LINK_STRIP_END, CONTENT_START, CONTENT_END, PARAGRAPH_END, PARAGRAPH_START, SPLICE, IGNORE
    TYPE = "HackerNews"
    SPLICE = "<div class=\'body-post"
    ARTICLE_START = "<a class=\'story-link"
    ARTICLE_END = "</a>"
    LINK_START = "<a class=\'story-link"
    LINK_END = "</div>"
    LINK_PREPEND = ""
    LINK_STRIP_START = "href="
    LINK_STRIP_END = ">"
    CONTENT_START = "<main class="
    CONTENT_END = "</main>"
    PARAGRAPH_START = "<p"
    PARAGRAPH_END = "</p>"
    IGNORE = "https://thehackernews.uk"
