from enum import Enum


class TIME_FORMATS(Enum):
    ISO_TIME_FORMAT = "%H:%M:%S"
    SIMPLE_TIME_FORMAT = "%H:%M"
    DECIMAL_TIME_FORMAT = "%H:%M:%S.%f"

class DATE_FORMATS(Enum):
    ISO_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"          #SQL uses this (but supports many time formats)
    ISO_DATE_FORMAT_U = "%Y-%m-%d %H:%M:%S.%f"
    SIMPLE_DATE_FORMAT = "%Y-%m-%d"                #Returned by HTML date input
    SIMPLE_DATE_FORMAT_T = "%Y-%m-%d %H:%M"
    HTML_DATE_FORMAT_T = "%Y-%m-%dT%H:%M"          #Returned by HTML date and time input


'''
class VALIDATION_TYPES(Enum):
    INT = 1
    NUMBER = 2
    TEXT = 3
    EMAIL = 4
'''

#Tells JavaScript what type of validation to use for the associated data
VALIDATION_TYPES = {
    'INT':1,
    'NUMBER':2,
    'TEXT':3,
    'EMAIL':4
}