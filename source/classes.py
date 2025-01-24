from datetime import datetime
from helpers import helpers as HLP
import db as db
import copy

from db import sql_data as SQL
from helpers.helpers import replaceNone


class Reports:
    STATUS_TABLE = {
        'active': "Active",
        'complete': "Complete",
        'deleted': "Deleted",
        'canceled': "Canceled"
    }



    @classmethod
    def sql_fetchone(cls, query, values=None):
        FUNC_NAME = "__sql_fetchone()"
        try:
            dbCon = db.db_connect()
            cursor = dbCon.cursor(dictionary=True)

            if (values):
                cursor.execute(query, values)
            else:
                cursor.execute(query)

            result = cursor.fetchone()

            cursor.close()
            dbCon.close()  # return connection to pool

            return result

        except:
            print(f"Error: {FUNC_NAME}: Could not process provided query and or values")
            return None


    @classmethod
    def sql_fetchall(cls, query, values=None):
        func_name = "__sql_fetchall()"
        try:
            dbCon = db.db_connect()
            cursor = dbCon.cursor(dictionary=True)

            if (values):
                cursor.execute(query, values)
            else:
                cursor.execute(query)

            result = cursor.fetchall()

            cursor.close()
            dbCon.close()  # return connection to pool

            return result

        except:
            print(f"Error: {func_name}: Could not process provided query and or values")
            return None



    #Return a blank string if val is False/None
    @classmethod
    def remove_none(cls, val):
        if(not val):
            return ""

        return val


