""" HackMTY """

import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, KeywordsOptions
from bs4 import BeautifulSoup
import urllib.request as urllib2


class GoogleResult:
    """ Google Search Results """
    def __init__(self, title, text, link):
        self.link = link
        self.title = title
        self.text = text


class GoogleSearch:

    def __init__(self):
        self.USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ 58.0.3029.81 Safari/537.36"
        self.SEARCH_URL = "https://google.com/search"
        self.RESULT_SELECTOR = ".srg h3.r a"
        self.TOTAL_SELECTOR = "#resultStats"
        self.RESULTS_PER_PAGE = 10
        self.DEFAULT_HEADERS = [
                ('User-Agent', self.USER_AGENT),
                ("Accept-Language", "en-US,en;q=0.5"),
            ]

    def search(self, query):
        """ Search in Google Scrapper """
        opener = urllib2.build_opener()
        opener.addheaders = self.DEFAULT_HEADERS
        response = opener.open(self.SEARCH_URL + "?q="+ urllib2.quote(query) + "&hl=" + "en")
        opener.close()

        mybytes = response.read()
        mystr = mybytes.decode("utf8")
        soup = BeautifulSoup(mystr, "html.parser")

        for div in soup.find_all("div", {"class": "g"}):
            div_link = div.find("h3", {"class": "r"})
            div_text = div.find("span", {"class": "st"})
            if div_link != None and div_text != None:
                link = div_link.a["href"]
                title = div_link.text
                text = div_text.text
                yield GoogleResult(title, text, link)


class Watson:

    def __init__(self):
        """ Watson Credentials """
        self.natural_language_understanding = NaturalLanguageUnderstandingV1(
            username='397f0adc-7d87-4b03-8a9a-c67300d468ed',
            password='A8DmyOcAqfSE',
            version="2018-03-16")

    def natural_language(self, text):
        """ Natural Language Proccessing """
        response = self.natural_language_understanding.analyze(
            text=text,
            features=Features(
                keywords=KeywordsOptions(
                    sentiment=False,
                    emotion=False,
                    limit=2)))
        for key in response.get("keywords", []):
            print(key.get("text", ""))
            yield key.get("text", "")


def search(text):
    google = GoogleSearch()
    watson = Watson()
    # Get all the concepts in the text
    results = []
    for concept in watson.natural_language(text):
        # Search in Google
        for result in google.search(concept):
            actual = {"title": result.title,"text": result.text,"link": result.link}
            results.append(actual)
    return results
