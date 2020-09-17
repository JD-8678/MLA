import trafilatura
from newsplease import NewsPlease
url = 'https://www.floridadems.org/2019/06/17/ahead-of-trumps-relaunch-fdp-highlights-how-trump-abandoned-workers/'

website = trafilatura.fetch_url(url)
fulltext = trafilatura.extract(website)

news = NewsPlease.from_url(url)
# print(news.maintext)
print(fulltext)