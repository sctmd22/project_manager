from enum import Enum

"""
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATETIME_FORMAT_U = DATETIME_FORMAT + ".%f"
SIMPLE_DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"
"""

class DATATYPES(Enum):
    VARCHAR = 1
    TEXT = 2
    INT = 3
    TINY_INT = 4
    SMALL_INT = 5
    DATETIME = 6
    TIME = 7
    ENUM = 8
    VARCHAR_DECIMAL = 9 #Exact decimal values stored as a VARCHAR in SQL
    BOOL = 10   #Uses TINYINT internally, but we will limit the values to 0 or 1

INT_SIZES = {
    'TINY_INT':     {'MIN':0, 'MAX':255},
    'SMALL_INT':    {'MIN':-32768, 'MAX':32767},
    'INT':          {'MIN':-2147483648, 'MAX':2147483647},
    'UINT':         {'MIN':0, 'MAX':2147483647},
}

TEXT_SIZES = {
    'TEXT':65535,
    'MEDIUM_TEXT':16777215,
    'LONGTEXT':4294967295
}


