
class FacebookData:
    def __init__(self):
        self.fb_url = ""
        self.fb_profilephoto = ""

class TwitterData:
    def __init__(self):
        self.twitter_id = ""


class Detail(FacebookData,TwitterData):
    def __init__(self):
        FacebookData.__init__(self)
        TwitterData.__init__(self)
        self.name = ""
        self.email = ""
        self.phoneno = ""

    @staticmethod
    def init_with_dict(detail_dict):
        detail = Detail()
        if(detail_dict == None):
            return detail
        detail.name = detail_dict['name']
        detail.phoneno = detail_dict['phoneno']
        detail.email = detail_dict['email']

        detail.fb_profilephoto = detail_dict['fb_profilephoto']
        detail.fb_url = detail_dict['fb_url']

        detail.twitter_id = detail_dict['twitter_id']
        return detail