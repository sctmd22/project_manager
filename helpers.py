from _datetime import datetime

GLB_project_status = {
    0: "Active",
    1: "Complete",
    2: "Deleted",
    3: "Canceled"
}

SQL_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
SIMPLE_DATE_FORMAT = '%Y-%m-%d'

def get_SQL_timestamp():
    return datetime.today().strftime(SQL_TIME_FORMAT)


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

    #Zip the data (typles and lists) to create a list of tuples to be added to the mysql database in one query
    str_table_data = list(zip(idList, strList, daysList))

    return str_table_data

def convertToInt(list):
    newList = []
    for i in range(len(list)):
        try:
            newList.append(int(list[i]))
        except:
            return list

    return newList