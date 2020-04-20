import mysql.connector as mc
import xml.etree.ElementTree as ET
from datetime import datetime

#parse temp Rss xml file
tree = ET.parse("nyt.xml")
root = tree.getroot()
ch = root.find('channel')

#connect to database
connection = mc.connect (host = "letkemann.ddns.net",
                        user = "mla",
                        passwd = "mla2020",
                        db = "news")
cursor = connection.cursor()

#get information from xml
for item in ch.findall('item'):
    title       = item.find('title').text
    link        = item.find('link').text
    description = item.find('description').text
    pubDate     = datetime.strptime(item.find('pubDate').text , '%a, %d %b %Y %H:%M:%S %z').strftime("%Y-%m-%d %H:%M:%S")
    categorys   = list()
    for category in item.findall('categroy'):
        categorys.append(category.text)

    #upload to Databank
    format_str = """INSERT INTO items (id, link, pubDate, description, category ) VALUES (0,'{l}','{date}','{d}','not Implemented yet');"""
    execute_str = format_str.format(l=link, date=pubDate, d = description)
    cursor.execute(execute_str)

connection.commit();

cursor.close()
connection.close()


