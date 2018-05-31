import json

import Browser
import DatabaseHandler
import Log

from Facebook import FacebookParser
from LinkedIn import LinkedInParser
from Twitter import TwitterParser
from Details import Detail

class Parser:
    @staticmethod
    def parse(name,email,phone):
        data = Detail()
        data.phoneno = phone
        data.name = name
        data.email = email

        browser = Browser.Browser()

        fb_parser = FacebookParser(browser,data)
        fb_parser.login()
        fb_parser.search()

        Log.log(data.__dict__)

        tw_parser = TwitterParser(browser,data)
        tw_parser.login()
        tw_parser.search()

        Log.log(data.__dict__)

        ld_parser= LinkedInParser(browser,data)
        ld_parser.login()
        ld_parser.search()
        browser.close_browser()
        DatabaseHandler.DataBaseHandler().insert_from_details(data)
        Log.log(data.__dict__)
        return data.__dict__

if __name__ == "__main__":
    Parser.parse("Vivek Kundariya","vivekkundariya@gmail.com","Vivek Kundariya")
