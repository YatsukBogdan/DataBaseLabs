import lxml
from lxml.html import parse
from lxml import etree
from get_links import get_links

links = get_links()
data_root = etree.Element('data')

for link in links:
    page_branch = etree.SubElement(data_root, 'page', url=link)
    dom = parse(link).getroot()
    text_content_elements_p = dom.cssselect('p')
    for text_content_element_p in text_content_elements_p:
        fragment_text = etree.SubElement(page_branch, 'fragment', type='text')
        fragment_text.text = text_content_element_p.text_content()

    text_content_elements_a = dom.cssselect('a')
    for text_content_element_a in text_content_elements_a:
        fragment_text = etree.SubElement(page_branch, 'fragment', type='text')
        fragment_text.text = text_content_element_a.text_content()

    img_content_elements = dom.cssselect('img')
    for img_content_element in img_content_elements:
        fragment_image = etree.SubElement(page_branch, 'fragment', type='image')
        fragment_image.text = img_content_element.get('src')

tree = etree.ElementTree(data_root)
tree.write('result_site.xml', pretty_print=True, encoding='utf-8')

lxml_tree = lxml.etree.parse('result_site.xml')
hrefs = lxml_tree.xpath("./page/fragment[contains(text(), 'http')]")

for href in hrefs:
    print href.text

shop_url = "http://www.fishing-mart.com.ua/2-fishing-mart-spinningovaya-ribalka?n=20&id_category=2"
dom = parse(shop_url).getroot()
items = dom.cssselect("#product_list h3 a")

shop_root = etree.Element('shop')

for item in items:
    item_url = item.get('href')
    item_branch = etree.SubElement(shop_root, 'item', url=item_url)
    item_dom = parse(item_url).getroot()

    name = item.text_content()
    name_branch = etree.SubElement(item_branch, 'name')
    name_branch.text = name

    image_url = item_dom.cssselect("#primary_block #image-block img")[0].get('src')
    image_branch = etree.SubElement(item_branch, 'image')
    image_branch.text = image_url

    description_paragraphs = item_dom.cssselect(".rte p")
    description = ""
    for description_paragraph in description_paragraphs:
        description += description_paragraph.text_content() + "\n"
    description_branch = etree.SubElement(item_branch, 'description')
    description_branch.text = description

    price = item_dom.cssselect("#our_price_display")[0].text_content()
    price_branch = etree.SubElement(item_branch, 'price')
    price_branch.text = price

shop_tree = etree.ElementTree(shop_root)
shop_tree.write('result_shop.xml', pretty_print=True, encoding='utf-8')

dom_shop = etree.parse('result_shop.xml')
xslt = etree.parse('pattern.xsl')
transform = etree.XSLT(xslt)
new_shop_dom = transform(dom_shop)
new_shop_dom.write('result_shop.html', pretty_print=True, encoding='utf-8')
