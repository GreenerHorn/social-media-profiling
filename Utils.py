import random
import Log
import time
import urllib


"""Checks given string is empty or not. Return True if string is empty"""
def is_empty_string(string):
    return string is None or string == ""

"""Generate random number between 0.7 and 1.7"""
def get_random_number():
    Log.log("Generating random number")
    return random.random()+0.7

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
