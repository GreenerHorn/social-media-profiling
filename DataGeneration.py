import pymongo

import Constants
import Log
import Recommendation
import random


def get_int_random(start, end):
    return random.randint(start, end)


tier_city_map = {
    3: 'Tier 3 City',
    2: 'Tier 2 City',
    1: 'Tier 1 City'
}

cars = ["Mahindra NuvoSport", "Mahindra KUV100 NXT", "Mahindra Bolero", "Mahindra Scorpio",
        "Mahindra TUV300", "Mahindra XUV500", "Mahindra Xylo",""]

movie_genre = ['Adventure', 'Fantasy', 'Animation', 'Drama', 'Horror', 'Action', 'Comedy',
               'History', 'Western', 'Thriller', 'Crime', 'Documentary', 'Science Fiction',
               'Mystery', 'Music', 'Romance', 'Family', 'War', 'TV Movie']

likes_insight = [
    "Media/news company", "News and media website", "Media", "Musician/band",
    "Entertainment website", "Charity", "Education", "Artist", "Internet company",
    "Community", "Arts and entertainment", "Science,technology & engineering",
    "Other", "Software", "TV channel", "Magazine", "Sport team", "Website", "Performance art",
    "Interest", "Public figure", "Education website", "TV programme","Community organisation",
    "Organisation", "Sports club", "Festival", "Event planner", "Local business",
    "College & University", "School", "Performance & event venue","Campus building",
    "App Page", "Sports", "Sporting event", "Video game", "TV network", "Just for fun",
    "Politician", "Machine shop", "Computer company", "Athlete", "Publisher", "Personal blog",
    "Product/service"
]

def generateRecommdation(name, email, phoneno):
    data = Recommendation.RecommendationDataMap()

    data.name = name
    data.email = email
    data.phoneno = phoneno

    data.tier_city = tier_city_map[get_int_random(1, 3)]

    data.count_travel = get_int_random(1,20)
    data.count_pol =  get_int_random(1,20)
    data.count_auto = get_int_random(1,20)
    data.count_shop = get_int_random(1,20)

    like = []
    random_no = get_int_random(5,10)
    choosen_array = []
    while len(choosen_array) != random_no:
        y = get_int_random(0,len(likes_insight)-1)
        if y not in choosen_array:
            choosen_array.append(y)
            like.append(likes_insight[y])
            x = get_int_random(2,15)
            like.append(x)
    data.likes_insights = like

    genre = []
    random_no = get_int_random(2,8)
    choosen_array = []
    while len(choosen_array) != random_no:
        y = get_int_random(0, len(movie_genre) - 1)
        if y not in choosen_array:
            choosen_array.append(y)
            genre.append(movie_genre[y])
            x = get_int_random(2, 15)
            genre.append(x)
    data.movie_genre = genre
    data.purchased_car = cars[get_int_random(0,len(cars)-1)]
    return data

def insert_db_recommender(data):
    client = pymongo.MongoClient(Constants.DB_URL)
    db = client[Constants.DATABASE]
    collection = db[Constants.DB_Recommender_collection]
    Log.log(data.get_dict(),collection.insert(data.__dict__))
    return

def get_all_data():
    with open("data.csv", "r") as f:
        data = f.read()
        data = data.split("\n")
        data = [x.split(",") for x in data]
        for e in data[10:700]:
            data = generateRecommdation(name=e[1],phoneno=e[0],email=e[2])
            insert_db_recommender(data)
    return

#get_all_data()
