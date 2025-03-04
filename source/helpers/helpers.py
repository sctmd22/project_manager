import copy
from datetime import datetime, timedelta
from sys import exception
from time import strptime

from werkzeug.exceptions import BadRequestKeyError

import GLOBALS as GB
from flask import request
import decimal
import db as db

from db import sql_data as SQL

MODULE_NAME = "helpers"

def get_form_values(formData):
    '''
    Iterate through the 'label' keys of formData, using the labels as parameters to request data from the submitted
    form. With the requested form data, update the 'val' key's in formData

    formData layout:
    [
        Row 1:
        {   'name':...,
            'title':...,
            'dataFields': {
                <FIELD1>: {'label':VALUE, 'val':VALUE, 'dataType':VALUE, 'size':{...}, 'errorLabel':VALUE},
                <FIELD2>: {'label':VALUE, 'val':VALUE, 'dataType':VALUE, 'size':{...}, 'errorLabel':VALUE},
                ....
                },
        }

        Row 2:
        {   'name':...,
            'title':...,
            'dataFields': {
                <FIELD1>: {'label':VALUE, 'val':VALUE, 'dataType':VALUE, 'size':{...}, 'errorLabel':VALUE},
                <FIELD2>: {'label':VALUE, 'val':VALUE, 'dataType':VALUE, 'size':{...}, 'errorLabel':VALUE},
                ....
                },
        }
        Row n...
    ]

    :param formData: A list of FORM data (formatted to the FORM template style)
    :return: The same FORM data as a dictionary, where the NAME is the key to each sub-dictioanry
    '''
    FUNC_NAME = "get_form_values(formData)"

    if(not formData):
        print(f"Error: {FUNC_NAME}: formData is empty")
        return None

    dataList = []

    if(isinstance(formData, dict)):
        dataList.append(copy.deepcopy(formData))

    elif (isinstance(formData, list)):
        dataList = copy.deepcopy(formData)

    else:
        print(f"Error: {FUNC_NAME}: formData is not a list or dict. Returning None. formData = {formData}")
        return None

    for row in dataList:
        dataFields = row['dataFields']

        for key, val in dataFields.items():
            if('label' in val):
                try:
                    val['val'] = request.form[val['label']]
                except BadRequestKeyError as e:
                    print(f"Error: {FUNC_NAME}: Could not request HTML element where name = {val['label']}")


    data = {}

    #Convert list of dicts to dictionary for easier value assignment. Use the value in the 'name' key as the new
        #key for each dict entry
    '''
    for row in dataList:
        key = row['name']
        del row['name']
        data[key] = row
    '''

    return dataList

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
    Take an ID or list of ID's corresponding to the SQL auto_id field in the SQL table sql_table and remove each entry

    :param sql_table: The name of the SQL table to delete data from
    :param delID: Either a single ID or a list of ID's which correspond to the SQL auto_id field
    :return: Number of items deleted. 0 if none or error
    """
    FUNC_NAME = "sql_delete(sql_table, idList)"

    numRows = 0

    if(not sql_table):
        print(f"Error: {FUNC_NAME}: TABLE not specified")
        return 0

    if(isinstance(delID, int)):
        return __sql_delete_item(sql_table, delID)

    elif(isinstance(delID, tuple) or isinstance(delID, list)):
        for id in delID:
            numRows += __sql_delete_item(sql_table, id)

        return numRows
    else:
        return 0

def __sql_delete_item(sql_table, id):
    FUNC_NAME = "__sql_delete_item(sql_table, id):"

    try:
        dbCon = db.db_connect()
        cursor = dbCon.cursor()

        SQL_PROJECT_GET = (f"DELETE FROM {sql_table} WHERE auto_id = %s")

        # Sending query as a tuple to reduce the risk of SQL injection
        values = (id,)
        cursor.execute(SQL_PROJECT_GET, values)

        numRows = cursor.rowcount

        if(numRows):
            print(f"Info: {FUNC_NAME}: Deleted {numRows} row from table='{sql_table}' where auto_id={id}")

        dbCon.commit()

        cursor.close()
        dbCon.close()  # return connection to pool

        return numRows

    except db.Error as e:
        print(f"Error: {FUNC_NAME}: {e}")
        return 0

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

def parseDate(data, ENUMS):
    '''
        Convert a string to a datetime object

    :param date:
    :return:
    '''

    FUNC_NAME = MODULE_NAME + ".parseDate(data, ENUMS)"

    if(not data):
        print(f"Warning: {FUNC_NAME}: data={data} is false")
        return None

    if(not isinstance(data, str)):
        data = toStr(data)

    success = False

    # Attempt to convert from string to a date time object using several formats
    if (data):
        for format in ENUMS:
            try:
                data = datetime.strptime(data, format.value)

            except ValueError:
                continue

            else:
                success = True
                return data

    if (not success):
        print(f"Warning: {FUNC_NAME}: data={data} could not be formatted to a datetime object")

    return None

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
                data = parseDate(data, GB.DATE_FORMATS)


            elif(dataType == SQL.DATATYPES.TIME):
                data = toStr(data)
                data = parseDate(data, GB.TIME_FORMATS)

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

            elif(dataType == SQL.DATATYPES.BOOL):
                data = toInt(data)

                if(not (data == 0 or data == 1)):
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


def processSql(sqlData):
    """
    1. Replace all instances of None with the returnType ('')
    2. Stringify timedeltas (need to do this for json serialization)

    :param sqlData: Any data which may contain None types
        1. A single variable
        2. A dictionary or nested dictionary
        3. A list of dictionaries/nested dictionaries
    :return: A copy of the input data with None replaced with the returnType
    """
    returnType = ''

    if(sqlData == None):
        return returnType

    elif(isinstance(sqlData, dict)):
        newDict = copy.deepcopy(sqlData)

        return __replaceNoneDict(newDict, returnType)

    elif(isinstance(sqlData, list)):
        newList = []

        for row in sqlData:
            newRow = copy.deepcopy(row)
            replaced = __replaceNoneDict(newRow, returnType)
            newList.append(replaced)

        return newList

    else:
        return sqlData

def __replaceNoneDict(data, returnType):
    """
    :param dataDict:     Recursively iterate through a dictionary, setting all values of None to ''
        Dictionary (or list of dicts) with key:values containing None data
    :return: A copy of dataDict
    """

    if(data == None):
        return returnType

    elif(isinstance(data, timedelta)):
        #print(f"Found timedelta = {data}. Converting to string = {str(data)}")
        return str(data)

    elif(isinstance(data, dict)):
        for key, val in data.items():
            data[key] = __replaceNoneDict(data[key], returnType)

    return data

def capitalizeFirst(val):
     #Capitalize the first letter of the passed string
    if(not val):
        return ''

    if(not isinstance(val, str)):
        return val

    return val[:1].upper() + val[1:]

def generateBreadcrumbs():
    '''
    Generate a breadcrumb trail to be displayed in the upper right portion of the web-app
    :return: A list of dictionaries containing HTML elements and properties to build the breadcrumb links
    '''
    root = request.url_root
    url = request.path  #Returns '/' for root

    # Remove leading and trailing '/', then split into a list using '/' as a separator
        #Returns a list with one empty string for root
    segments = url.strip('/').split('/')

    homePath = 'home' #Arbitrary name

    if(segments[0] == ''):     #Either re-assign or insert the homePath into the list of url items
        segments[0] = homePath
    else:
        segments.insert(0, homePath)


    template = {'activeClass':'', 'url':'', 'href':'', 'title':'', 'aria':'', 'nav-item':'', 'nav-link':''}

    breadCrumbsList = []


    for i, item in enumerate(segments):
        data = template.copy()

        #Leave root as is for home, otherwise concatenate root with item, where item is part of the url path
        if(not (item == "home")):
            root = root + item + '/'

        data['url'] = root.strip('/')   #Remove the last '/' character, otherwise invalid url

        data['title'] = capitalizeFirst(item)

        data['href'] = f'<a href="{data['url']}">{data['title'] }</a>'

        #Remove the link/<a href></a> and apply necessary properties to last element
        if(i == len(segments)-1):
            data['activeClass'] = ' active'
            data['aria'] = 'aria-current=page'
            data['href'] = data['title']

        breadCrumbsList.append(data)

    return breadCrumbsList

def dateToStr(date, format):
    '''
    Convert a datetime object to a string in the specified format

    :param date: A datetime object
    :param format: A string of date formatting options
    :return: The formatted date string
    '''
    FUNC_NAME = "dateToStr(date, format)"

    if(not isinstance(date, datetime)):
        print(f"Error: {FUNC_NAME}: date={date} is not a datetime object")
        return ''

    try:
        newDate = date.strftime(format)
        return newDate

    except:
        print(f"Error: {FUNC_NAME}: Could not format date={date} is not a datetime object")
        return date


def listToDict():
    pass

