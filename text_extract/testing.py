# Imports
import requests
from bs4 import BeautifulSoup
from newspaper import Article

# URL input
url = 'https://www.lawenforcementtoday.com/michigan-prosecutor-reviewing-cases-90-convicted-murderers-serving-life-sentences/'

# Saving input
page = url
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

# Title
article_title = soup.find('title').get_text()

# Paragraphs / Text
paragraph_list = soup.find_all('p')
paragraph_text = ''
for paragraph in paragraph_list:
    paragraph_text = paragraph_text + '\n' + paragraph.get_text()

# Parsing and downloading
article = Article(url)
article.download()
article.parse()

# Author
article_author = str(article.authors)

# Date
article_published_date = str(article.publish_date)

# Keywords
article_keywords = str(article.keywords)


