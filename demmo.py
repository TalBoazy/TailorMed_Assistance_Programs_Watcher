from Assistance_Program_DB import AssistanceProgramDB
from Url_Parser import UrlParser
from Scraper import Scraper
from UI_Interface import UI

"""
demmo file
"""
class Demmo:
    def __init__(self):
        self.db = AssistanceProgramDB()
        self.url_parser = UrlParser()
        self.scraper = Scraper()
        self.ui_manager = UI()
        self.urls = ["https://www.healthwellfoundation.org/fund/acute-myeloid-leukemia-medicare-access/",
                                "https://www.healthwellfoundation.org/fund/amyotrophic-lateral-sclerosis/",
                                "https://www.healthwellfoundation.org/fund/cancer-related-behavioral-health/",
                                "https://www.healthwellfoundation.org/fund/chronic-lymphocytic-leukemia-medicare-access/",
                                "https://www.healthwellfoundation.org/fund/congenital-sucrase-isomaltase-deficiency/"]
        self.run()

    def init_table(self):
        """
        initiate the SQL DB
        """
        self.db.create_the_table()

    def insert_values(self):
        """
        inserts 5 assistance programs from the website
        """
        self.scraper.get_multi_html(self.urls)
        htmls = self.scraper.website
        objs = self.url_parser.parse_url(self.urls,htmls)
        self.db.write(objs)

    def run(self):
        """
        initialize all values and presents the table
        """
        self.init_table()
        self.insert_values()
        self.ui_manager.present_table()


if __name__ == "__main__":
    run = Demmo()