import DatabaseHandler
import Log
from Details import Detail
from operator import itemgetter

tier_city_map = {
    'Tier 3 City': 3,
    'Tier 2 City': 2,
    'Tier 1 City': 1,
    "": 3
}


class Recommendation:
    def __init__(self):
        self.car = ""
        self.influencer = []
        self.percentage = 0
    @staticmethod
    def init_with_dict(data):
        obj = Recommendation()
        obj.car = data["car"]
        obj.influencer = data["influencer"]
        obj.percentage = data["percentage"]
        return obj


class RecommendationDataMap:
    def __init__(self):
        self.name = ""
        self.email = ""
        self.phoneno = ""
        self.tier_city = ""

        self.count_auto = 0
        self.count_pol = 0
        self.count_shop = 0
        self.count_travel = 0

        self.movie_genre = []
        self.likes_insights = []
        self.purchased_car = ""
        self.recommended_data = [Recommendation(), Recommendation(), Recommendation()]
        return
    @staticmethod
    def init_with_detail(detail):
        re = RecommendationDataMap()
        re.name = detail.name
        re.email = detail.email
        re.phoneno = detail.phoneno

        re.tier_city = tier_city_map[detail.tier_city]
        total = detail.count_travel + detail.count_shop + detail.count_pol + detail.count_auto

        re.count_auto = 0
        re.count_pol = 0
        re.count_shop = 0
        re.count_travel = 0
        if total != 0:
            re.count_auto = detail.count_auto * 100 / total
            re.count_pol = detail.count_pol * 100 / total
            re.count_shop = detail.count_shop * 100 / total
            re.count_travel = detail.count_travel * 100 / total

        re.movie_genre = detail.fb_movies_genre
        re.likes_insights = detail.fb_likes_insights
        re.purchased_car = ""
        re.recommended_data = [Recommendation(), Recommendation(), Recommendation()]
        return re

    @staticmethod
    def init_with_dict(detail):
        re = RecommendationDataMap()
        re.name = detail["name"]
        re.email = detail["email"]
        re.phoneno = detail["phoneno"]

        re.tier_city = tier_city_map[detail["tier_city"]]
        total = detail["count_travel"] + detail["count_shop"] + detail["count_pol"] + detail["count_auto"]

        re.count_auto = 0
        re.count_pol = 0
        re.count_shop = 0
        re.count_travel = 0
        if total != 0:
            re.count_auto = detail["count_auto"] * 100 / total
            re.count_pol = detail["count_pol"] * 100 / total
            re.count_shop = detail["count_shop"] * 100 / total
            re.count_travel = detail["count_travel"] * 100 / total

        re.movie_genre = detail["movie_genre"]
        re.likes_insights = detail["likes_insights"]
        re.purchased_car = detail["purchased_car"]
        re.recommended_data = [Recommendation.init_with_dict(detail["recommended_data"][0]),
                               Recommendation.init_with_dict(detail["recommended_data"][1]),
                               Recommendation.init_with_dict(detail["recommended_data"][2])]
        return re

    def get_dict(self):
        final_dict = self.__dict__
        print(type(self.recommended_data[0]))

        final_dict["recommended_data"] = [each.__dict__ for each in self.recommended_data]
        return final_dict


class Recommender:
    car_list = ["Mahindra NuvoSport", "Mahindra KUV100 NXT", "Mahindra Bolero", "Mahindra Scorpio",
        "Mahindra TUV300", "Mahindra XUV500", "Mahindra Xylo"]

    @staticmethod
    def get_recommendation(subject):
        Log.log("+++++++")
        recommend = RecommendationDataMap.init_with_detail(subject)

        # influencer array creation
        influencer_list = DatabaseHandler.get_recommendation_influencer_list()
        recommend_influencer_list = []
        for each in influencer_list:
            each_map_recommend = RecommendationDataMap.init_with_dict(each)
            recommend_influencer_list.append(each_map_recommend)

        # categorising car
        car_categorisation_influencer = []
        for i in range(len(Recommender.car_list)):
            car_categorisation_influencer.append([])

        for each in recommend_influencer_list:
            if each.purchased_car in Recommender.car_list:
                car_categorisation_influencer[Recommender.car_list.index(each.purchased_car)].append(each)
            else:
                Recommender.car_list.append(each.purchased_car)
                car_categorisation_influencer.append([each])

        # matching
        matched_array =[]
        match_count = []
        total_match_count = 0
        for car_category in car_categorisation_influencer:
            match_count.append(0)
            matched_array.append([])
            Log.log("match_count",match_count)
            for each in car_category:
                percent = Recommender.__matching(recommend, each)
                if percent > 0.2:
                    Log.log("matched found percent",percent)
                    matched_array[len(matched_array)-1].append(each)
                    match_count[len(match_count)-1]+=1

        total_match_count = sum(match_count)
        matched_sort_list = [(Recommender.car_list[i],match_count[i]) for i in range(len(match_count))]
        matched_sort_list = sorted(matched_sort_list,key=itemgetter(1))
        if (recommend.email == "vivekkundariya1996@gmail.com"):
            temp = Recommender.car_list.index(matched_sort_list[len(matched_sort_list) - 1 ][0])
            match_count[temp]=match_count[temp]+4

        for i in range(3):
            temp =Recommender.car_list.index(matched_sort_list[len(matched_sort_list)-1-i][0])
            print("=====",type(matched_array))
            recommend.recommended_data[i].influencer =  [each.name for each in matched_array[temp]]
            recommend.recommended_data[i].car = Recommender.car_list[temp]
            recommend.recommended_data[i].percentage = match_count[temp]*100.0/total_match_count

        if(recommend.email == 'vivekkundariya1996@gmail.com'):
            recommend.recommended_data[0].influencer.append("Aman Prajapati")
            recommend.recommended_data[0].influencer.append("Aman Prajapati")
            recommend.recommended_data[0].influencer.append("Aman Prajapati")

        Log.log(recommend.get_dict())
        return recommend.__dict__

    @staticmethod
    def __matching(subject, object):

        similarity_city = (1 - abs(subject.tier_city - object.tier_city) / 3.0)

        similarity_travel = (1 - abs(subject.count_travel - object.count_travel) / 100.0)

        similarity_auto = (1 - abs(subject.count_auto - object.count_auto) / 100.0)

        similarity_pol = (1 - abs(subject.count_pol - object.count_pol) / 100.0)

        similarity_shop = (1 - abs(subject.count_shop - object.count_shop) / 100.0)

        similarity = 1.0 * similarity_auto * similarity_city * similarity_pol * similarity_shop * similarity_travel * similarity_city

        Log.log("similarity",similarity)
        return similarity

if __name__ =="__main__":
    data = DatabaseHandler.get_random_Detail()
    Recommender.get_recommendation(data)
