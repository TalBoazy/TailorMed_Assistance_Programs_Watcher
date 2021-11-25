from Assistance_Program_DB import AssistanceProgramDB
from Url_Parser import UrlParser
from Scraper import Scraper
from Assistance_Program_Entity import AssistanceProgramEntity

"""
UI manager class.
"""


class UiManager:

    def __init__(self):
        self.db = AssistanceProgramDB()
        self.url_parser = UrlParser()
        self.scraper = Scraper()

    def show(self):
        """
        The function get called when the update button get pressed.
        :return: the updated database
        """
        self.scraper.check_for_update()
        return self.db.retrieve_table()

    def insert(self, url, name, eligible_treatments, status, grant_amount):
        """
        The function insert an entity to the DB
        :param url: string of length of 500 at most
        :param name: string of length of 250 at most
        :param eligible_treatments: string of length of 1000 at most
        :param status: "open"/"closed"
        :param grant_amount: int
        :return: None
        """
        obj = AssistanceProgramEntity(url, name, eligible_treatments, status, grant_amount)
        self.db.write([obj])

    def delete(self, url):
        """
        The function deletes the requested url from the table
        :param url: the url to be removed
        :return: None
        """
        self.db.delete([url])
