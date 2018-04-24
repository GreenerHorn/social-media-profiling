import random
import Log
import time

"""Checks given string is empty or not. Return True if string is empty"""
def is_empty_string(string):
    return string is None or string == ""

"""Generate random number between 0.5 and 1.5"""
def get_random_number():
    Log.log("Generating random number")
    return random.random()+0.5

def random_wait():
    Log.log("random wait")
    time.sleep(get_random_number())
    return

def remove_non_ascii(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])