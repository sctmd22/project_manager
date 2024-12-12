from datetime import datetime
from GLOBALS import *

def get_SQL_timestamp():
    return datetime.today().strftime(SQL_DATETIME_FORMAT)


def get_simple_date():
    return datetime.today().strftime(SIMPLE_DATE_FORMAT)


def num_str_targets():
    numStrTargets = 5
    return numStrTargets


#Replace empty strings with 0
def zero_fill(list):
    listLen = len(list)

    if(listLen == 0):
        print(f"List is length 0")
        return 0

    try:
        for i in range(len(list)):
            if(list[i] == ''):
                list[i] = 0

    except:
        print(f"Could not iterate through list")
        return 0


    return list

def create_str_table(str, days, id):
    #Pad data to get to desired length
    #str_table_str_padded = str + ['0'] * (num_str_targets() - len(str_table_strength))
    #str_table_days_padded = days + ['0'] * (num_str_targets() - len(str_table_days))

    strList = zero_fill(str)
    daysList = zero_fill(days)

    idList = [id] * num_str_targets() #Create a list of id's

    #Zip the data (tuples and lists) to create a list of tuples to be added to the mysql database in one query
    str_table_data = list(zip(idList, strList, daysList))

    return str_table_data


def listStrtoInt(list):
    newList = []
    for i in range(len(list)):
        try:
            newList.append(int(list[i]))
        except:
            return list

    return newList


def strToInt(val):
    try:
        newVal = int(val)

    except:
        print(f"Error: Could not convert '{val}' to integer")
        return None

    return newVal

def strToFloat(val):
    if(val == ""):
        return 0


    try:
        newVal = float(val)

    except:
        print(f"Error: Could not convert '{val}' to float")
        return None

    return newVal

#Convert a date string of HTML_DATE_FORMAT to a python datetime
def formToDate(strDate):
    funcName = "strToDate"

    if(strDate == ""):
        print(f"Error: {funcName}: strTime is empty")
        return None

    try:
        newDate = datetime.strptime(strDate, HTML_DATE_FORMAT) #Convert to datetime object

    except:
        print(f"Error: {funcName} Could not convert '{strDate}' to DATETIME using '{HTML_DATE_FORMAT}'")
        return None

    return newDate


#Convert a time string of either HTML time input or MYSQL time to a python datetime
    #MySQL will convert a python datetime to a TIME object automatically when inserting
def formToTime(strTime):
    funcName = "formToDate"

    size = len(strTime)

    if(not size):
        print(f"Error: {funcName}: date is empty")
        return None

    #HH:MM
    elif(size == len(HTML_TIME_FORMAT)):
        try:
            newTime = datetime.strptime(strTime, HTML_TIME_FORMAT)

        except:
            print(f"Error: {funcName} Could not convert '{strTime}' to DATETIME using format '{HTML_TIME_FORMAT}'")
            return None

        return newTime

    #HH:MM:SS
    elif(size == len(SQL_TIME_FORMAT)):
        try:
            newTime = datetime.strptime(strTime, SQL_TIME_FORMAT)

        except:
            print(f"Error: {funcName} Could not convert '{strTime}' to DATETIME using format '{SQL_TIME_FORMAT}'")
            return None

        return newTime

    return None



def removeNone(val):
    if(not val):
        return ""

    return val

