import random
import Log
import time
import urllib

def is_empty_string(string):
    return string is None or string == ""

def get_random_number():
    Log.log("Generating random number 1+")
    return random.random() + 1

def random_wait():
    Log.log("random wait")
    time.sleep(get_random_number())
    return

def remove_non_ascii(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])

def url_encode(query):
    encoded = urllib.parse.quote(query)
    Log.log("encoded", query, encoded)
    return encoded

def tier_city(data):
    city_tier = 'Tier 3 City'
    city_x = ['ahmedabad', 'bangalore', 'chennai', 'delhi', 'hyderabad', 'kolkata', 'mumbai', 'pune']
    city_y = ['agra', 'ajmer', 'aligarh', 'allahabad', 'amravati', 'amritsar', 'asansol', 'aurangabad',
              'bareilly', 'belgaum', 'bhavnagar', 'bhiwandi', 'bhopal', 'bhubaneswar', 'bikaner',
              'bokaro', 'chandigarh', 'coimbatore', 'cuttack', 'dehradun', 'dhanbad', 'durg', 'durgapur',
              'erode', 'faridabad', 'firozabad', 'ghaziabad', 'gorakhpur', 'gulbarga', 'guntur', 'gurgaon',
              'guwahati', 'gwalior', 'indore', 'jabalpur', 'jaipur', 'jalandhar', 'jammu', 'jamnagar',
              'jamshedpur', 'jhansi', 'jodhpur', 'kannur', 'kanpur', 'kakinada', 'kochi', 'kottayam',
              'kolhapur', 'kollam', 'kota', 'kozhikode', 'kurnool', 'lucknow', 'ludhiana', 'madurai', 'malappuram',
              'malegaon', 'mangalore', 'meerut', 'moradabad', 'mysore', 'nagpur', 'nashik', 'nellore', 'noida',
              'patna', 'pondicherry', 'raipur', 'rajkot', 'rajahmundry', 'ranchi', 'rourkela', 'salem', 'sangli',
              'siliguri', 'solapur', 'srinagar', 'surat', 'thiruvananthapuram', 'palakkad', 'thrissur',
              'tiruchirappalli', 'tiruppur', 'ujjain', 'vijayapura', 'vadodara', 'varanasi', 'vasai-virar city',
              'vijayawada', 'visakhapatnam', 'warangal']
    for i in city_x:
        if i.lower() in data.lower():
            city_tier = 'Tier 1 City'

    for i in city_y:
        if i.lower() in data.lower():
            city_tier = 'Tier 2 City'
    return city_tier
