import os
from pymongo import MongoClient
from random import randint
from facebook import *
from TwitterLinkedin import *
from Twitter import *

import pandas as pd
import datetime
import threading

client = MongoClient(port=27017)
db=client.mahindra
coll=db.profileData

class DatabaseHandler:

    def Storedata(name,email,no):
	print "start"
	dic={'name':name, 'email':email.lower(),'number':no}
	
	try:
		cursor=coll.find(dic)
		print cursor 
		if  cursor.count()==0:
			print "asdf"
			coll.insert_one(dic)
		return "success"
	except Exception as e:
		print str(e)
		return "error"

    def UpdateDB(data,document):
	coll.update(document,{"$set":data})
        
