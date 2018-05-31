import Log
import pymongo
import Constants
from Details import Detail
from random import random,randint


class DataBaseHandler:
    db = None
    client = None
    collection = None

    def __init__(self):
        if DataBaseHandler.client is None:
            DataBaseHandler.client = pymongo.MongoClient(Constants.DB_URL)
            DataBaseHandler.db = DataBaseHandler.client[Constants.DATABASE]
            DataBaseHandler.collection = DataBaseHandler.db[Constants.DB_UserData_Collection]
        return

    def get_all_data(self):
        if DataBaseHandler.db is None:
            return
        return list(DataBaseHandler.collection.find())

    def insert_from_details(self, detail):
        if type(detail).__name__ != 'Detail':
            Log.log("No suitable detail given")
            return
        detail_dict = detail.__dict__
        if '_id' in detail_dict:
            detail_dict.pop('_id', None)
        Log.log(detail_dict)
        Log.log("inserted with id ",DataBaseHandler.collection.insert(detail_dict))
        Log.log(self.get_all_data())
        return

    def get_data_with_email(self,email):
        cursor = DataBaseHandler.collection.find_one({'email':email})
        Log.log(cursor)
        return Detail().init_with_dict(cursor)

    def update_from_detail(self,detail):
        if type(detail).__name__ != 'Detail':
            Log.log("No suitable detail given")
            return

        search_dict = {'email':detail.email}
        cursor = DataBaseHandler.collection.find_one(search_dict)
        Log.log(cursor)

        if cursor is None:
            Log.log("data not found, while updating so inserting the data")
            self.insert_from_details(detail)
            return

        detail_dict = detail.__dict__
        if '_id' in detail_dict:
            detail_dict.pop('_id', None)

        set_dict = {'$set':detail_dict}
        Log.log(set_dict)
        Log.log("Update status ", DataBaseHandler.collection.update_one(search_dict, set_dict) is not None)
        return

def get_random_Detail():
    data = Detail()
    data.name = str(random())
    data.email = str(random())
    data.number = str(random())
    x=["a","b","c"]
    y=['Tier 3 City','Tier 2 City','Tier 1 City',""]
    data.purchased_car = x[randint(0,2)]
    data.count_shop = randint(0, 10)
    data.count_auto = randint(0, 10)
    data.count_pol = randint(0, 10)
    data.count_travel = randint(0, 10)
    data.tier_city=y[randint(0,3)]
    return data

def get_recommendation_influencer_list():
    client = pymongo.MongoClient(Constants.DB_URL)
    db = client[Constants.DATABASE]
    collection = db[Constants.DB_Recommender_collection]
    cursor_list = list(collection.find())
    return cursor_list


if __name__ == "__main__":
    x = Detail()
    x.email = "abcd"
    DataBaseHandler().insert_from_details(x)
    Log.log(DataBaseHandler().get_data_with_email("vivek").__dict__)
    x.phoneno = "123456789"
    DataBaseHandler().update_from_details(x)


