import copy
from datetime import datetime
from GLOBALS import *
from flask import request
import decimal
import db as db

from db import sql_data as SQL

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
    elif(size == len(SQL.TIME_FORMAT)):
        try:
            newTime = datetime.strptime(strTime, SQL.TIME_FORMAT)

        except:
            print(f"Error: {funcName} Could not convert '{strTime}' to DATETIME using format '{SQL.TIME_FORMAT}'")
            return None

        return newTime

    return None


def removeNone(val):
    if(not val):
        return ""

    return val


def get_form_values(formData):
    """

    """
    FUNC_NAME = "get_form_values(formData)"

    if(not formData):
        print(f"Error: {FUNC_NAME}: formData is empty")
        return None

    if(not isinstance(formData, list)):
        print(f"Error: {FUNC_NAME}: formData is not a list. formData = {formData}")
        return None


    dataList = copy.deepcopy(formData)

    for row in dataList:

        #If the labels key exists and has data, iterate through the elements requesting the form data
        if('labels' in row):
            for key, val in row['labels'].items():
                row['values'][key] = request.form[row['labels'][key]]

        else:
            #Directly read the 'name' key to get form elements
            row['value'] = request.form[row['name']]


    data = {}

    #Convert list of dicts to dictionary for easier value assignment. Use the value in the 'name' key as the new
        #key for each dict entry
    for row in dataList:
        key = row['name']
        del row['name']
        data[key] = row

    return data




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


#Get the 'edit' argument from the url and check if it is true or false
def get_edit():
    arg = 'edit'

    result = request.args.get(arg, default='false') #Default is a string 'false' not a bool. Keep it this way.

    if(result.lower() == 'true'):
        return True
    else:
        return False


def sql_insert(sql_table, dataList):
    """
    Iterate through the 'dataList', inserting each row of SQL formatted data into the 'sql_table' database

    :param sql_table:
    :param dataList:  A list of dictionaries with data, properties and column names of a SQL table
    :return: A list of the last auto_increment ID of each row inserted. 'None' if the auto_increment ID cannot
    be obtained from the database
    """

    FUNC_NAME = "sql_insert(sql_table, dataList)"

    if(not sql_table):
        print(f"Error: {FUNC_NAME}: TABLE not specified")
        return None

    if(not dataList):
        print(f"Error: {FUNC_NAME}: dataList empty")
        return None

    if(not isinstance(dataList, list)):
        print(f"Error: {FUNC_NAME}: dataList is not a dictionary")
        return None


    IDList = [] #Store the lastrowid for each insertion
    id = None

    for row in dataList:

        colList = []
        valList = []
        escapeList = []

        #Grab dictionary values to create a list of SQL column names and a list of corresponding values
        for key, value in row.items():
            colList.append(key)
            valList.append(value['data'])

        """
        for index, item in enumerate(colList):
            print(f"{item} <> {valList[index]}")
        """

        #Separate list items with commas
        colNames = ', '.join(colList)


        #Create %s placeholder string
        for index in range(len(colList)):
            escapeList.append('%s')

        placeholders = ', '.join(escapeList)

        try:
            dbCon = db.db_connect()
            cursor = dbCon.cursor()

            query = (f"INSERT INTO {sql_table} ({colNames}) VALUES ({placeholders})")

            #print(f"query: {query}")
            #print(f"values: {valList}")

            cursor.execute(query, valList)
            dbCon.commit()


            id = cursor.lastrowid # Get the auto-increment ID. returns 0 if table has no auto_increment

            if not id:
                id = None

            cursor.close()
            dbCon.close()  # return connection to pool


        except db.Error as err:
            print(f"Error: {FUNC_NAME}: Error message: {err}")
            id = None

        IDList.append(id)

    if(len(IDList) == 1):
        return id

    return IDList

