import requests
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

    def __init__(self, browser,data):
        self.browser = browser
        self.data = data
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
                        self.data.tier_city = Utils.tier_city(self.data.lives)
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
                    self.data.fb_profilephoto = i
                    Log.log('Profile Pic available ', i)
                    return
        except Exception as e:
            Log.log(str(e), ' failed in getImage (Profile Pic Not available) ')
        return

    def __get_likes_auto_politics(self, array_of_like):
        self.data.total_likes = len(array_of_like)
        auto_keywords = ['auto', 'motor', 'drive', 'gear', 'speed', 'race', 'racing', 'formula', 'formula one',
                         'drag race', 'vehicle', 'car', 'bike', 'moto', 'offroad', 'sae', 'baja', 'tyre', 'mechanical',
                         'f1', 'toyota', 'volkswagen', 'ford', 'bmw', 'audi', 'honda', 'suzuki', 'mazda', 'renault',
                         'nissan', 'volvo', 'yamaha', 'mahindra', 'kia', 'hyundai', 'fiat', 'tesla', 'jaguar',
                         'ferrari', 'chevrolet', 'tata', 'bugatti', 'lamborghini', 'jeep']
        politics_keywords = ['barack obama', 'donald trump', 'narendra modi', 'arvind kejriwal', 'shashi tharoor',
                             'rahul gandhi', 'bjp', 'congress', 'bhartiya janata party', 'lalu prasad', 'nitish kumar',
                             'arun jaitley', 'mamata banerjee', 'sushma swaraj', 'amit shah', 'india', 'gandhi',
                             'nehru', 'ambedkar', 'atal', 'kalam', 'pm', 'president', 'shastri', 'sardar patel', 'rss',
                             'rashtriya', 'netaji', 'subhash bose', 'ntr', 'manmohan', 'naidu', 'thackeray', 'rao',
                             'reddy']
        travel = ['makemytrip', 'cleartrip', 'irctc', 'indigo', 'jetairways', 'emirates', 'yatra', 'paytm', 'spicejet',
                  'airasia', 'oyo', 'bookmyshow', 'pvr', 'ixigo', 'discovery', 'national geography', 'history',
                  'redbus']
        online_shopping = ['flipkart', 'amazon', 'myntra', 'jabong', 'paytm', 'shopclues', 'snapdeal', 'foodpanda',
                           'food', 'mcdonald', 'pizza', 'kfc']
        try:
            for i in array_of_like:
                for j in auto_keywords:
                    if j.lower() in i.lower():
                        self.data.count_auto += 1
                for k in politics_keywords:
                    if k.lower() in i.lower():
                        self.data.count_pol += 1
                for k in online_shopping:
                    if k.lower() in i.lower():
                        self.data.count_shop += 1
                for k in travel:
                    if k.lower() in i.lower():
                        self.data.count_travel += 1
        except Exception as ex:
            Log.log("error ", str(ex))

        Log.log("Likes auto politics shopping travel done")
        return

    def __get_friends_list(self, page):
        friend_list = []
        friend_list_html = page.find_all("div", {"class": "clearfix _5qo4"})
        for friend in friend_list_html:
            img_name_tag = friend.find("img")
            url_tag = friend.find("a")
            name = ""
            image = ""
            url = ""
            if url_tag and url_tag.get("href"):
                url = url_tag.get("href")
            if img_name_tag and img_name_tag.get("src"):
                image = img_name_tag.get("src")
            if img_name_tag and img_name_tag.get("aria-label"):
                name = img_name_tag.get("aria-label")
            friend_list.append(name)
            friend_list.append(image)
            friend_list.append(url)

            Log.log(name, " ", url, " ", image)
        self.data.fb_friend = friend_list
        Log.log("Friend list complete")
        return

    def __get_likes_movies(self, like_list):
        final = []
        try:
            for x in like_list:
                xGenre = search(x)
                for each in xGenre:
                    if each not in final:
                        final.append(each)
                        final.append(1)
                    else:
                        index = final.index(each)
                        final[index + 1] += 1
        except Exception as ex:
            print(str(ex))
            print("Error in getGenre")
        self.data.fb_movies_genre = final
        return

    def __get_likes(self):
        self.browser.open_link(self.data.fb_url + "/likes_all")
        Utils.random_wait()
        self.browser.scroll_end()
        Utils.random_wait()
        page = BeautifulSoup(self.browser.browser.page_source, "lxml")
        likes_all = page.find_all("div", {"class": "_6a _6b"})
        Log.log("likes_all count ", len(likes_all))
        like_list = []
        insights = []
        for like in likes_all:
            like_text_tag = like.find("div", {"class": "fsl fwb fcb"})
            like_type_tag = like.find("div", {"class": "fsm fwn fcg"})
            if like_text_tag is not None and like_type_tag is not None:
                like_text = like_text_tag.text
                like_type = like_type_tag.text
                Log.log(like_type, " ", like_text)
                like_list.append(like_text)
                if like_type not in insights:
                    insights.append(like_type)
                    insights.append(1)
                else:
                    index = insights.index(like_type)
                    insights[index + 1] += 1
        self.data.fb_likes = like_list
        self.data.fb_likes_insights = insights
        Log.log("insights ", insights)
        Log.log("total number of like_list ", len(like_list), " like_list ", like_list)
        self.__get_likes_auto_politics(like_list)
        self.__get_likes_movies(like_list)
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


def search(query):
    mapper = {
        12: 'Adventure',
        14: 'Fantasy',
        16: 'Animation',
        18: 'Drama',
        27: 'Horror',
        28: 'Action',
        35: 'Comedy',
        36: 'History',
        37: 'Western',
        53: 'Thriller',
        80: 'Crime',
        99: 'Documentary',
        878: 'Science Fiction',
        9648: 'Mystery',
        10402: 'Music',
        10749: 'Romance',
        10751: 'Family',
        10752: 'War',
        10770: 'TV Movie'
    }
    try:
        get_url = 'https://api.themoviedb.org/3/search/movie?api_key=d19e3034bd731f3ecf5809f7a8dbdbbe&query=' + query
        req = requests.get(get_url)
        x = req.json()
        #Log.log(x, get_url)
        if x["total_results"] > 0:
            y = x['results'][0]['genre_ids']
            y = [mapper[e] for e in y]
            Log.log(y)
            return y
    except Exception as ex:
        Log.log(str(ex))
        Log.log('movie search failed movie not found for ' + str(query))
    return []


if __name__ == "__main__":
    br = Browser()
    fp = FacebookParser(br)
    fp.login()
    fp.search("Reshav Kumar", "", "Reshav Kumar")
    Log.log(fp.data.__dict__)
    # br.close_browser()