class CylinderReport(Reports):
    #Number of cylinder strength targets
    NUM_STR_TARGETS = 5

    TB_REPORT_DATA = "cyl_report_data"
    TB_STR_REQ = "cyl_str_req"
    TB_CYLINDERS = "cyl_items"
    TB_CONDITIONS = "cyl_conditions_table"

    SCC_OPTIONS = {
        'yes': 'Yes',
        'no': 'No'
    }

    MOULD_OPTIONS = {
        '100x200_plastic': '100x200 Plastic',
        '150x300_plastic': '150x300 Plastic'
    }

    UNITS_OPTIONS = {
        'meters': 'm',
        'yards': 'yd'
    }

    FORM_FIELD_TEMPLATE = [
        {'name': 'cylinderID',          'title': ''},
        {'name': 'dateCreated',         'title': ''},
        {'name': 'createdBy',           'title': ''},
        {'name': 'cylTitle',            'title': ''},
        {'name': 'cylStatus',           'title': ''},
        {'name': 'cylProject',          'title': ''},
        {'name': 'cylTicket',           'title': ''},
        {'name': 'cylSupplier',         'title': ''},
        {'name': 'cylLoadNum',          'title': ''},
        {'name': 'cylTruckNum',         'title': ''},
        {'name': 'cylContractor',       'title': ''},
        {'name': 'cylSampled',          'title': ''},
        {'name': 'cylMix',              'title': ''},
        {'name': 'cylMouldType',        'title': ''},
        {'name': 'cylPONum',            'title': ''},
        {'name': 'cylPlacement',        'title': ''},
        {'name': 'cylCement',           'title': ''},
        {'name': 'cylVolume',           'title': ''},
        {'name': 'cylVolumeUnits',      'title': ''},
        {'name': 'cylCastDate',         'title': ''},
        {'name': 'cylCastTime',         'title': ''},
        {'name': 'cylBatchTime',        'title': ''},
        {'name': 'cylSampleTime',       'title': ''},
        {'name': 'cylDateTransported',  'title': ''},
        {'name': 'cylNotes',            'title': ''},
        {'name': 'cylSCC',              'title': ''},

    ]


    STR_LABELS = {
        'strength':'Strength',
        'days':'Days',
        'id':'ID'
    }

    #Template for the HTML strength table which gets repeated X number of times
    #'labels' and 'valData' are used for writing to HTML data and reading HTML forms
        #When the table is built it will look like: {'name':'str',   'title':'Target {n}',   'labels':{'strength':'strStrength', 'days':'strDays', 'id':'strID'}, 'valData':{'strength':'', 'days', 'id':''}}
    FORM_STR_TEMPLATE = {
        'name':'strTable',   'title':'Target {n}',   'labels': {},    'valData':{}
    }


    CONDITIONS_LABELS = {
        'actual':'Actual',
        'min':'Min',
        'max':'Max',
        'notes':'Notes',
        'id':'ID'
    }


    #Template for field/measurement data and properties
    #When the table is built, one entry will look like:
        #{'name':'cylConFlow', 'property':'flow', 'SCC':True, 'CYL':False, 'labels':{'actual':'cylConFlowActual', 'min':'cylConFlowMin', ...etc}, 'data':{'actual':'', 'min':'', 'max':'', 'notes':'', 'id':''}}
    FORM_CONDITIONS_TEMPLATE = [
        {'name':'cylConFlow',               'title':'Flow (mm)',                           'property':'flow',           'SCC':True, 'CYL': False,   'labels':{}, 'valData':{}},
        {'name':'cylConT50',                'title':'T<sub>50</sub>(s)',                   'property':'t_50',           'SCC':True, 'CYL': False,   'labels':{}, 'valData':{}},
        {'name':'cylConVSI',                'title':'VSI',                                 'property':'vsi',            'SCC':True, 'CYL': False,   'labels':{}, 'valData':{}},
        {'name':'cylConSlump',              'title':'Slump (mm)',                          'property':'slump',          'SCC':False, 'CYL':True,    'labels':{}, 'valData':{}},
        {'name':'cylConAir',                'title':'Air (%)',                             'property':'air',            'SCC':True, 'CYL':True,     'labels':{}, 'valData':{}},
        {'name':'cylConDensity',            'title':'Unit Density (kg/m<sup>3</sup>)',     'property':'density',        'SCC':True, 'CYL': True,    'labels':{}, 'valData':{}},
        {'name':'cylConSampleTemp',         'title':'Sample Temp (&deg;C)',                'property':'sampleTemp',     'SCC':True, 'CYL': True,    'labels':{}, 'valData':{}},
        {'name':'cylConAmbientTemp',        'title':'Ambient Temp (&deg;C)',               'property':'ambientTemp',    'SCC':True, 'CYL': True,    'labels':{}, 'valData':{}},
        {'name':'cylConInitialTemp',        'title':'Initial Curing Conditions (&deg;C)',  'property':'initialTemp',    'SCC':True, 'CYL': True,    'labels':{}, 'valData':{}},
    ]

    '''-------------------------------------SQL DATA-------------------------------------'''

    SQL_STR_REQ_PROPERTIES = {
        'cyl_report_id':      {'dataType': SQL.DATATYPES.INT,     'size':SQL.INT_SIZES['INT']},
        'target_strength':    {'dataType': SQL.DATATYPES.INT,     'size':SQL.INT_SIZES['INT']},
        'target_days':        {'dataType': SQL.DATATYPES.INT,     'size':SQL.INT_SIZES['INT']}
    }



    SQL_CONDITIONS_PROPERTIES = {
        'cyl_report_id':           {'dataType': SQL.DATATYPES.INT,              'size': SQL.INT_SIZES['INT']},
        'property':                {'dataType': SQL.DATATYPES.VARCHAR,          'size': 255},
        'val_actual':              {'dataType': SQL.DATATYPES.VARCHAR_DECIMAL,  'size': 15},
        'val_min':                 {'dataType': SQL.DATATYPES.VARCHAR_DECIMAL,  'size': 15},
        'val_max':                 {'dataType': SQL.DATATYPES.VARCHAR_DECIMAL,  'size': 15},
        'notes':                   {'dataType': SQL.DATATYPES.VARCHAR,          'size': 1000}
    }

    """ 'val_actual_precision':    {'dataType': SQL.DATATYPES.TINY_INT, 'size': SQL.INT_SIZES['TINY_INT']},
        'val_min_precision':       {'dataType': SQL.DATATYPES.TINY_INT, 'size': SQL.INT_SIZES['TINY_INT']},
        'val_max_precision':       {'dataType': SQL.DATATYPES.TINY_INT, 'size': SQL.INT_SIZES['TINY_INT']},"""



    SQL_REPORT_PROPERTIES = {
        'project_id':                  {'dataType': SQL.DATATYPES.INT,         'size': SQL.INT_SIZES['INT']},
        'date_created':                {'dataType': SQL.DATATYPES.DATETIME,    'size': None},
        'created_by':                  {'dataType': SQL.DATATYPES.VARCHAR,     'size': 50},
        'report_title':                {'dataType': SQL.DATATYPES.VARCHAR,     'size': 255},
        'status':                      {'dataType': SQL.DATATYPES.ENUM,        'size': None, 'enums': Reports.STATUS_TABLE},
        'is_scc':                      {'dataType': SQL.DATATYPES.ENUM,        'size': None, 'enums': SCC_OPTIONS},
        'ticket_num':                  {'dataType': SQL.DATATYPES.VARCHAR,     'size': 50},
        'project_name':                {'dataType': SQL.DATATYPES.VARCHAR,     'size': 50},
        'supplier':                    {'dataType': SQL.DATATYPES.VARCHAR,     'size': 50},
        'load_num':                    {'dataType': SQL.DATATYPES.VARCHAR,     'size': 50},
        'truck_num':                   {'dataType': SQL.DATATYPES.VARCHAR,     'size': 50},
        'contractor':                  {'dataType': SQL.DATATYPES.VARCHAR,     'size': 50},
        'sampled_from':                {'dataType': SQL.DATATYPES.VARCHAR,     'size': 50},
        'mould_type':                  {'dataType': SQL.DATATYPES.ENUM,        'size': None, 'enums': MOULD_OPTIONS},
        'mix_id':                      {'dataType': SQL.DATATYPES.VARCHAR,     'size': 50},
        'po_num':                      {'dataType': SQL.DATATYPES.VARCHAR,     'size': 50},
        'placement_type':              {'dataType': SQL.DATATYPES.VARCHAR,     'size': 50},
        'cement_type':                 {'dataType': SQL.DATATYPES.VARCHAR,     'size': 50},
        'load_volume':                 {'dataType': SQL.DATATYPES.VARCHAR,     'size': 50},
        'load_volume_units':           {'dataType': SQL.DATATYPES.ENUM,        'size': None, 'enums': UNITS_OPTIONS},
        'date_cast':                   {'dataType': SQL.DATATYPES.DATETIME,    'size': None},
        'time_batch':                  {'dataType': SQL.DATATYPES.TIME,        'size': None},
        'time_sample':                 {'dataType': SQL.DATATYPES.TIME,        'size': None},
        'time_cast':                   {'dataType': SQL.DATATYPES.TIME,        'size': None},
        'date_transported':            {'dataType': SQL.DATATYPES.DATETIME,    'size': None},
        'notes':                       {'dataType': SQL.DATATYPES.TEXT,        'size': SQL.TEXT_SIZES['TEXT']}
    }



    #Constructor
    def __init__(self, data):
        self.id = data['id']
        self.date_created = data['dateCreated']
        self.title = data['title']
        self.status = data['status']
        self.project_name = data['projectName']
        self.ticket_num = data['ticketNum']
        self.supplier = data['supplier']
        self.load_num = data['loadNum']
        self.truck_num = data['truckNum']
        self.contractor = data['contractor']
        self.sampled_from = data['sampledFrom']
        self.mix_ID = data['mixId']
        self.mould_type = data['mouldType']
        self.po_num = data['poNum']
        self.placement_type = data['placementType']
        self.cement_type = data['cementType']
        self.load_volume = data['loadVolume']
        self.load_volume_units = data['loadVolumeUnits']
        self.date_cast = data['dateCast']
        self.batch_time = data['batchTime']
        self.sample_time = data['sampleTime']
        self.cast_time = data['castTime']
        self.date_transported = data['dateTransported']
        self.notes = data['notes']
        self.is_scc = data['isSCC']
        self.created_by = data['createdBy']

        self.strength_table = data['strTable']
        self.conditions_table = data['conditionsTable']

        self.submitted_id = -1

    #Create a new cylinder report with default values
    @classmethod
    def create_default(cls):
        id = -1
        createdby = 'admin'

        #Create data tables from templates
        strTable = cls.__create_data_n_table(id, cls.FORM_STR_TEMPLATE, cls.STR_LABELS, cls.NUM_STR_TARGETS)
        conTable = cls.__create_data_table(id, cls.FORM_CONDITIONS_TEMPLATE, cls.CONDITIONS_LABELS)

        defaultData = {
            "id": id,
            "dateCreated": datetime.today(),
            "title": "Report Title",
            "status": "active",
            "projectName": "",
            "ticketNum": "",
            "supplier": "",
            "loadNum": "",
            "truckNum": "",
            "contractor": "",
            "sampledFrom": "",
            "mixId": "",
            "mouldType": list(cls.MOULD_OPTIONS.keys())[0],   #Get keys from dict, convert to list, get 0th item
            "poNum": "",
            "placementType": "",
            "cementType": "",
            "loadVolume": "",
            "loadVolumeUnits": "meters",
            "dateCast": "",
            "batchTime": "",
            "sampleTime": "",
            "castTime": "",
            "dateTransported": "",
            "notes": "",
            "isSCC": "no",
            "createdBy": createdby,

            "strTable": strTable,
            "conditionsTable": conTable
        }

        #Call the CylinderReport constructor to create a class instance with the default data
        return cls(defaultData)

    @classmethod
    def create_from_db(cls, id, editing):
        strTable = cls.__create_data_n_table(id, cls.FORM_STR_TEMPLATE, cls.STR_LABELS, cls.NUM_STR_TARGETS)
        conTable = cls.__create_data_table(id, cls.FORM_CONDITIONS_TEMPLATE, cls.CONDITIONS_LABELS)

        #Get database values
        report_sql = super().sql_fetchone(f"SELECT * FROM {cls.TB_REPORT_DATA} WHERE auto_id = %s", (id,)) #The (id,) is a tuple of values which corresponds to %s
        str_sql = super().sql_fetchall(f"SELECT * FROM {cls.TB_STR_REQ} WHERE cyl_report_id = %s ORDER BY auto_id ASC", (id,))
        con_sql = super().sql_fetchall(f"SELECT * FROM {cls.TB_CONDITIONS} WHERE cyl_report_id = %s ORDER BY auto_id ASC", (id,))

        str_result = cls.__sql_to_html_strength(str_sql, strTable, editing)
        con_result = cls.__sql_to_html_con(con_sql, conTable)


        # Prevent HTML errors from None types being in time inputs
        batchTime = super().remove_none(report_sql['time_batch'])
        sampleTime = super().remove_none(report_sql['time_sample'])
        castTime = super().remove_none(report_sql['time_cast'])

        data = {
            "id": report_sql['auto_id'],
            "dateCreated": report_sql['date_created'],
            "title": report_sql['report_title'],
            "status": report_sql['status'],
            "projectName": report_sql['project_name'],
            "ticketNum": report_sql['ticket_num'],
            "supplier": report_sql['supplier'],
            "loadNum": report_sql['load_num'],
            "truckNum": report_sql['truck_num'],
            "contractor": report_sql['contractor'],
            "sampledFrom": report_sql['sampled_from'],
            "mixId": report_sql['mix_id'],
            "mouldType": report_sql['mould_type'],
            "poNum": report_sql['po_num'],
            "placementType": report_sql['placement_type'],
            "cementType": report_sql['cement_type'],
            "loadVolume": report_sql['load_volume'],
            "loadVolumeUnits": report_sql['load_volume_units'],
            "dateCast": report_sql['date_cast'],
            "batchTime": batchTime,
            "sampleTime": sampleTime,
            "castTime": castTime,
            "dateTransported": report_sql['date_transported'],
            "notes": report_sql['notes'],
            "isSCC": report_sql['is_scc'],

            "createdBy": "admin",

            "strTable": str_result,
            "conditionsTable": con_result,

        }

        return cls(data)

    @classmethod
    def __create_data_n_table(cls, id, templateRow, keyNames, n):
        dataList = []

        startVal = 1  #Start at 0 or 1

        for i in range(n):
            index = str(i + startVal)
            data = copy.deepcopy(templateRow)
            data['title'] = data['title'].replace('{n}', index)   #Replace any instances of {n} in 'title' with index

            name = data['name']
            data['name'] = name + index

            #Iterate through labels and assign/concatenate names to the 'labels' and 'valData' subdicts
                # Using the keys from 'keyNames' as keys for the 'labels' sub dictionary and assigning
                    # a value which is a combination of data['name'] and keyName's key value plus an index string
            for key,value in keyNames.items():
                data['labels'][key] = name + value + index  #ex: {'name':'blah',  'labels':{'key':'blahKeyVal'}}
                data['valData'][key] = None
                data['valData']['id'] = id  #auto_id

            dataList.append(data)

        return dataList


    @classmethod
    def __create_data_table(cls, id, template, keyNames):
        """
        Inputs:
            1. id: Corresponds to the auto_id column in SQL
            2. template: [{'name':'myName', 'labels':{}, 'valData':{}}]
            3. keyNames: {
                'attr1':'Attr1Name',
                'attr2':'Attr2Name',
                etc...
            }


        Output: [{'name':'myName', 'labels':{'attr1':'myNameAttr1Name', 'attr2':'myNameAttr2Name'}, 'valData':{'attr1':'', 'attr2':''}}]

        This function takes the 'name' value from the template parameter and does two things:
            1. Populates the 'labels' sub-dictionary with attribute:concatenated name pairs where it combines the 'name'
                value of the 'template' parameter with the attribute names of each attribute key in the 'keyNames' parameter
            2. Populates the 'valData' sub-dictionary with attribute:'' pairs where the key attribute corresponds to the
                keys of the 'keyNames' parameter

        Explanation: The CylinderReport class has several lists of dicts that start with FORM_ and correspond to
        HTML form input elements. Jinja (generally) reads these directly to create groups of form inputs, and they are also
        used when submitting forms to get data from each input.

         There are three types of form groupings:
            1. Basic list of inputs
            2. Tables with unique rows
            3. Tables with identical rows

            1: The FORM_TEMPLATE is simply a list of dicts of in the format of [{'name':'inputName'}]. These can be output
                and read directly and don't require table generation (There maybe be other key:values corresponding to
                possibly a title or maybe HTML attributes)


            2: The FORM_TEMPLATE is still a list of dicts but the format is as follows [{'name':'rowName', 'labels':{}, 'valData:'{}}]
                -Every input in HTML should have a unique name. Creating a table of these manually would require a lot of
                repetition so it's easier to generate a table combining the 'name' value with pre-defined suffixes, where the
                suffixes come from the keyNames parameter dictionary

            3: The FORM_TEMPLATE for this type is the simplest. It is just a single dict with the same format as previously
                mentioned: {'name':'rowName', 'labels':{}, 'valData:'{}}. The user specifies how many rows they want a list
                is generated with the appropriate labels and valData as in case 2 also using suffixes from keyName. The only
                difference is an integer starting at 0? is assigned to each label to make them unique...

        """
        dataList = []

        for row in template:
            newRow = copy.deepcopy(row) #copy.deepcopy(): copies nested dicts as copy() alone passes references to nested dicts

            for key,val in keyNames.items():
                newRow['labels'][key] = row['name'] + val
                newRow['valData'][key] = ''
                newRow['valData']['id'] = id  # auto_id

            dataList.append(newRow)

        return dataList


    @classmethod
    def __sql_to_html_strength(self, sqlResult, formTable, editing):
        """
        Assign SQL data to FORM template. Remove any trailing results where both days and strength are 0

        :param sqlResult: List of SQL results
        :param formTable: List of HTML form values and properties
        :param editing: Boolean. True if the form is being edited, false otherwise
        :return: A list of HTML form values ready to be output to the page
        """

        strList = []

        strTable = copy.deepcopy(formTable)

        #Ensure all None values are removed
        sqlResult = replaceNone(sqlResult)

        if (not editing):
            # Looping backwards, drop any entries that are 0 up until the first entry with nonzero data
            for i in range(len(sqlResult) - 1, 0, -1):
                if (not sqlResult[i]['target_strength'] and not sqlResult[i]['target_days']):
                    sqlResult.pop(i)
                else:
                    break


        #Populate the strTable with the SQL results
        for i in range(len(sqlResult)):
            strTable[i]['valData']['strength'] = sqlResult[i]['target_strength']
            strTable[i]['valData']['days'] = sqlResult[i]['target_days']
            strTable[i]['valData']['id'] = sqlResult[i]['auto_id']
            strList.append(strTable[i])


        return strList

    @classmethod
    def __sql_to_html_con(self, sqlResult, formTable):
        retList = []

        newFormTable = copy.deepcopy(formTable)

        #Ensure all None values are removed
        sqlResult = replaceNone(sqlResult)

        #Ensure the 'property' fields match and populate the table
        for row in newFormTable:
            for sql in sqlResult:
                if(row['property'] == sql['property']):
                    row['valData']['actual'] = sql['val_actual']
                    row['valData']['min'] = sql['val_min']
                    row['valData']['max'] = sql['val_max']
                    row['valData']['notes'] = sql['notes']
                    row['valData']['id'] = sql['auto_id']
                    break

        return newFormTable

    #Read form data and create SQL entry
    def form_submit(self):

        fieldData = HLP.get_form_values(self.FORM_FIELD_TEMPLATE)

        for key,val in fieldData.items():
            print(f"fieldData: {fieldData[key]}")



        fieldDataClean = self.__field_form_to_sql(fieldData)
        parentID = HLP.sql_insert(self.TB_REPORT_DATA, fieldDataClean)

        self.submitted_id = parentID #Populate submitted_id so the newly inserted cylinder can be loaded back from the DB

        conData = HLP.get_form_values(self.conditions_table)
        strengthData = HLP.get_form_values(self.strength_table)

        conDataClean = self.__con_form_to_sql(conData, parentID)
        strDataClean = self.__strength_form_to_sql(strengthData, parentID)

        HLP.sql_insert(self.TB_CONDITIONS, conDataClean)
        HLP.sql_insert(self.TB_STR_REQ, strDataClean)

    def __field_form_to_sql(self, fieldData):
        sqlData = self.SQL_REPORT_PROPERTIES.copy()

        sqlData.pop('project_id')

        sqlData['date_created']['data'] = fieldData['dateCreated']['valData']
        sqlData['created_by']['data'] = fieldData['createdBy']['valData']
        sqlData['report_title']['data'] = fieldData['cylTitle']['valData']
        sqlData['status']['data'] = fieldData['cylStatus']['valData']
        sqlData['is_scc']['data'] = fieldData['cylSCC']['valData']
        sqlData['ticket_num']['data'] = fieldData['cylTicket']['valData']
        sqlData['project_name']['data'] = fieldData['cylProject']['valData']
        sqlData['supplier']['data'] = fieldData['cylSupplier']['valData']
        sqlData['load_num']['data'] = fieldData['cylLoadNum']['valData']
        sqlData['truck_num']['data'] = fieldData['cylTruckNum']['valData']
        sqlData['contractor']['data'] = fieldData['cylContractor']['valData']
        sqlData['sampled_from']['data'] = fieldData['cylSampled']['valData']
        sqlData['mould_type']['data'] = fieldData['cylMouldType']['valData']
        sqlData['mix_id']['data'] = fieldData['cylMix']['valData']
        sqlData['po_num']['data'] = fieldData['cylPONum']['valData']
        sqlData['placement_type']['data'] = fieldData['cylPlacement']['valData']
        sqlData['cement_type']['data'] = fieldData['cylCement']['valData']
        sqlData['load_volume']['data'] = fieldData['cylVolume']['valData']
        sqlData['load_volume_units']['data'] =  fieldData['cylVolumeUnits']['valData']
        sqlData['date_cast']['data'] = fieldData['cylCastDate']['valData']
        sqlData['time_batch']['data'] = fieldData['cylBatchTime']['valData']
        sqlData['time_sample']['data'] = fieldData['cylSampleTime']['valData']
        sqlData['time_cast']['data'] = fieldData['cylSampleTime']['valData']
        sqlData['date_transported']['data'] = fieldData['cylDateTransported']['valData']
        sqlData['notes']['data'] = fieldData['cylNotes']['valData']


        dataList = []
        dataList.append(sqlData)

        dataList = HLP.sql_sanitize(dataList)

        return dataList

    def __con_form_to_sql(self, conData, parent_id):
        """
        1. Assign the values from the 'conData' parameter to a specific SQL table
        2. Convert the result to a list
        3. Sanitize the data with a helper function
        4. Return the list

        :param conData: A dictionaries where each main key's value corresponds to HTML form input data. There is a 'valData'
            sub-dictionary which will be populated with key:values which correspond to some SQL database columns
        :return: A list of dictionaries which correspond to a specific SQL table with clean data ready to be inserted into the
            database
        """
        dataList = []

        for key, val in conData.items():
            sqlData = copy.deepcopy(self.SQL_CONDITIONS_PROPERTIES)

            sqlData['cyl_report_id']['data'] = parent_id
            sqlData['property']['data'] = conData[key]['property']
            sqlData['val_actual']['data'] = conData[key]['valData']['actual']
            sqlData['val_min']['data'] = conData[key]['valData']['min']
            sqlData['val_max']['data'] = conData[key]['valData']['max']
            sqlData['notes']['data'] = conData[key]['valData']['notes']
            #sqlData['val_actual_precision']['data'] = 0
            #sqlData['val_min_precision']['data'] = 0
            #sqlData['val_max_precision']['data'] = 0

            dataList.append(sqlData)

        dataList = HLP.sql_sanitize(dataList)

        return dataList

    def __strength_form_to_sql(self, strData, parent_id):
        """
        1. Assign the values from the 'strData' parameter to a specific SQL table
        2. Convert the result to a list
        3. Sanitize the data with a helper function
        4. Return the list

        :param strData: A dictionaries where each main key's value corresponds to HTML form input data. There is a 'valData'
            sub-dictionary which will be populated with key:values which correspond to some SQL database columns
        :return: A list of dictionaries which correspond to a specific SQL table with clean data ready to be inserted into the
            database
        """
        print(f"strData: {strData}")

        dataList = []

        for key, val in strData.items():
            sqlData = copy.deepcopy(self.SQL_STR_REQ_PROPERTIES.copy())

            sqlData['cyl_report_id']['data'] = parent_id
            sqlData['target_strength']['data'] = strData[key]['valData']['strength']
            sqlData['target_days']['data'] = strData[key]['valData']['days']
            dataList.append(sqlData)

        dataList = HLP.sql_sanitize(dataList)

        return dataList


    #Convert object dict
    def to_dict(self):
        objectData = {
            "id": self.id,
            "dateCreated": self.date_created,
            "title": self.title,
            "status": self.status,
            "projectName": self.project_name,
            "ticketNum": self.ticket_num,
            "supplier": self.supplier,
            "loadNum": self.load_num,
            "truckNum": self.truck_num,
            "contractor": self.contractor,
            "sampledFrom": self.sampled_from,
            "mixId": self.mix_ID,
            "mouldType": self.mould_type,
            "poNum": self.po_num,
            "placementType": self.placement_type,
            "cementType": self.cement_type,
            "loadVolume": self.load_volume,
            "loadVolumeUnits": self.load_volume_units,
            "dateCast": self.date_cast,
            "batchTime": self.batch_time,
            "sampleTime": self.sample_time,
            "castTime": self.cast_time,
            "dateTransported": self.date_transported,
            "notes": self.notes,
            "isSCC": self.is_scc,
            "createdBy": self.created_by,

            "strTable": self.strength_table,
            "conditionsTable": self.conditions_table
        }

        return objectData

    #Return data tables as dicts
    def tables_to_dict(self):
        dataTables = {
            "loadVolumeData": self.UNITS_OPTIONS,
            "mouldData": self.MOULD_OPTIONS,
            "sccData": self.SCC_OPTIONS,
            "statusData": self.STATUS_TABLE
        }

        return dataTables



