from bs4 import BeautifulSoup

import Browser
import Constants
import Details
import Log
import Utils
from difflib import get_close_matches


def find_best_url(titles_urls, name):
    titles1 = titles_urls[0]
    links1 = titles_urls[1]
    titles2 = []
    Log.log(links1, titles1)
    if titles1 == []:
        return []
    elif len(titles1) == 1:
        best_match = links1
    else:
        for i in titles1:
            titles2.append(i.split('|')[0].split('-')[0])
        Log.log(titles2)
        best_match = get_close_matches(name, titles2)
        best_link = []
        for ea in best_match:
            best_link.append(links1[titles2.index(ea)])
        best_match = [best_match, best_link]
    return best_match


class LinkedInParser:
    linkedin_base_url = "https://linkedin.com/"
    linkedin_search_url = "https://www.google.co.in/search?q=site:linkedin.com"

    def __init__(self, browser, data):
        self.browser = browser
        self.data = data
        return

    def login(self):
        try:
            self.browser.open_link(LinkedInParser.linkedin_base_url)
            emailElement = self.browser.browser.find_element_by_id("login-email")
            emailElement.send_keys(Constants.LINKEDIN_ID)
            passwordElement = self.browser.browser.find_element_by_id("login-password")
            passwordElement.send_keys(Constants.LINKEDIN_PASS)
            passwordElement.submit()
            Utils.random_wait()
            Log.log("linkedin login success")
        except Exception as e:
            Log.log("linkedin login failed" + str(e))
        return

    def __email_process(self, email):
        commonEmails = ['gmail', 'ymail', 'yahoo', 'rediff', 'outlook', 'icloud', 'inbox', 'rediffmail', 'live']
        domain = email.split("@")[1]
        domain = domain.split(".")[0].lower()
        Log.log("domain ", domain)
        if domain not in commonEmails:
            return domain
        return None

    def __search(self, name, context):
        link_list = []
        name_list = []
        for search in context:
            url_linkedin = LinkedInParser.linkedin_search_url + " " + name + " " + search
            self.browser.open_link(url_linkedin)
            Utils.random_wait()
            page = BeautifulSoup(self.browser.browser.page_source, 'lxml')
            elements_links = page.select('div.g cite')
            elements_titles = page.select('h3.r')
            titles = []
            links = []
            for ele in range(0, len(elements_titles)):
                if "linkedin.com/in/" in elements_links[ele].get_text():
                    titles.append(elements_titles[ele].a.text.lower())
                    links.append(elements_links[ele].get_text().lower())
            result = [titles, links]
            result = find_best_url(result, name)
            link_list += result[1]
            name_list += result[0]
            Log.log(result)
        self.data.linkedin_id = list(set(link_list))
        return

    def search(self):
        context = []
        Log.log("linkedin search initiated")
        domain = self.__email_process(self.data.email)
        if domain is not None:
            context.append(domain)

        if Utils.is_empty_string(self.data.works) == False:
            context.append(self.data.works)

        if Utils.is_empty_string(self.data.studies) == False:
            context.append(self.data.studies)

        if Utils.is_empty_string(self.data.studied) == False:
            context.append(self.data.studied)

        if Utils.is_empty_string(self.data.lives) == False:
            context.append(self.data.lives)

        if Utils.is_empty_string(self.data.home) == False:
            context.append(self.data.home)

        Log.log("context to be search are ", context)
        self.__search(self.data.name, context)


if __name__ == "__main__":
    br = Browser.Browser()
    data = Details.Detail()
    data.name = "Vivek Kundariya"
    data.email = "vivekkundariya1996@gmail.com"
    data.studies = "army institute of technlogy,pune"
    ld = LinkedInParser(br, data)
    ld.login()
    ld.search()
