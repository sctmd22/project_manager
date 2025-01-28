import copy
from datetime import datetime
from sys import exception

from werkzeug.exceptions import BadRequestKeyError

from GLOBALS import *
from flask import request
import decimal
import db as db

from db import sql_data as SQL


def get_form_values(formData):
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
                try:
                    row['valData'][key] = request.form[row['labels'][key]]
                except BadRequestKeyError as e:
                    print(f"Error: {FUNC_NAME}: Could not request HTML element where name = {row['labels'][key]}")

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


def sql_delete(sql_table, delID):
    """

    :param sql_table: The name of the SQL table to delete data from
    :param delID: Either a single ID or a list of ID's which correspond to the SQL auto_id field
    :return:
    """
    FUNC_NAME = "sql_delete(sql_table, idList)"

    if(not sql_table):
        print(f"Error: {FUNC_NAME}: TABLE not specified")
        return False

    if(isinstance(delID, int)):
        __sql_delete_item(sql_table, delID)
        return True

    elif(isinstance(delID, tuple) or isinstance(delID, list)):
        for id in delID:
            __sql_delete_item(sql_table, id)

        return True

    else:
        return False


def __sql_delete_item(sql_table, id):
    dbCon = db.db_connect()
    cursor = dbCon.cursor()

    SQL_PROJECT_GET = (f"DELETE FROM {sql_table} WHERE auto_id = %s")

    # Sending query as a tuple to reduce the risk of SQL injection
    values = (id,)
    cursor.execute(SQL_PROJECT_GET, values)

    dbCon.commit()

    cursor.close()
    dbCon.close()  # return connection to pool



def sql_update(sql_table, dataListIn):
    """
       Iterate through the 'dataListIn',  updating each row of SQL formatted data of the 'sql_table' database

       :param sql_table: The name of the SQL table to update
       :param dataList:  A list of dictionaries with data, properties and column names of a SQL table
       :return: True if successful, otherwise False
       """

    FUNC_NAME = "sql_update(sql_table, dataListIn)"

    if (not sql_table):
        print(f"Error: {FUNC_NAME}: TABLE not specified")
        return None

    if (not dataListIn):
        print(f"Error: {FUNC_NAME}: dataListIn empty")
        return None

    if (not isinstance(dataListIn, list)):
        print(f"Error: {FUNC_NAME}: dataListIn is not a dictionary")
        return None

    #Make a copy of dataList
    dataList = copy.deepcopy(dataListIn)

    autoIDData = None

    returnVal = True

    for row in dataList:
        colList = []
        valList = []

        try:
            autoIDData = row.pop('auto_id')  # Remove and get autoID value
            autoIDVal = autoIDData['data']

        except KeyError as e:
            print(f"Error: {FUNC_NAME}: key does not exist in dataList where key={e}")
            returnVal = False
            break


        # Grab dictionary values to create a list of SQL column names and a list of corresponding values
        for key, value in row.items():
            keyString = key + " = %s"
            colList.append(keyString)
            valList.append(value['data'])


        valList.append(autoIDVal)

        # Separate list items with placeholder
        colNames = ', '.join(colList)

        try:
            dbCon = db.db_connect()
            cursor = dbCon.cursor()

            query = (f"UPDATE {sql_table} SET {colNames} WHERE auto_id = %s")

            cursor.execute(query, valList)
            dbCon.commit()

            cursor.close()
            dbCon.close()  # return connection to pool


        except db.Error as err:
            print(f"Error: {FUNC_NAME}: Error message: {err}")
            returnVal = False

    return returnVal


def sql_insert(sql_table, dataList):
    """
    Iterate through the 'dataList', inserting each row of SQL formatted data into the 'sql_table' database

    :param sql_table: The name of the SQL table to insert into
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

        #print(f"SANITIZE ROW: {newRow}")

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
                success = False

                # Attempt to convert from string to a date time object using several formats
                if(data):
                    for format in DATE_FORMATS:
                        try:
                            data = datetime.strptime(data, format.value)

                        except ValueError:
                            continue

                        else:
                            success = True
                            break

                if(not success):
                    print(f"Warning: {FUNC_NAME}: data={data} could not be formatted to a datetime object")
                    data = None


            elif(dataType == SQL.DATATYPES.TIME):
                data = toStr(data)
                success = False

                # Attempt to convert from string to a date time object using several formats
                if (data):
                    for format in TIME_FORMATS:
                        try:
                            data = datetime.strptime(data, format.value)

                        except ValueError:
                            continue

                        else:
                            success = True
                            break

                if (not success):
                    print(f"Warning: {FUNC_NAME}: data={data} could not be formatted to a datetime object")
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

    if(not val):
        return None

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



def replaceNone(noneData):
    """
    Replace all instances of None with the returnType ('')

    :param noneData: Any data which may contain None types
        1. A single variable
        2. A dictionary or nested dictionary
        3. A list of dictionaries
    :return: A copy of the input data with None replaced with the returnType
    """
    returnType = ''

    if(noneData == None):
        return returnType

    elif(isinstance(noneData, dict)):
        newDict = copy.deepcopy(noneData)

        return replaceNoneDict(newDict, returnType)

    elif(isinstance(noneData, list)):
        newList = []

        for row in noneData:
            newRow = copy.deepcopy(row)
            replaced = replaceNoneDict(newRow, returnType)
            newList.append(replaced)

        return newList

    else:
        return noneData


def replaceNoneDict(data, returnType):
    """
    :param dataDict:     Recursively iterate through a dictionary, setting all values of None to ''
        Dictionary (or list of dicts) with key:values containing None data
    :return: A copy of dataDict
    """

    if(data == None):
        return returnType

    elif(isinstance(data, dict)):
        for key, val in data.items():
            data[key] = replaceNoneDict(data[key], returnType)

    return data



def capitalizeFirst(val):
    if(not val):
        return ''

    if(not isinstance(val, str)):
        return val

    return val[:1].upper() + val[1:]

