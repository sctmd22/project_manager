from datetime import datetime
from GLOBALS import *
from flask import request
import db as db



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




def get_form_values(formList):
    """
    Iterate through a list of HTML form elements and return a dict containing all the elementName:value
    """

    FUNC_NAME = "get_form_values(formList)"


    data = {}

    if(not formList):
        print(f"Error: {FUNC_NAME}: formList is empty")
        return None

    if(not isinstance(formList, list)):
        print(f"Error: {FUNC_NAME}: formList is not a list")
        return None

    for element in formList:
        data[element] = request.form[element]

    return data


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
            #Defaults for anywhere the key value is not true
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


#Get the 'edit' argument from the url and check if it is true or false
def get_edit():
    arg = 'edit'

    result = request.args.get(arg, default='false') #Default is a string 'false' not a bool. Keep it this way.

    if(result.lower() == 'true'):
        return True
    else:
        return False




def sql_insert(sql_table, columns, values):
    """
    Insert values into corresponding columns of a SQL table

    sql_table:  The SQL table name to insert data into
    columns:    A list of the SQL column names
    values:     A list of values corresponding to the column names
    """
    FUNC_NAME = "sql_insert()"

    if(not sql_table):
        print(f"Error: {FUNC_NAME}: TABLE is None")
        return -1

    if(not columns):
        print(f"Error: {FUNC_NAME}: columns argument is None")
        return -1

    if(not values):
        print(f"Error: {FUNC_NAME}: values argument is None")
        return -1

    if(not isinstance(columns, list)):
        print(f"Error: {FUNC_NAME}: columns={columns} is not a list")
        return -1

    if (not isinstance(values, list)):
        print(f"Error: {FUNC_NAME}: values={values} is not a list")
        return -1

    if(len(columns) != len(values)):
        print(f"Error: {FUNC_NAME}: values={values} and columns={columns} are not equal length")
        return -1


    #Separate list items with commas
    valueString = ', '.join(columns)


    valueList = []
    #Create %s string for values
    for index in range(len(columns)):
        valueList.append('%s')

    valueList = ', '.join(valueList)

    try:
        dbCon = db.db_connect()
        cursor = dbCon.cursor()

        QUERY = (f"INSERT INTO {sql_table} ({valueString}) VALUES ({valueList})")

        cursor.execute(QUERY, values)
        dbCon.commit()

        # Get the auto-increment ID
        id = cursor.lastrowid

        cursor.close()
        dbCon.close()  # return connection to pool

        return id

    except:
        print(f"Error: {FUNC_NAME}: Could not submit into sql_table={sql_table} where columns={columns} and values={values}")
        return -1



def sql_sanitize(value):
    """
        Ensure all the incoming data is formatted and truncated for the SQL database
        value: A dictionary with three keys: [data], [dataType], [size]
                    data:       The data to be formatted
                    dataType:   Enumerable which contains the SQL data type
                    size:       For VARCHARS or TEXT types: The max number of characters the data can be
                                For INT types:  Contains a dict with the [min] and [max] size the int can be
    """
    FUNC_NAME = "sql_sanitize(value)"

    type = value['dataType']
    data = value['data']


    if(type == db.SQL_DATATYPES.VARCHAR):
        sizeLimit = value['size']
        data = str(data)
        dataLen = len(data)

        if(dataLen > sizeLimit):
            data = data[0:sizeLimit]
            print(f'WARNING: {FUNC_NAME}: VARCHAR data of length={dataLen} truncated to {sizeLimit} characters')

    elif(type == db.SQL_DATATYPES.TEXT):
        sizeLimit = value['size']
        data = str(data)
        dataLen = len(data)

        if(dataLen > sizeLimit):
            data = data[0:sizeLimit]
            print(f'WARNING: {FUNC_NAME}: TEXT data of length={dataLen} truncated to {sizeLimit} characters')


    elif(type == db.SQL_DATATYPES.TINY_INT):
        minSize = value['size']['min']
        minSize = value['size']['max']


    elif(type == db.SQL_DATATYPES.SMALL_INT):

        pass

    elif(type == db.SQL_DATATYPES.INT):

        pass


    elif(type == db.SQL_DATATYPES.DATETIME):
        pass
    elif(type == db.SQL_DATATYPES.TIME):
        pass
    elif(type == db.SQL_DATATYPES.ENUM):
        pass
    else:
        pass


    return data
