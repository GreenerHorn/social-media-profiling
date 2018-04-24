import Constants
import Log, Utils
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from Browser import Browser


class FacebookParser:
    fb_base_url = "https://www.facebook.com/"
    def __init__(self,browser):
        self.browser = browser
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
        Log.log("Login complete")
        return

if __name__ =="__main__":
    br = Browser()
    fp = FacebookParser(br)
    fp.login()
    br.close_browser()