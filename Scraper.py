from Url_Parser import UrlParser
from Assistance_Program_DB import AssistanceProgramDB
import _thread, time, urllib
import urllib.request

"""
Web Scraping tool
"""
class Scraper:

    def __init__(self):
        self.url_parser=UrlParser()
        self.db_manager = AssistanceProgramDB()
        self.website = {}

    def get_html(self, url):
        """

        :param url: The given url to be accessed
        :return: The requested web content
        """
        try:
            self.website[url] = urllib.request.urlopen(url).read()
        except ValueError:  # in case there was a connection problem
            self.website[url] = None


    def get_multi_html(self, urls):
        """

        :param urls: urls to be loaded
        :return: None
        """
        if not urls:
            return [] # else program will stop
        for url in urls: _thread.start_new_thread(self.get_html, (url,))
        while len(self.website.keys()) != len(urls): time.sleep(0.1)

    def reset_website(self):
        """
        The function resets the class's dictionary object
        :return: None
        """
        self.website={}

    def check_for_update(self):
        """
        The function compares the DB entities alongside the web updated entities.
        If a change is detected the DB is updated.
        :return:
        """
        self.reset_website()
        urls = self.db_manager.retrieve_primary()
        urls = [url[0] for url in urls]
        db_entities = self.db_manager.retrieve(urls)
        self.get_multi_html(urls)
        entities = self.url_parser.parse_url(urls, self.website)
        updated_entities=[]
        n=len(db_entities)
        for i in range(n):
            if not entities[i]:
                continue
            elif db_entities[i].name != entities[i].name or db_entities[i].status != entities[i].status \
                or db_entities[i].eligible_treatments != entities[i].eligible_treatments or \
                db_entities[i].grant_amount != entities[i].grant_amount:
                updated_entities.append(entities[i])
        self.db_manager.write(updated_entities)

