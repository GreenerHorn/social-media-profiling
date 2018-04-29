from bs4 import BeautifulSoup
import Constants
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from Browser import Browser
from Details import Detail
import Log, Utils


class FacebookParser:
    fb_base_url = "https://www.facebook.com"
    fb_query_search_url = fb_base_url + "/search/people/?q="

    def __init__(self, browser):
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
                url = url.split('_')[0]
                if url not in links and 'serp_result_link' in lis and 'EntRegularPersonalUser' in lis and 'https://www.facebook.com/' in url:
                    links.append(url)
                    Log.log("id fetched : ", url)
        return links

    def __search(self, search_item):
        search_url = FacebookParser.fb_query_search_url + Utils.url_encode(search_item)
        Log.log("search_url", search_url)
        self.browser.open_link(search_url)
        Utils.random_wait()
        page = BeautifulSoup(self.browser.browser.page_source, 'lxml')
        links = self.__get_people_links(page)
        Log.log(links)
        if len(links) > 0:
            self.data.fb_url = links[0]
            self.data.fb_possible_ids = links
            return True
        return False

    def __get_overview(self):
        self.browser.open_link(self.data.fb_url + '/about?section=overview')
        self.browser.scroll()
        Utils.random_wait()
        page = BeautifulSoup(self.browser.browser.page_source, 'lxml')
        self.__get_profile_pic(page)
        self.__get_friends_list(page)
        try:
            overview = page.find_all('div', {'class': '_c24 _50f4'})
            for over in overview:
                inner_text = over.text
                strWithNewLine = [s.strip() for s in inner_text.splitlines()]
                for string in strWithNewLine:
                    string = Utils.remove_non_ascii(string)
                    string = string.lower()
                    if 'works' in string:
                        self.data.works = string.replace('works', '')
                    elif 'studies' in string:
                        self.data.studies = string.replace('studies', '')
                    elif 'studied' in string:
                        self.data.studied = string.replace('studied', '')
                    elif 'lives' in string:
                        self.data.lives = string.replace('lives', '')
                    elif 'from' in string:
                        self.data.home = string.replace('from', '')

            Log.log("overview done")
        except Exception as ex:
            Log.log('[-] overview ' + str(ex))
        return

    def __get_profile_pic(self, page):
        Log.log("")
        try:
            elements = page.find('img', {'class': '_11kf img'})
            # Log.log(elements)
            inner_text = elements.get('src')
            Log.log(inner_text)
            strWithNewLine = [s.strip() for s in inner_text.splitlines()]
            for i in strWithNewLine:
                if Utils.is_empty_string(i) == False:
                    self.data.fb_profilephoto = i;
                    Log.log('Profile Pic available ', i)
                    return
        except Exception as e:
            Log.log(str(e), ' failed in getImage (Profile Pic Not available) ')
        return

    def __get_friends_list(self, page):
        friend_list = []
        friend_list_html = page.find_all("div", {"class": "clearfix _5qo4"})
        for friend in friend_list_html:
            img_name_tag = friend.find("img")
            url_tag = friend.find("a")
            name = ""
            image = ""
            url =""
            if url_tag and url_tag.get("href"):
                url = url_tag.get("href")
            if img_name_tag and img_name_tag.get("src"):
                image = img_name_tag.get("src")
            if img_name_tag and img_name_tag.get("aria-label"):
                name = img_name_tag.get("aria-label")
            friend_list.append(name)
            friend_list.append(image)
            friend_list.append(url)

            Log.log(name , " " , url , " " , image)
        self.data.fb_friend = friend_list
        Log.log("Friend list complete")
        return

    def __get_likes(self):
        self.browser.open_link(self.data.fb_url+"/likes_all")
        Utils.random_wait()
        self.browser.scroll_end()
        Utils.random_wait()
        page = BeautifulSoup(self.browser.browser.page_source,"lxml")
        likes_all = page.find_all("div",{"class":"_6a _6b"})
        Log.log("likes_all count ",len(likes_all))
        like_list = []
        insights = []
        for like in likes_all:
            like_text_tag = like.find("div",{"class":"fsl fwb fcb"})
            like_type_tag = like.find("div",{"class":"fsm fwn fcg"})
            if like_text_tag is not None and like_type_tag is not None:
                like_text = like_text_tag.text
                like_type = like_type_tag.text
                Log.log(like_type," ",like_text)
                like_list.append(like_text)
                if like_type not in insights:
                    insights.append(like_type)
                    insights.append(1)
                else:
                    index = insights.index(like_type)
                    insights[index+1] += 1
        self.data.fb_likes = like_list
        self.data.fb_likes_insights = insights
        Log.log("insights ", insights)
        Log.log("total number of like_list ", len(like_list)," like_list ", like_list)
        return

    def __find_all_details(self):
        Log.log("finding details")
        self.__get_overview()
        self.__get_likes()
        Log.log("data ", self.data.__dict__)
        return

    def search(self, email, phone, name):
        self.data.phoneno = phone
        self.data.name = name
        self.data.email = email
        if self.__search(phone) == True or self.__search(email) == True or self.__search(name) == True:
            self.__find_all_details()
        return


if __name__ == "__main__":
    br = Browser()
    fp = FacebookParser(br)
    fp.login()
    fp.search("Reshav Kumar", "", "Reshav Kumar")
    Log.log(fp.data.__dict__)
    #br.close_browser()
