from Log import log
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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


if __name__ == '__main__':
	br = Browser()
	
