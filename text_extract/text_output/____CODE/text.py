url_list = [
            "https://www.nytimes.com/2020/03/16/world/middleeast/israel-coronavirus-cellphone-tracking.html",
            "https://www.bbc.com/news/world-europe-51918596",
            "https://www.theguardian.com/uk-news/2020/mar/18/london-coronavirus-lockdown-tougher-measures",
            "https://www.lawenforcementtoday.com/michigan-prosecutor-reviewing-cases-90-convicted-murderers-serving-life-sentences/",
            "https://abcnews.go.com/US/police-implement-sweeping-policy-prepare-coronavirus-spread/story?id=69672368&cid=clicksource_4380645_2_heads_hero_live_headlines_hed",
            "https://www.nbcnews.com/news/us-news/trump-says-hospital-ships-heading-coronavirus-battle-navy-says-they-n1163081",
            "https://www.whitehouse.gov/briefings-statements/remarks-president-trump-vice-president-pence-members-coronavirus-task-force-press-conference-3/"
            ]

# lawenforcementtoday does not work with boilerpipe
# New York Times does not properly work with newspaper

#set path for output folder
# path = ..........


for i in range (len(url_list)):
    url = url_list[i]
    import tldextract

    ext = tldextract.extract(url)
    output_path = (path + ext.domain +"/")
    import os

    if not os.path.exists(output_path):
        os.mkdir(output_path)


    import requests

    r = requests.get(url)

    with open(output_path + "source.html", 'wb') as f:
        f.write(r.content)


    import requests
    from readability import Document

    response = requests.get(url)
    page = Document(response.text)
    html = page.summary()

    file = open(output_path + "readability_html.html", "w")
    file.write(html)
    file.close()

    from newspaper import Article

    page = Article(url)
    page.download()
    page.parse()

    file = open(output_path + "newspaper_url.txt", "w")
    file.write(page.text)
    file.close()


    from newspaper import fulltext
    import requests

    page = requests.get(url).text
    content = fulltext(page)

    file = open(output_path + "newspaper_url_other.txt", "w")
    file.write(content)
    file.close()


    from newspaper import fulltext
    import requests

    page = html
    content = fulltext(page)

    file = open(output_path + "newspaper_readability_html.txt", "w")
    file.write(content)
    file.close()


    from goose3 import Goose

    g = Goose()
    page = g.extract(url=url)


    file = open(output_path + "goose_url.txt", "w")
    file.write(page.cleaned_text)
    file.close()


    from goose3 import Goose

    g = Goose()
    page = g.extract(raw_html=html)

    file = open(r"D:\Benutzer\Popik\Desktop\MLA\test\goose_readability_html.txt", "w")
    file.write(page.cleaned_text)
    file.close()


    import html2text
    h = html2text.HTML2Text()
    h.ignore_links = True

    file = open(output_path + "html2text_readability_html.txt", "w")
    file.write(h.handle(html))
    file.close()

    if not (ext.domain == "lawenforcementtoday"):
        from boilerpy3 import extractors

        extractor = extractors.DefaultExtractor()

        content = extractor.get_content_from_url(url)

        file = open(output_path + "boilerpipe_url.txt", "w")
        file.write(content)
        file.close()

    import trafilatura

    downloaded = trafilatura.fetch_url(url)
    extracted = trafilatura.extract(downloaded)

    file = open(output_path + "trafilatura.txt", "w")
    file.write(extracted)
    file.close()

    page = html
    extracted = trafilatura.extract(page)
    file = open(output_path + "trafilatura_readability.txt", "w")
    file.write(extracted)
    file.close()

    import requests
    from bs4 import BeautifulSoup
    from newspaper import Article

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    paragraph_list = soup.find_all('p')
    paragraph_text = ''
    for paragraph in paragraph_list:
        paragraph_text = paragraph_text + '\n' + paragraph.get_text()

    file = open(output_path + "soup.txt", "w")
    file.write(paragraph_text)
    file.close()

    ####
    page = html
    soup = BeautifulSoup(page.content, 'html.parser')

    paragraph_list = soup.find_all('p')
    paragraph_text = ''
    for paragraph in paragraph_list:
        paragraph_text = paragraph_text + '\n' + paragraph.get_text()

    file = open(output_path + "soup_readability.txt", "w")
    file.write(paragraph_text)
    file.close()