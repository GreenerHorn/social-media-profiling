
class FacebookData:
    def __init__(self):
        self.fb_url = ""
        self.fb_profilephoto = ""
        self.fb_possible_ids = []
        self.works = ""
        self.studies = ""
        self.studied = ""
        self.lives = ""
        self.home = ""
        self.tier_city = ""
        self.fb_friend = []
        self.fb_likes = []
        self.fb_likes_insights = []
        self.count_auto = 0
        self.count_pol = 0
        self.count_shop = 0
        self.count_travel = 0
        self.total_likes = 0
        self.fb_movies_genre =[]


class TwitterData:
    def __init__(self):
        self.twitter_id = []

class LinkedInData:
    def __init__(self):
        self.linkedin_id = []

class Detail(FacebookData,TwitterData,LinkedInData):
    def __init__(self):
        FacebookData.__init__(self)
        TwitterData.__init__(self)
        LinkedInData.__init__(self)
        self.name = ""
        self.email = ""
        self.phoneno = ""
        self.kloutid = ""
        self.kloutscore = 0

    @staticmethod
    def init_with_dict(detail_dict):
        detail = Detail()
        if(detail_dict == None):
            return detail
        detail.name = detail_dict['name']
        detail.phoneno = detail_dict['phoneno']
        detail.email = detail_dict['email']

        detail.fb_url = detail_dict["fb_url"]
        detail.fb_profilephoto = detail_dict["fb_profilephoto"]
        detail.fb_possible_ids = detail_dict["fb_possible_ids"]
        detail.works = detail_dict["works"]
        detail.studies = detail_dict["studies"]
        detail.studied = detail_dict["studied"]
        detail.lives = detail_dict["lives"]
        detail.home = detail_dict["home"]
        detail.tier_city = detail_dict["tier_city"]
        detail.fb_friend = detail_dict["fb_friend"]
        detail.fb_likes = detail_dict["fb_likes"]
        detail.fb_likes_insights = detail_dict["fb_likes_insights"]
        detail.count_auto = detail_dict["count_auto"]
        detail.count_pol = detail_dict["count_pol"]
        detail.count_shop = detail_dict["count_shop"]
        detail.count_travel = detail_dict["count_travel"]
        detail.total_likes = detail_dict["total_likes"]
        detail.fb_movies_genre = detail_dict["fb_movies_genre"]

        detail.twitter_id = detail_dict['twitter_id']
        detail.kloutid = detail_dict["kloutid"]
        detail.kloutscore = detail_dict["kloutscore"]
        detail.linkedin_id = detail_dict['linkedin_id']
        return detail

#print(Detail().__dict__)