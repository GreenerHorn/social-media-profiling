from Log import log
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import Utils

class Browser:
    """Browser is the class which handles
    all the operation related to Browser"""

    def __init__(self):
        try:
            ffprofile = webdriver.FirefoxProfile()
            ffprofile.set_preference("dom.webnotifications.enabled", False)
            self.browser = webdriver.Firefox(ffprofile)
            log('Browser created')
        except Exception as ex:
            self.browser = None
            log("Error due to ", str(ex))
        return

    def open_link(self, link):
        if Utils.is_empty_string(link):
            log("openLink Failed due to empty link address")
            return
        try:
            self.browser.get(link)
            log("Opened link : ", link)
        except Exception as ex:
            log("Failed due to ", str(ex))
        return

    def close_browser(self):
        if self.browser is None:
            log('Browser already closed or not created')
            return
        self.browser.quit()
        self.browser = None
        log('Browser closed')
        return

    def scroll(self, count=3):
        if self.browser is None:
            log('Browser already closed or not created')
            return
        try:
            elm = self.browser.find_element_by_tag_name('html')
            i = 0
            while i < count:
                elm.send_keys(Keys.END)
                Utils.random_wait()
                i = i + 1
            elm.send_keys(Keys.HOME)
            log('Scroll complete')
        except Exception as scrollEx:
            log('Failed scrolling due to ', str(scrollEx))
        return

    def scroll_end(self):
        try:
            # Get scroll height
            last_height = self.browser.execute_script("return document.body.scrollHeight")
            while True:
                elm = self.browser.find_element_by_tag_name('html')
                elm.send_keys(Keys.END)
                time.sleep(2)
                # Calculate new scroll height and compare with last scroll height
                new_height = self.browser.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            log("end of page")
        except Exception as ex:
            log("exception ",str(ex))
        return

if __name__ == '__main__':
    br = Browser()
    br.open_link("https://pythonspot.com/random-numbers/")
    Utils.random_wait()
    br.scroll_end()

    br.close_browser()

