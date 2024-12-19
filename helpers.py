from datetime import datetime
from GLOBALS import *
from flask import request

def get_SQL_timestamp():
    return datetime.today().strftime(SQL_DATETIME_FORMAT)


def get_simple_date():
    return datetime.today().strftime(SIMPLE_DATE_FORMAT)



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

def listStrtoInt(list):
    newList = []
    for i in range(len(list)):
        try:
            newList.append(int(list[i]))
        except:
            return list

    return newList


def strToInt(val):
    FUNC_NAME = "strToInt()"

    if(val == ''):
        return 0

    try:
        newVal = int(val)

    except:
        print(f"Error: {FUNC_NAME}: Could not convert '{val}' to integer")
        return None

    return newVal

def strToFloat(val):
    FUNC_NAME = "strToFloat()"
    if(val == ""):
        return 0

    try:
        newVal = float(val)

    except:
        print(f"Error: {FUNC_NAME}: Could not convert '{val}' to float")
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


#Iterate through 'Mix and field data' form inputs and build a dictionary of id's and values
    #Format and validate the data before returning
def get_cyl_field_data():
    FUNC_NAME = "get_cyl_field_data()"

    data = {}


    for id in CYL_FORM_FIELD_LIST:
        data[id] = request.form[id]

    # Convert string dates to datetime objects
    data['cylDateTransported'] = formToDate(data['cylDateTransported'])
    data['cylCastDate'] = formToDate(data['cylCastDate'])

    # Convert string times to datetime objects (MYSQL could handle strings but this is stricter)
    data['cylBatchTime'] = formToTime(data['cylBatchTime'])
    data['cylSampleTime'] = formToTime(data['cylSampleTime'])
    data['cylCastTime'] = formToTime(data['cylCastTime'])


    return data


#Iterate through conditions table form id's and create a list of dictionaries with the actial, min, max, notes and property values
def get_cyl_conditions_data(scc_val):
    sccCylKey = 'CYL'

    if(scc_val == 'yes'):
        sccCylKey = 'SCC'

    data = []

    #Loop through the CYL_CONDITIONS_TABLE getting the result of each entry
        #If scc_val is set, reset the rows where CYL = True to default values
    for row in CYL_CONDITIONS_TABLE:
        measureDict = {}

        #autoID's are stored in a hidden input and can always be read.
            #Technically ALL the inputs can be read as they are only hidden via JavaScript which keeps them in HTML
        autoID = request.form[row['name'] + CYL_CONDITIONS_SUFFIX['id']]

        if(row[sccCylKey] == True):
            valActual = request.form[row['name'] + CYL_CONDITIONS_SUFFIX['actual']]
            valMin = request.form[row['name'] + CYL_CONDITIONS_SUFFIX['min']]
            valMax = request.form[row['name'] + CYL_CONDITIONS_SUFFIX['max']]
            notes = request.form[row['name'] + CYL_CONDITIONS_SUFFIX['notes']]

        else:
            #Defaults for any where the key value is not true
            valActual = 0
            valMin = 0
            valMax = 0
            notes = ''


        measureDict['auto_id'] = autoID
        measureDict['val_actual'] = valActual
        measureDict['val_min'] = valMin
        measureDict['val_max'] = valMax
        measureDict['notes'] = notes
        measureDict['property'] = row['property']

        data.append(measureDict)


    return data



def get_cyl_str_data():
    str_table_strength = request.form.getlist('str_table_strength')
    str_table_days = request.form.getlist('str_table_days')
    str_table_id = request.form.getlist('str_table_id')

    strengthList = []

    #Build a dictionary that contains strength, days, and auto_id for each strength table entry
    for i in range(len(str_table_strength)):
        strDict = {}
        strDict['strength'] = strToInt(str_table_strength[i])
        strDict['days'] = strToInt(str_table_days[i])
        strDict['id'] = strToInt(str_table_id[i])
        strengthList.append(strDict)

    return strengthList

def strToIntID(val):
    FUNC_NAME = "strToIntID()"

    try:
        newInt = int(val)


    except:
        print(f"Error: {FUNC_NAME}: Could not convert '{val}' to a valid MySQL ID")
        return False

    if(newInt < 0):
        print(f"Error: {FUNC_NAME}: {newInt} is negative and therefore cannot be a valid MySQL ID")
        return False

    return newInt



def cyl_get_editing(getID):
    FUNC_NAME = "cyl_get_editing(getID)"
    #Default is a string 'false' not a bool. Keep it this way.
    try:
        get_edit = request.args.get(getID, default='false')

    except:
        print(f"Error: {FUNC_NAME}: Cannot GET '{getID}'")
        return False

    if(get_edit.lower() == 'true'):
        return True

    return False