def sql_sanitize(valueList):
    """
        Ensure all the incoming data is formatted and truncated for the SQL database
    """
    FUNC_NAME = "sql_sanitize(value)"

    newList = []

    #Duplicate the list
    '''
    for row in valueList:
        newRow = copy.deepcopy(row)
        newList.append(newRow)
    '''
    #Iterate through the list of SQL PROPERTY dictionaries, then iterate through the key:values where the keys
        #correspond to SQL columns. The data to be sanitized is stored the 'data' key of each SQL PROPERTY dict

    for row in valueList:
        newRow = copy.deepcopy(row) #Copy the row as to not alter original

        for key,val in newRow.items():

            dataType = val['dataType']
            data = val['data']
            sizeLimit = val['size']

            enums = None

            if('enums' in val):
                enums = val['enums']

            sizeMin = 0
            sizeMax = 0

            #print(f"data={data}, sizeLimit={sizeLimit}, type={type}")
    
            if(isinstance(sizeLimit, dict)):
                sizeMin = sizeLimit['MIN']
                sizeMax = sizeLimit['MAX']
    
    
            if(dataType == SQL.DATATYPES.VARCHAR):
                data = str(data)
                dataLen = len(data)
    
                if(dataLen > sizeLimit):
                    data = data[0:sizeLimit]
                    print(f'WARNING: {FUNC_NAME}: VARCHAR data of length={dataLen} truncated to {sizeLimit} characters')
    
            elif(dataType == SQL.DATATYPES.TEXT):
                data = str(data)
                dataLen = len(data)
    
                if(dataLen > sizeLimit):
                    data = data[0:sizeLimit]
                    print(f'WARNING: {FUNC_NAME}: TEXT data of length={dataLen} truncated to {sizeLimit} characters')
    
    
            elif(dataType == SQL.DATATYPES.TINY_INT):
                data = toInt(data)
                data = compare_int_size(data, sizeMin, sizeMax)
    
    
            elif(dataType == SQL.DATATYPES.SMALL_INT):
                data = toInt(data)
                data = compare_int_size(data, sizeMin, sizeMax)
    
            elif(dataType == SQL.DATATYPES.INT):
                data = toInt(data)
                data = compare_int_size(data, sizeMin, sizeMax)

    
            elif(dataType == SQL.DATATYPES.DATETIME):
    
                data = toStr(data)
    
                # Attempt to convert from string to a date time object using one of two SQL formats
                try:
                    data = datetime.strptime(data, SQL.DATETIME_FORMAT)
    
                except ValueError as e:
                    print(f"Warning {FUNC_NAME}: {e}. Trying alternate date format.")
    
                    try:
                        data = datetime.strptime(data, SQL.DATETIME_FORMAT_U)
    
                    except ValueError as e:
                        print(f"Warning {FUNC_NAME}: {e}. Returning None type.")
                        data = None
    
            elif(dataType == SQL.DATATYPES.TIME):
                data = toStr(data)
    
                try:
                    data = datetime.strptime(data, HTML_TIME_FORMAT)
    
                except ValueError as e:
                    print(f"Warning {FUNC_NAME}: {e}. Trying alternate time format.")
    
                    try:
    
                        data = datetime.strptime(data, HTML_TIME_FORMAT_S)
    
                    except ValueError as e:
                        print(f"Warning {FUNC_NAME}: {e}. Returning None type.")
                        data = None
    
    
            elif(dataType == SQL.DATATYPES.ENUM):
                #Checking to ensure passed enum exists in passed dict
    
                if (data not in enums):
                    print(f"Error: {FUNC_NAME}: Could not find item={data} in enumeration list={enums}")
                    data = None

            elif(dataType == SQL.DATATYPES.VARCHAR_DECIMAL):
                data = toStr(data)

                try:
                    decimal.Decimal(data)

                except decimal.InvalidOperation as e:
                    print(f"Error: {FUNC_NAME}: Could not convert {data} to Decimal")
                    data = None

            else:
                data = None


            newRow[key]['data'] = data

        newList.append(newRow)


    return newList

def compare_int_size(integer, min, max):
    funcName = "compare_int_size(integer, min, max)"
    fallback = None

    val = integer

    if(not isinstance(integer, int)):
        return fallback

    if(integer < min):
        val = fallback
        print(f"Error: {funcName}: integer={integer} less than mininum size={min}. Returning {fallback}")

    elif(integer > max):
        val = fallback
        print(f"Error: {funcName}: integer={integer} greater than max size={max}. Returning {fallback}")

    return val

def toInt(val):
    funcName = "toInt(val)"

    try:
        val = int(val)
        return val

    except ValueError as e:
        print(f"Warning: {funcName}: Cannot cast val={val} to integer. Error message: {e}")
        return None


def toStr(val):
    funcName = "toStr(val)"

    try:
        val = str(val)
        return val

    except ValueError as e:
        print(f"Error: {funcName}: Cannot cast val={val} to string. Error msg: {e}")
        return None

