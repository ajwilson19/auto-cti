TYPE=""
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


def switch_cisa():
    global TYPE,ARTICLE_START,ARTICLE_END,LINK_START,LINK_END,LINK_PREPEND,LINK_STRIP_START,\
        LINK_STRIP_END,CONTENT_START,CONTENT_END,PARAGRAPH_END,PARAGRAPH_START
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

def switch_palo_alto():
    global TYPE, ARTICLE_START, ARTICLE_END, LINK_START, LINK_END, LINK_PREPEND, LINK_STRIP_START, \
        LINK_STRIP_END, CONTENT_START, CONTENT_END, PARAGRAPH_END, PARAGRAPH_START
    TYPE = "PaloAlto"
    ARTICLE_START = "<article"
    ARTICLE_END = "</article>"
    LINK_START = "<h3 class=\"h5 news__title mb-15\">"
    LINK_END = "</h3>"
    LINK_PREPEND = ""
    LINK_STRIP_START = "<h3 class=\"h5 news__title mb-15\"><a href=\""
    LINK_STRIP_END = "\" data-page-track="
    CONTENT_START = "<div class=\"article__content"
    CONTENT_END = "</article>"
    PARAGRAPH_START = "<p"
    PARAGRAPH_END = "</p>"
