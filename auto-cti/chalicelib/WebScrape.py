"""
* Author: Dbog
* Date: 4/21/2024
* Description: Blah blah blah, Im the best fucking coder, Blah Blah Blah
"""

import re
from urllib.request import Request, urlopen
from chalicelib import config as config

"""
###########################################################################
#
# Article Page Scraping Functions
# Description:
#       Functions built to parse links of article hubs to get the links  
#           for every recent article. no pagination changes built in to
#           ensure only most recent articles are grabbed
#
###########################################################################
"""

"""
    Initiates the scraping of a article hub link. It starts by utilizing the switch method
        to switch the configuration to the right type of link then opens the link and
        initiates teh scraping to get the article links.
        
    Input: Article Hub Link
    Output: A List of each Article Link on the Artcile Hub
"""
def scrape_link(link) -> list:
    config.switch(link)
    page = url_open(link)
    articles = get_article_links(page) #ARTICLE LINKS!!!!
    return articles

"""
    Takes the page of the article hub and using the configuration global variables
        parses the links out of the article pop ups to get all the links. It starts by splicing to 
        ignore the earlier HTML, then parses each paragraph using the ARTICLE_START and ARTICLE_END 
        config global variables. Within this function the check_ignore() function is called to ensure 
        that ignored links do not make it through to the next stage. Ignored links would be like 
        Advertisement Links, Deal Links, or Sponsored Links to ensure we get the best results
            
    Input: Main Page in HTML of the Article Hub
    Output: Every Valuable Article Link on the page
"""
def get_article_links(page) -> list:
    html = page.read().decode("utf-8")
    articles_left = True
    articles = []

    html = html[html.find(config.SPLICE):]

    while articles_left:
        # sidx = Start Index
        # eidx = End Index
        sidx = html.find(config.ARTICLE_START)
        eidx = html.find(config.ARTICLE_END) + len(config.ARTICLE_END)

        article = html[sidx:eidx]

        if article != "": # YIPEEEEE
            articles.append(article[article.find(config.LINK_START):article.find(config.LINK_END)])
        else:
            articles_left = False

        html = html[eidx:]

    links = []

    for article in articles:
        link = format_article_string(article)

        if not check_ignore(link):
            links.append(link)

    return links

"""
    Formats the article string to strip off any remaining HTML that may have occured from the earlier parsing
        then for some sites, the article strings parsed are only the end and need the website title prepended.
        These links are then sent through a final cleaning in the format_link() function.
        
    Input: Unformated dirty article string
    Output: Clean Article String for next stage
"""
def format_article_string(article_string) -> 'Formatted Article Link':
    # sidx = Start Index
    # eidx = End Index
    sidx = article_string.find(config.LINK_STRIP_START) + len(config.LINK_STRIP_START)
    eidx = article_string.find(config.LINK_STRIP_END)

    return format_link(config.LINK_PREPEND + article_string[sidx:eidx])

"""
###########################################################################
#
# Single Article Scraping Functions
# Description:
#
###########################################################################
"""

"""
    Gets a list of all of the articles from a list of links from the main article hub     
    Input: 
    Output: 
"""
def get_formatted_articles(links) -> 'Formatted Article Link':
    formatted = []
    for link in links:
        try:
            formatted.append([link, scrape_article(link)])
        except:
            print("Error on Link:",link)
    return formatted

"""
    
    Input:
    Output:
"""
def scrape_article(article_link):
    config.switch(article_link)
    article = url_open(article_link)
    return read_article(article)

"""

    Input:
    Output:
"""
def read_article(article) -> 'Full Article':
    html = article.read().decode("utf-8")
    html = html[html.find(config.CONTENT_START):html.find(config.CONTENT_END) + len(config.CONTENT_END)]
    p_left = True
    paragraphs = []
    html = html[html.find(config.CONTENT_START):]
    while p_left:
        # sidx = Start Index
        # eidx = End Index
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


"""
###########################################################################
#
# Scraping Helper Functions
# Description:
#   Helper functions built out to assist in the scraping of article hubs and
#       General articles. 
#
###########################################################################
"""

"""
    Utilizing the urlopen() function from the urllib library, we open a link with a request
        built to look like a user agent instead of a program. Some of the articles we encountered
        had small anti-webscraping countermeasures, this gets passed some of the easy ones. 
        
    IMPORTANT NOTE: 
        This is only for the very simple countermeasures. Sites like Talos Intelligence
            have much more advanced countermeasures, but the scraping is already built out for
            it if this is built out more to get past those counter measures - Dbog
    
    Input: Link to open
    Output: Raw HTML Page of the link
"""
def url_open(link) -> 'HTML Page':
    req = Request(
        url=link,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    page = urlopen(req)
    return page

"""
    Scrapes the article title from the given link. this article title does still have the dashes
        in it and it is not perfectly formatted. More prominent usage in testing. Gets the values
        after the last dash
        
    Input: Link with the title desired.
    Output: 
"""
def scrape_article_title(link) -> 'Parsed Link':
    parsed = link.split("/")
    if parsed[-1] == '':
        return parsed[-2]
    return parsed[-1]

"""
    Checks if the current link needs to be ignored or not. Configuration global variable
        IGNORE is a list of links that need to be ignored in the event that there are multiple
        
    Input: Link to be checked
    Output: Boolean on if the link needs to be ignored(True) or not(False)
"""
def check_ignore(link) -> bool:
    # If its None it means no ignores have been defined
    if config.IGNORE is not None:
        # IGNORE is the only config variable that is a list, for multiple ignores
        for IGNORE in config.IGNORE:
            if link.__contains__(IGNORE):
                return True
    return False

"""
    Removes all HTML statements that may have gotten through in paragraphs that are 
        parsed from the web page. Uses a regex to remove everything between <> brackets. 
        WARNING: Will not remove HTML that have either bracket cut off. 
        
    Input: A parsed paragraph from a Web Page with possible HTML
    Output: A cleaned paragraph with no HTML left
"""
def remove_html(paragraph) -> 'Clean Paragraph':
    new_paragraph = re.sub(re.compile('<.*?>'), '', paragraph)
    return new_paragraph


"""
    Formats a given link to remove any extrenuous quotation marks that make
        it through the earlier parser functions
        
    Input: Link with possible issues
    Output: A clean link ready to parse
"""
def format_link(link) -> 'Clean Link':
    if link.__contains__("\""):
        return link.strip("\"")
    elif link.__contains__("\'"):
        return link.strip("\'")
    return link
