import Log
import pymongo
import Constants
from Details import Detail

class DataBaseHandler:
    db = None
    client = None
    collection = None

    def __init__(self):
        if DataBaseHandler.client is None:
            DataBaseHandler.client = pymongo.MongoClient(Constants.DB_URL)
            DataBaseHandler.db = DataBaseHandler.client[Constants.DATABASE]
            DataBaseHandler.collection = DataBaseHandler.db[Constants.DB_Collection]
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

    def update_from_details(self,detail):
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
        Log.log("Update status ",DataBaseHandler.collection.update_one(search_dict,set_dict)!= None)
        return


if __name__ == "__main__":
    x = Detail()
    x.email = "vivek"
    DataBaseHandler().insert_from_details(x)
    Log.log(DataBaseHandler().get_data_with_email("vivek").__dict__)
    x.phoneno = "7030307739"
    DataBaseHandler().update_from_details(x)


