import time

from bs4 import BeautifulSoup
import Log
import Browser,Utils,Constants,Details
from difflib import get_close_matches

class TwitterParser:
    twitter_base_url = "https://twitter.com/login?lang=en"
    twitter_import_url = "https://twitter.com/who_to_follow/matches"
    def __init__(self,browser,data):
        self.browser = browser
        self.data = data
        return
    def login(self):
        Log.log("twitter login intitiated")
        self.browser.open_link(TwitterParser.twitter_base_url)
        username = self.browser.browser.find_element_by_class_name("js-username-field")
        password = self.browser.browser.find_element_by_class_name("js-password-field")
        username.send_keys(Constants.TWITTER_ID)
        Utils.random_wait()
        password.send_keys(Constants.TWITTER_PASS)
        submit = self.browser.browser.find_element_by_css_selector("button.submit")
        Utils.random_wait()
        Utils.random_wait()
        submit.click()
        Log.log("twitter Login")
        return
    def import_following(self):
        Log.log("import following")
        self.browser.open_link(TwitterParser.twitter_import_url)
        Utils.random_wait()
        try:
            importButton = self.browser.browser.find_element_by_class_name("EdgeButton.EdgeButton--primary.action-btn.js-follow-all")
            if importButton is not None:
                importButton.click()
            Log.log("Import Successful")
        except Exception as e:
            Log.log("Excepetion Raised " + str(e))
        return
    def get_list(self):
        Log.log("getting list")
        self.import_following()
        self.browser.open_link("https://twitter.com/" + Constants.TWITTER_ID + "/following")
        Utils.random_wait()
        self.browser.scroll(4)
        time.sleep(6)
        Utils.random_wait()
        self.browser.scroll_end()
        page = BeautifulSoup(self.browser.browser.page_source, 'lxml')
        links = []
        name = []
        l = page.find_all('a', class_='fullname ProfileNameTruncated-link u-textInheritColor js-nav')
        for link in l:
            url = link.get('href')
            nam = link.text
            nam = nam.splitlines()

            if url and url not in links and '/' in url:
                links.append(url[1:])
                name.append(nam[1].strip().lower())
        Log.log("name:", name)
        Log.log("name count:",len(name))
        Log.log("links:", links)
        self.name_list = name
        self.links_list = links
        return
    def search(self):
        self.get_list()
        close_match = get_close_matches(self.data.name,self.name_list)
        matches_handle = []
        for e in close_match:
            matches_handle.append(self.links_list[self.name_list.index(e)])
        Log.log("close matches: ",close_match)
        self.data.twitter_id = matches_handle
        return

if __name__ == "__main__":
    br = Browser.Browser()
    data = Details.Detail()
    data.name = "vivek"
    twitter = TwitterParser(br,data)
    twitter.login()
    twitter.search()
    Log.log(data.__dict__)
