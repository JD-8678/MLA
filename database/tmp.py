import xml.etree.ElementTree as ET
import sqlite3 as sql

tree = ET.parse("nyt.xml")
root = tree.getroot()
ch = root.find('channel')

print(root.tag)

for item in ch.findall('item'):
    title     = item.find('title').text
    link      = item.find('link').text
    pubDate   = item.find('pubDate').text
    categorys = list()
    for category in item.findall('categroy'):
        categorys.append(category.text)
    print(title)

