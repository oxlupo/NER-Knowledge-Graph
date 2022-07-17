import requests
import pprint
from bs4 import BeautifulSoup as bs
def specifictag(url):
    """function for get only specific tag that exist in whitelist"""

    blacklist = ['input', 'u', 'body', 'html',
         'textarea', 'nobr', 'b', 'span', 'td', 'tr',
         'br', 'table', 'form', 'img', 'head', 'meta',
         'script', 'style', 'center', 'header', 'footer', 'div',]
    list_ = []
    soup = bs(requests.get(url=url, timeout=10, verify=False).text)
    s = " "
    # remove all blacklisted tags
    tags = [tag for tag in soup.find_all(True) if tag.name not in blacklist]

    # show tag tree after first extraction
    tag_tree = [(tag.name, [t.name for t in tag.findChildren()]) for tag in tags]

    # remove children tags that are blacklisted
    for tag in tags:
        for child in tag.findChildren():
            if child.name in blacklist:
                child.extract()
    for tag in tags:
        text = tag.text
        list_.append(text)

    with_out_header_footer = s.join(list_)
    # pprint.pprint(tags)
    return with_out_header_footer

def connection(url):
    """get text of a website with request library"""
    data = requests.get(url=url, verify=False, timeout=10).content
    soup = bs(data, "html.parser")
    soup = soup.text
    soup = soup.replace("\n", " ")
    return soup
