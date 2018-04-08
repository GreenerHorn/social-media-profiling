from flask_cors import CORS, cross_origin
import os
from flask import Flask, render_template, request,jsonify
from werkzeug import secure_filename
from DataBase import *
from TwitterLinkedin import *
from Twitter import *
import json
from name import *
import requests
import Log
app = Flask(__name__)
CORS(app)


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]


app.config['UPLOAD_FOLDER'] = "/home/ashish/mahindra"
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      try:
      	      global path
	      filename=secure_filename(f.filename)
	      f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	      path=app.config['UPLOAD_FOLDER']+'/'+filename
	      status=Loadcsv(path)
	      if status=="success":
	     		 return "success"
	      else:
	     		 return "failed"
      except Exception as e:
      		print repr(e)
		return 'failed'



def processData(cursur,dummy):
	dummy['flag']=1
	if cursur.has_key('number'):
		dummy['number']=cursur['number']
	if cursur.has_key('from'):
		dummy['from']=cursur['from']
	if cursur.has_key('email'):
		dummy['email']=cursur['email']
	if cursur.has_key('birthday'):
		dummy['birthday']=cursur['birthday']
	if cursur.has_key('lives'):
		dummy['lives']=cursur['lives']
	if cursur.has_key('name'):
		dummy['name']=cursur['name']
	if cursur.has_key('studied'):
		dummy['studied']=cursur['studied']
	if cursur.has_key('works'):
		dummy['works']=cursur['works']
	if cursur.has_key('studies'):
		dummy['studies']=cursur['studies']
	if cursur.has_key('interest'):
		dummy['interest']=cursur['interest']
	if cursur.has_key('friends'):
		dummy['friends']=cursur['friends']
	if cursur.has_key('status'):
		dummy['status']=cursur['status']
	if cursur.has_key('linkedin_url'):
		dummy['linkedin_url']=cursur['linkedin_url']
	if cursur.has_key('city_tier'):
		dummy['city_tier']=cursur['city_tier']
	if cursur.has_key('count_travel'):
		dummy['count_travel']=cursur['count_travel']
	if cursur.has_key('count_shop'):
		dummy['count_shop']=cursur['count_shop']
	if cursur.has_key('count_auto'):
		dummy['count_auto']=cursur['count_auto']
	if cursur.has_key('count_politics'):
		dummy['count_politics']=cursur['count_politics']
	if cursur.has_key('topics'):
		dummy['topics']=cursur['topics']
	if cursur.has_key('influencees'):
		dummy['influencees']=cursur['influencees']
	if cursur.has_key('influencers'):
		dummy['influencers']=cursur['influencers']
	if cursur.has_key('score'):
		dummy['score']=cursur['score']
	if cursur.has_key('twitterId'):
		dummy['twitterId']=cursur['twitterId']
	if cursur.has_key('kloutid'):
		if cursur['kloutid']!='Not Public':
			dummy['kloutId']=cursur['kloutid']
	if cursur.has_key('fb_url'):
		if cursur['fb_url']!='Not Public':
			dummy['fb_url']=cursur['fb_url']
	if cursur.has_key('profilePic'):
		if cursur['profilePic']!='Not Public':
			dummy['profilePic']=cursur['profilePic']
	if cursur.has_key('genre'):
			for x in cursur['genre']:
				dummy['genre'][x[0]]=x[1]
	value=cleanData(cursur['name'],cursur['number'],cursur['email'])
	
	if value['isCompany']=="1":		
		result = doGoogleSearch(name)
		if len(result[0]):
			link = result[1][0]
			x=doAutoPortal(link)
		#latitude, longitude=get_coordinates(x[1])
		#dummy['latitude']=latitude
		#dummy['longitude']=longitude
		dummy['companyAddress']=x[1]
		dummy['isCompany']=1
	return dummy
		



@app.route('/getData', methods=['POST'])
def  getData():

	db=DataBaseHandler()
	email=request.json["email"] 
	cursur=getSingleuser(email)
	print "2"
	if cursur is None:
		dummy=getDummy()
		return json.dumps(dummy)
	#print  cursur[0]
	print cursur[0]
	dummy=getDummy()
	print "3"
	x=processData(cursur[0],dummy)
	#print json.dumps(x)
	return json.dumps(x)
	
	
@app.route('/getPercentage', methods=['GET'])
def  getPercentage():
	return str((getcc()/float(getlen()))*100)
	#return str((3/float(84))*100)
    
@app.route('/glassDoor', methods=['POST'])
def  getglassDoor():
	job=request.json["company"] 
	response = requests.get('http://api.glassdoor.com/api/api.htm?t.p=198675&t.k=bNhFK8dJnmY&userip=0.0.0.0&useragent=59.0.3071.115&format=json&v=1&action=employers&q='+job, headers=headers)
	print   response.text
	return response.text
	
    

    
@app.route('/postData', methods=['POST'])
def  postData():
	print "1.0"
	print request.json["name"]
	name=request.json["name"]
	email=request.json["email"] 
	phone=request.json["mob_no"]
	print "1.1"
	try:
			print "1.2"
	 		status=Storedata(name,email,phone)
	    		f=Facebook()
			browser = None
			while (browser is None):
				print  'hello'
				browser = f.createBrowser()
			while not f.facebookLogin(browser):
				time.sleep(1)
				print '[+] retrying fb login'
			while not linkedinLogin(browser):
				time.sleep(1)
				print '[+] retrying linkedin login'
			
			data=f.facebookData(browser,name,email,phone)
			data.update({'name':name,'email':email,'number':phone})
			y = linkedinData(browser,data)
			data['linkedin_url']= y
			twitterLogin(browser)
			List = getList(browser)
			y = twitterData(browser,List,name.lower())
			data.update(y)
			
	    		print "1"
			browser.close()
			print "2"
			dummy=getDummy()
			x=processData(data,dummy)
			UpdateDB(data,{'name':name,'email':email,'number':phone})
			print "1.3"
			str1=json.dumps(x)
			return str1
    		
    	except Exception as e:
    		print repr(e)
    		return "Failed"
    	

 		

if __name__ == '__main__':
    app.debug = True
    app.run(threaded=True)
    
    
    
    




