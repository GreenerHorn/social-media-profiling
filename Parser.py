import json
from threading import Thread
from time import gmtime, strftime
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
        Log.log(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        browser = Browser.Browser()

        fb_parser = FacebookParser(browser,data)
        fb_parser.login()
        status = fb_parser.search()
        like_thread = None
        if(status ==True):
            fb_parser.get_likes()
            like_thread = Thread(target=lambda: fb_parser.get_likes_movies(data.fb_likes))
            like_thread.start()
            fb_parser.get_overview()

        Log.log(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        Log.log(data.__dict__)

        tw_parser = TwitterParser(browser,data)
        tw_parser.login()
        tw_parser.search()

        Log.log(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        Log.log(data.__dict__)

        ld_parser= LinkedInParser(browser,data)
        ld_parser.login()
        ld_parser.search()
        browser.close_browser()
        if(like_thread is not None):
            like_thread.join()
        if data.email != "vivekkundariya1996@gmail.com":
            DatabaseHandler.DataBaseHandler().insert_from_details(data)
        Log.log(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        Log.log(data.__dict__)
        return data.__dict__

if __name__ == "__main__":
    Parser.parse("Vivek Kundariya","vivekkundariya@gmail.com","Vivek Kundariya")
