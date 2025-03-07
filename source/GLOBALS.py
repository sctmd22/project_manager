from enum import Enum

class TIME_FORMATS(Enum):
    ISO_TIME_FORMAT = "%H:%M:%S"
    SIMPLE_TIME_FORMAT = "%H:%M"
    DECIMAL_TIME_FORMAT = "%H:%M:%S.%f"

class DATE_FORMATS(Enum):
    ISO_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
    ISO_DATE_FORMAT_S = "%Y-%m-%dT%H:%M:%S"
    SQL_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"          #SQL uses this (but supports many time formats)
    SQL_DATE_FORMAT_U = "%Y-%m-%d %H:%M:%S.%f"
    SIMPLE_DATE_FORMAT = "%Y-%m-%d"                #Returned by HTML date input
    SIMPLE_DATE_FORMAT_T = "%Y-%m-%d %H:%M"
    HTML_DATE_FORMAT_T = "%Y-%m-%dT%H:%M"          #Returned by HTML date and time input

#Tells JavaScript what type of validation to use for the associated data
VALIDATION_TYPES = {
    'INT':1,
    'POS_INT':2,
    'NEG_INT':3,
    'NUMBER':4,
    'TEXT':5,
    'EMAIL':6
}


