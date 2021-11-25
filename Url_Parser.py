from bs4 import BeautifulSoup
from Assistance_Program_Entity import AssistanceProgramEntity

"""
The url Parser Class
"""
class UrlParser:

    def get_html_text(self, html):
        """
        Given an html file content, the function retrieves the text values in the given page
        :param html: The given html
        :return: The text values in the given page
        """
        if not html:
            return None  # in case there was a problem with loading
        soup = BeautifulSoup(html)
        for script in soup(["script", "style"]):
            script.decompose()
        return list(soup.stripped_strings)

    def parse_url(self, urls, website):
        """

        :param urls: The given urls to scrape
        :param website: Mapping tool for url and html content
        :return: AssistanceProgramEntity list of the required url keys.
        """
        entities = []
        #self.get_multi_html(urls)
        for url in urls:
            strips = self.get_html_text(website[url])
            if not strips:
                entities.append(None)
                continue
            name = self.get_org_name(strips)
            status = self.get_status(strips)
            max_fund = self.get_max_fund(strips)
            treatments = self.get_treatments(strips)
            if name is None or status is None or max_fund is None or treatments is None:
                # wrong html file format
                continue
            entities.append(AssistanceProgramEntity(url, name, treatments, status, max_fund))
        return entities

    def get_org_name(self, strips):
        """

        :param strips: html text context
        :return: The Organization name
        """
        if not len(strips):
            return None
        return strips[0]

    def get_index(self, val, strips):
        """

        :param val: The required value
        :param strips: html text context
        :return: The requested index or None if val is not in strips
        """
        index=None
        try:
            index=strips.index(val)
        except ValueError:
            print(f'HTML file in wrong format')
        return index

    def get_status(self, strips):
        """

        :param strips: html text context
        :return: The organization status
        """
        index = self.get_index("Status", strips)
        if index is None:
            return
        if strips[index + 1][:4] == "Open":
            return "Open"
        return "Closed"

    def get_max_fund(self, strips):
        """

        :param strips: html text context
        :return: The organization max fund
        """
        index=self.get_index("Maximum Award Level", strips)
        if index is None:
            return
        return int(strips[index + 1][1:].replace(",", ""))

    def get_treatments(self, strips):
        """

        :param strips: html text context
        :return: The organization available treatments
        """
        end = self.get_index("Fund Definition", strips)
        if end is None:
            return
        if "Treatments Covered" in strips:
            start = self.get_index("Treatments Covered", strips)
        else:
            start = self.get_index("Medications Covered", strips)
            if start is None:
                return
        return ",".join(str(cond) for cond in strips[start + 1:end])[:1000]
