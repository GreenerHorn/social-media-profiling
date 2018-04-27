from bs4 import BeautifulSoup

import Constants
import Log, Utils
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from Browser import Browser
from Details import Detail


class FacebookParser:
    fb_base_url = "https://www.facebook.com"
    fb_query_search_url = fb_base_url+"/search/people/?q="
    def __init__(self,browser):
        self.browser = browser
        self.data = Detail()
        return

    def login(self):
        self.browser.open_link(FacebookParser.fb_base_url)
        br = self.browser.browser
        br.get("https://facebook.com")
        Utils.random_wait()
        emailElement = br.find_element_by_id('email')
        emailElement.send_keys(Constants.FB_ID)
        passElement = br.find_element_by_id('pass')
        passElement.send_keys(Constants.FB_PASS)
        subElement = br.find_element_by_id("loginbutton")
        Utils.random_wait()
        subElement.submit()
        Utils.random_wait()
        Utils.random_wait()
        Utils.random_wait()
        Log.log("Login complete")
        return

    def __get_people_links(self, page):
        links = []
        l = page.find_all('a')
        for link in l:
            url = link.get('href')
            lis = link.get('data-testid')
            if url and lis:
                url = url.replace('?ref=br_rs', '')
                url = url.replace('&ref=br_rs', '')
                if url not in links and 'serp_result_link' in lis and 'EntRegularPersonalUser' in lis and 'https://www.facebook.com/' in url:
                    links.append(url)
                    Log.log("id fetched : ",url)
        return links

    def __search(self,search_item):
        search_url = FacebookParser.fb_query_search_url+Utils.url_encode(search_item)
        Log.log("search_url",search_url)
        self.browser.open_link(search_url)
        Utils.random_wait()
        page = BeautifulSoup(self.browser.browser.page_source, 'lxml')
        links = self.__get_people_links(page)
        Log.log(links)
        if len(links)>0:
            self.data.fb_url = links[0]
            self.data.fb_possible_ids = links
            return True
        return False

    def __find_all_details(self):
        Log.log("")
        pass
    def search(self,email,phone,name):
        self.data.phoneno = phone
        self.data.name = name
        self.data.email = email
        if self.__search(phone) == True or self.__search(email) == True or self.__search(name) == True:
            self.__find_all_details()
        return



if __name__ =="__main__":
    br = Browser()
    fp = FacebookParser(br)
    fp.login()
    fp.search("","","Vivek Kundariya")
    Log.log(fp.data.__dict__)
    br.close_browser()