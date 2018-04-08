import os
from pymongo import MongoClient
from random import randint
from facebook import *
from TwitterLinkedin import *
from Twitter import *
import Log
import pandas as pd
import datetime
import threading
dic={}

c=0
length=0

class DataBaseHandler:
	cilent=None
	db=None
    def __init__(self):
    	if DataBaseHandler.client is None:
	        client = MongoClient(port=27017)
	        db=client.mahindra
	        coll=db.profileData
	    return
        

    def Storedata(name,email,no):
		Log.log("In storeData")
		dic={'name':name, 'email':email.lower(),'number':no}
		
		try:
			cursor=coll.find(dic)
			print cursor 
			if  cursor.count()==0:
				coll.insert_one(dic)
			return "success"
		except Exception as e:
			print str(e)
			return "error"



    def UpdateDB(data,document):
    	Log.log("In UpdateDB")
		coll.update(document,{"$set":data})
		Log.log("UpdateDB completed")

	def getDBlen():
		Log.log("In getDBlen")
		count=coll.find().count()
		Log.log("getDBlen completed")
		return count

	def csvBrowserWork(listt,i):
	if len(listt):
		f=Facebook()
		browser = f.createBrowser()
		f.facebookLogin(browser)
		linkedinLogin(browser)
		twitterLogin(browser)
		List = getList(browser)
		listDataFinder(browser,f,listt,List,i)
		browser.close()


	def listDataFinder(browser,fb,person,List,i):	
		global c
		print datetime.datetime.now()
		
		for x in person:
			time.sleep(1)
			x[2]=str(x[2])
			data=fb.facebookData(browser,x[0].lower(),x[1].lower(),x[2].lower())
			data.update({'name':x[0].lower(),'email':x[1].lower(),'number':x[2].lower()})
			y = linkedinData(browser,data)
		    	data['linkedin_url']= y
			y = twitterData(browser,List,x[0].lower())
			data.update(y)
			cursor=coll.find({'name':x[0].lower(),'email':x[1].lower(),'number':x[2].lower()})
			print {"name":x[0],"email":x[1],"number":x[2]}
			if  cursor.count()==0:
				data['_id']=str(i)
				data['name']=str(x[0])
				data['email']=str(x[1].lower())
				data['number']=str(x[2])
				coll.insert_one(data)
			else:
				UpdateDB(data,{"_id":str(i),"name":x[0],"email":x[1],"number":x[2]})
			i=i+1
			lock=threading.Lock()
			lock.acquire()
			try:
			  	 c=c+1
			  	
			finally:
			    lock.release()
			print c
		
		print datetime.datetime.now()
		return 


	def getSingleuser(email):
			if coll.find({"email":email}).count()==0:
				return None
			return coll.find({"email":email})



	def Loadcsv(path):
	try:
		Log.log(" in Loadcsv")
		global length
		#os.system("mongoimport -d mahindra -c profileData --type csv --file "+path+" --headerline")
		
		df = pd.read_csv(path)
		total_rows=len(df.axes[0])
		total_cols=len(df.axes[1])
		length=total_rows
		x=df.iloc[:,:].values
		len_x= len(x)
		le=(len_x)/1
		threads=[]
		y=x[:min(le,len_x)]
		size=coll.find().count()
		t = threading.Thread(target=csvBrowserWork, args=(y,size+0,))
		print 'er'
		t.start()
		"""print 't'
		threads.append(t)
		y=x[min(le,len_x):min(2*le,len_x)]
		t =threading.Thread(target=csvBrowserWork, args=(y,size+min(le,len_x)))
		t.start()
		threads.append(t)
		y=x[min(2*le,len_x):min(3*le,len_x)]
		t = threading.Thread(target=csvBrowserWork, args=(y,size+min(2*le,len_x)))
		t.start()
		threads.append(t)
		y=x[min(3*le,len_x):len_x]
		t = threading.Thread(target=csvBrowserWork, args=(y,size+min(3*le,len_x)))
    		t.start()
   		threads.append(t)
   		"""
   		'''for t in threads:
   			 t.join()'''
		return "success"
	except Exception as e: 
		print str(e)
		return "error"

	def getcc():
		global c
		return c
	def getlen():
		global length
		return length
        
