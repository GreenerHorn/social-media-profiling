import random
import Log
"""Checks given string is empty or not. Return True if string is empty"""
def is_empty_string(string):
    return string is None or string == ""

"""Generate random number between 0.5 and 1.5"""
def get_random_time():
    Log.log("Generating random number")
    return random.random()+0.5
