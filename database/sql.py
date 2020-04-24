import mysql.connector as mc
import xml.etree.ElementTree as ET
from datetime import datetime, tzinfo,  timezone

#parse temp Rss link
import requests
rss = requests.get("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml");

root = ET.fromstring(rss.content)
ch = root.find('channel')

#connect to database
connection = mc.connect (host = "letkemann.ddns.net",
                        user = "mla",
                        passwd = "mla2020",
                        db = "news")
cursor = connection.cursor()

#get last update
cursor.execute("SELECT lastUpdate FROM state;")
state = cursor.fetchone()
#should be only one item
for x in state:
    update = x.replace(tzinfo=timezone.utc)
#
link = ""
lastUpdate = datetime.min.replace(tzinfo=timezone.utc)
count = 0

#get information from xml
for item in ch.findall('item'):
    title       = item.find('title').text
    link        = item.find('link').text
    description = item.find('description').text
    pubDate     = datetime.strptime(item.find('pubDate').text , '%a, %d %b %Y %H:%M:%S %z').astimezone(tz=timezone.utc)
    if lastUpdate < pubDate:
        lastUpdate = pubDate

    if pubDate < update:
        print("contiue")
        continue
    pubDate_str = pubDate.strftime("%Y-%m-%d %H:%M:%S")
    categorys   = list()
    categorys_str= "";
    for category in item.findall('categroy'):
        categorys.append(category.text)
    for c in categorys:
        categorys_str = categorys_str + c + ", "

    #extract content with newspaper
    import trafilatura as traf
    #page = traf.fetch_url(link)
    #content_str = traf.extract(page)
    content_str = "tmp";

    #upload to Databank
    format_str = """INSERT INTO items (id, link, pubDate, description, category, content ) VALUES (0,'{l}','{date}','{d}','{c}','{content}');"""
    execute_str = format_str.format(l=link, date=pubDate_str, d = description, c = categorys_str, content = content_str)
    try:
        cursor.execute(execute_str)
        count = count + 1
    except:
        print(link)
        execute_str = execute_str = format_str.format(l=link, date=pubDate_str, d = description, c = categorys_str, content = "error in parsing")
        try:
            cursor.execute(execute_str)
            count = count +1
        except:
            print(link + "no chance")

#get prev items count
cursor.execute("SELECT items_count FROM state;")
state = cursor.fetchone()

for x in state:
    count = count + int(x);
#update state
cursor.execute("UPDATE state SET lastUpdate='" + lastUpdate.strftime("%Y-%m-%d %H:%M:%S") + "', items_count=" + str(count) + ";")

connection.commit();

cursor.close()
connection.close()



