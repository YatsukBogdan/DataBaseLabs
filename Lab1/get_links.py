from lxml.html import parse


def get_links():
    links = ['http://www.ostriv.in.ua/']
    i = 0
    while len(links) <= 20:
        dom = parse(links[i]).getroot()
        domain = 'ostriv.in.ua'
        new_links = dom.cssselect('a')
        for new_link in new_links:
            new_link_url = new_link.get('href')
            if new_link_url not in links and new_link_url.find(domain) != -1 and new_link_url.find('http') != -1:
                links.append(new_link_url)
        i += 1
    return links
