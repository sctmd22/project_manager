from datetime import datetime

from filters import strip_date_f
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


    #This looks stupid. As with other 'options', the left is what is stored in SQL and the right is what is displayed
        #on the webpage
    BREAK_TYPE_OPTIONS = {
        '1':'1',
        '2':'2',
        '3':'3',
        '4':'4',
        '5':'5',
        '6':'6'
    }



    FORM_LABELS = (
        'projectID',    #Parent (project) ID
        'cylinderID',   #autoID
        'dateCreated',
        'createdBy',
        'reportTitle',
        'status',
        'projectName',
        'ticketNum',
        'supplier',
        'loadNum',
        'truckNum',
        'contractor',
        'sampledFrom',
        'mixID',
        'mouldType',
        'poNum',
        'placementType',
        'cementType',
        'volume',
        'volumeUnits',
        'castDate',
        'castTime',
        'batchTime',
        'sampleTime',
        'dateTransported',
        'dateReceived',
        'dateReceivedEqual',
        'notes',
        'isScc'

    )

    FORM_FIELD_TEMPLATE = [
        {'name': 'cyl',          'title':'', 'labels':{}, 'valData':{}}
    ]


    STR_LABELS = (
        'strength',
        'days',
        'visible',
        'autoID'
    )

    #Template for the HTML strength table which gets repeated X number of times
    #'labels' and 'valData' are used for writing to HTML data and reading HTML forms
        #When the table is built it will look like: {'name':'str',   'title':'Target {n}',   'labels':{'strength':'strStrength', 'days':'strDays', 'id':'strID'}, 'valData':{'strength':'', 'days', 'id':''}}
    FORM_STR_TEMPLATE = {
        'name':'strTable',   'title':'Target {n}',   'labels': {},    'valData':{}
    }


    CONDITIONS_LABELS = (
        'actual',
        'min',
        'max',
        'notes',
        'autoID'
    )


    #Template for field/measurement data and properties
    #When the table is built, one entry will look like:
        #{'name':'cylConFlow', 'property':'flow', 'SCC':True, 'CYL':False, 'labels':{'actual':'cylConFlowActual', 'min':'cylConFlowMin', ...etc}, 'data':{'actual':'', 'min':'', 'max':'', 'notes':'', 'id':''}}
        #'title': Used to output a text title in HTML
        #'property': These are stored as VARCHARs in SQL to keep track of each property. Also used to match the data when going from the HTML form to SQL and reverse
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


    CYL_ITEMS_LABELS = (
        'itemID',
        'dateReceived',
        'dateTested',
        'age',
        'diameter',
        'length',
        'area',
        'weight',
        'strength',
        'breakType',
        'requiredStrength',
        'percentStrength',
        'initials',
        'autoID'
    )



    FORM_ITEMS_TEMPLATE = [{
        'name':'cylItem',   'title':'',   'labels': {},    'valData':{}
    }]

    '''-------------------------------------SQL DATA-------------------------------------'''

    SQL_STR_REQ_PROPERTIES = {
        'cyl_report_id':      {'dataType': SQL.DATATYPES.INT,       'size':SQL.INT_SIZES['UINT'],      'data':None},
        'target_strength':    {'dataType': SQL.DATATYPES.INT,       'size':SQL.INT_SIZES['UINT'],      'data':None},
        'target_days':        {'dataType': SQL.DATATYPES.INT,       'size':SQL.INT_SIZES['UINT'],      'data':None},
        'target_visible':     {'dataType': SQL.DATATYPES.TINY_INT,  'size':SQL.INT_SIZES['TINY_INT'],  'data':None},
        'auto_id':            {'dataType': SQL.DATATYPES.INT,       'size':SQL.INT_SIZES['UINT'],      'data':None}
    }



    SQL_CONDITIONS_PROPERTIES = {
        'cyl_report_id':           {'dataType': SQL.DATATYPES.INT,              'size': SQL.INT_SIZES['INT'],       'data':None},
        'property':                {'dataType': SQL.DATATYPES.VARCHAR,          'size': 255,                        'data':None},
        'val_actual':              {'dataType': SQL.DATATYPES.VARCHAR_DECIMAL,  'size': 15,                         'data':None},
        'val_min':                 {'dataType': SQL.DATATYPES.VARCHAR_DECIMAL,  'size': 15,                         'data':None},
        'val_max':                 {'dataType': SQL.DATATYPES.VARCHAR_DECIMAL,  'size': 15,                         'data':None},
        'notes':                   {'dataType': SQL.DATATYPES.VARCHAR,          'size': 1000,                       'data':None},
        'auto_id':                 {'dataType': SQL.DATATYPES.INT,              'size': SQL.INT_SIZES['INT'],       'data':None}
    }


    SQL_CYLINDERS_PROPERTIES = {
        'cyl_report_id':               {'dataType': SQL.DATATYPES.INT,         'size': SQL.INT_SIZES['INT'],                    'data':None},
        'item_id':                     {'dataType': SQL.DATATYPES.VARCHAR,     'size': 50,                                      'data':None},
        'date_received':               {'dataType': SQL.DATATYPES.DATETIME,    'size': None,                                    'data':None},
        'date_tested':                 {'dataType': SQL.DATATYPES.DATETIME,    'size': None,                                    'data':None},
        'age':                         {'dataType': SQL.DATATYPES.VARCHAR,     'size': 10,                                      'data':None},
        'diameter':                    {'dataType': SQL.DATATYPES.VARCHAR_DECIMAL, 'size': 10,                                  'data':None},
        'length':                      {'dataType': SQL.DATATYPES.VARCHAR_DECIMAL, 'size': 10,                                  'data':None},
        'area':                        {'dataType': SQL.DATATYPES.VARCHAR_DECIMAL, 'size': 10,                                  'data':None},
        'weight':                      {'dataType': SQL.DATATYPES.VARCHAR_DECIMAL, 'size': 10,                                  'data':None},
        'strength':                    {'dataType': SQL.DATATYPES.VARCHAR_DECIMAL, 'size': 10,                                  'data':None},
        'break_type':                  {'dataType': SQL.DATATYPES.ENUM,        'size': None, 'enums': BREAK_TYPE_OPTIONS,       'data':None},
        'percent_strength':            {'dataType': SQL.DATATYPES.INT,         'size': SQL.INT_SIZES['INT'],                    'data':None},
        'initials':                    {'dataType': SQL.DATATYPES.VARCHAR,     'size': 10,                                      'data':None},
        'notes':                       {'dataType': SQL.DATATYPES.TEXT,        'size': SQL.TEXT_SIZES['TEXT'],                  'data':None},
        'auto_id':                     {'dataType': SQL.DATATYPES.INT,         'size': SQL.INT_SIZES['INT'],                    'data':None}
    }


    SQL_REPORT_PROPERTIES = {
        'project_id':                  {'dataType': SQL.DATATYPES.INT,         'size': SQL.INT_SIZES['INT'],                    'data':None},
        'date_created':                {'dataType': SQL.DATATYPES.DATETIME,    'size': None,                                    'data':None},
        'created_by':                  {'dataType': SQL.DATATYPES.VARCHAR,     'size': 50,                                      'data':None},
        'report_title':                {'dataType': SQL.DATATYPES.VARCHAR,     'size': 255,                                     'data':None},
        'status':                      {'dataType': SQL.DATATYPES.ENUM,        'size': None, 'enums': Reports.STATUS_TABLE,     'data':None},
        'is_scc':                      {'dataType': SQL.DATATYPES.ENUM,        'size': None, 'enums': SCC_OPTIONS,              'data':None},
        'ticket_num':                  {'dataType': SQL.DATATYPES.VARCHAR,     'size': 50,                                      'data':None},
        'project_name':                {'dataType': SQL.DATATYPES.VARCHAR,     'size': 50,                                      'data':None},
        'supplier':                    {'dataType': SQL.DATATYPES.VARCHAR,     'size': 50,                                      'data':None},
        'load_num':                    {'dataType': SQL.DATATYPES.VARCHAR,     'size': 50,                                      'data':None},
        'truck_num':                   {'dataType': SQL.DATATYPES.VARCHAR,     'size': 50,                                      'data':None},
        'contractor':                  {'dataType': SQL.DATATYPES.VARCHAR,     'size': 50,                                      'data':None},
        'sampled_from':                {'dataType': SQL.DATATYPES.VARCHAR,     'size': 50,                                      'data':None},
        'mould_type':                  {'dataType': SQL.DATATYPES.ENUM,        'size': None, 'enums': MOULD_OPTIONS,            'data':None},
        'mix_id':                      {'dataType': SQL.DATATYPES.VARCHAR,     'size': 50,                                      'data':None},
        'po_num':                      {'dataType': SQL.DATATYPES.VARCHAR,     'size': 50,                                      'data':None},
        'placement_type':              {'dataType': SQL.DATATYPES.VARCHAR,     'size': 50,                                      'data':None},
        'cement_type':                 {'dataType': SQL.DATATYPES.VARCHAR,     'size': 50,                                      'data':None},
        'load_volume':                 {'dataType': SQL.DATATYPES.VARCHAR,     'size': 50,                                      'data':None},
        'load_volume_units':           {'dataType': SQL.DATATYPES.ENUM,        'size': None, 'enums': UNITS_OPTIONS,            'data':None},
        'date_cast':                   {'dataType': SQL.DATATYPES.DATETIME,    'size': None,                                    'data':None},
        'time_batch':                  {'dataType': SQL.DATATYPES.TIME,        'size': None,                                    'data':None},
        'time_sample':                 {'dataType': SQL.DATATYPES.TIME,        'size': None,                                    'data':None},
        'time_cast':                   {'dataType': SQL.DATATYPES.TIME,        'size': None,                                    'data':None},
        'date_transported':            {'dataType': SQL.DATATYPES.DATETIME,    'size': None,                                    'data':None},
        'date_received':               {'dataType': SQL.DATATYPES.DATETIME,    'size': None,                                    'data':None},
        'date_received_equal':         {'dataType': SQL.DATATYPES.BOOL,        'size': None,                                    'data':None},
        'notes':                       {'dataType': SQL.DATATYPES.TEXT,        'size': SQL.TEXT_SIZES['TEXT'],                  'data':None},
        'auto_id':                     {'dataType': SQL.DATATYPES.INT,         'size': SQL.INT_SIZES['INT'],                    'data':None}
    }



    #Constructor
    def __init__(self, data, id):
        self.id = id
        self.field_table = data['fieldTable']
        self.strength_table = data['strTable']
        self.conditions_table = data['conditionsTable']
        self.cyl_items_table = data['cylItemsTable']

    #Create a new cylinder report with default values
    @classmethod
    def create_default(cls):
        parent_id = None
        cylinder_id = None
        createdby = 'admin'

        #Create data tables from templates
        fieldTable = cls.__create_data_table(cls.FORM_FIELD_TEMPLATE, cls.FORM_LABELS)
        strTable = cls.__create_data_n_table(cls.FORM_STR_TEMPLATE, cls.STR_LABELS, cls.NUM_STR_TARGETS)
        conTable = cls.__create_data_table(cls.FORM_CONDITIONS_TEMPLATE, cls.CONDITIONS_LABELS)


        #Ensure first item is always visible
        strTable[0]['valData']['visible'] = 1

        #Populate some defaults
        fieldTable[0]['valData']['projectID'] = parent_id
        fieldTable[0]['valData']['cylinderID'] = cylinder_id
        fieldTable[0]['valData']['dateCreated'] = datetime.today()
        fieldTable[0]['valData']['createdBy'] = createdby
        fieldTable[0]['valData']['reportTitle'] = 'Report Title'
        fieldTable[0]['valData']['status'] = 'active'
        fieldTable[0]['valData']['mouldType'] = list(cls.MOULD_OPTIONS.keys())[0] #Get keys from dict, convert to list, get 0th item
        fieldTable[0]['valData']['volumeUnits'] = "meters"
        fieldTable[0]['valData']['isScc'] = "no"
        fieldTable[0]['valData']['dateReceivedEqual'] = "checked"


        defaultData = {
            "fieldTable": fieldTable,
            "strTable": strTable,
            "conditionsTable": conTable,
            "cylItemsTable": ""
        }

        #Call the CylinderReport constructor to create a class instance with the default data
        return cls(defaultData, cylinder_id)

    @classmethod
    def create_from_db(cls, id, editing=False):
        #Get database values
        report_sql = super().sql_fetchone(f"SELECT * FROM {cls.TB_REPORT_DATA} WHERE auto_id = %s", (id,)) #The (id,) is a tuple of values which corresponds to %s
        str_sql = super().sql_fetchall(f"SELECT * FROM {cls.TB_STR_REQ} WHERE cyl_report_id = %s ORDER BY auto_id ASC", (id,))
        con_sql = super().sql_fetchall(f"SELECT * FROM {cls.TB_CONDITIONS} WHERE cyl_report_id = %s ORDER BY auto_id ASC", (id,))
        cyl_items_sql = super().sql_fetchall(f"SELECT * FROM {cls.TB_CYLINDERS} WHERE cyl_report_id = %s ORDER BY auto_id ASC", (id,))

        fieldTable = cls.__create_data_table(cls.FORM_FIELD_TEMPLATE, cls.FORM_LABELS)
        strTable = cls.__create_data_n_table(cls.FORM_STR_TEMPLATE, cls.STR_LABELS, cls.NUM_STR_TARGETS)
        conTable = cls.__create_data_table(cls.FORM_CONDITIONS_TEMPLATE, cls.CONDITIONS_LABELS)
        cylTable = cls.__create_data_table(cls.FORM_ITEMS_TEMPLATE, cls.CYL_ITEMS_LABELS)

        field_result = cls.__sql_to_html_field(report_sql, fieldTable)
        str_result = cls.__sql_to_html_strength(str_sql, strTable, editing)
        con_result = cls.__sql_to_html_con(con_sql, conTable)
        cyl_items_result = cls.__sql_to_html_cyl_items(cyl_items_sql, cylTable)

        id = field_result[0]['valData']['cylinderID'] #only 1 item in the list

        data = {
            "fieldTable":field_result,
            "strTable": str_result,
            "conditionsTable": con_result,
            "cylItemsTable": cyl_items_result
        }

        return cls(data, id)

    @classmethod
    def __create_data_n_table(cls, templateRow, formLabels, n):
        dataList = []

        startVal = 1  #Start at 0 or 1

        for i in range(n):
            index = str(i + startVal)
            data = copy.deepcopy(templateRow)
            data['title'] = data['title'].replace('{n}', index)   #Replace any instances of {n} in 'title' with index

            name = data['name']
            data['name'] = name + index #Concatenate the index value to the name

            #Iterate through labels and assign/concatenate names to the 'labels' and 'valData' subdicts
                # Using the keys from 'keyNames' as keys for the 'labels' sub dictionary and assigning
                    # a value which is a combination of data['name'] and keyName's key value plus an index string

            for key in formLabels:
                label = HLP.capitalizeFirst(key)    #The label is simply the key value with the first letter capitalized
                data['labels'][key] = name + label + index
                data['valData'][key] = None

            dataList.append(data)

        return dataList

    @classmethod
    def __create_data_table(cls, template, formLabels):
        """
        Inputs:
            1. template: [{'name':'myName', 'labels':{}, 'valData':{}}]
            2. formLabels: (
                'labelOne':,
                'labelTwo',
                etc...
            )


        Output: [{'name':'myName', 'labels':{'labelOne':'myNameLabelOne', 'labelTwo':'myNameLabelTwo'}, 'valData':{'labelOne':'', 'labelTwo':''}}]

        This function takes the 'name' value from the template parameter and does two things:
            1. Populates the 'labels' sub-dictionary of the template parameter with the items in the formLabels tuple.
                    key: item
                    value: nameItemN
                        name -> The value of the 'name' key of each row of the template parameter
                        Item -> item (first letter capitalized)
                        N   -> Index starting at 0 or 1 counting up

            2. Populates the 'valData' sub-dictionary with the items from the formLabels tuple.
                    key: item

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

            for key in formLabels:
                label = HLP.capitalizeFirst(key)
                newRow['labels'][key] = row['name'] + label
                newRow['valData'][key] = ''

            dataList.append(newRow)

        return dataList

    @classmethod
    def __sql_to_html_field(self, sqlResult, formTable):
        formData = copy.deepcopy(formTable)

        sqlResult = replaceNone(sqlResult)

        #formTable only has 1 list element
        for row in formData:
            row['valData']['projectID'] = sqlResult['project_id']
            row['valData']['cylinderID'] = sqlResult['auto_id']
            row['valData']['dateCreated'] = sqlResult['date_created']
            row['valData']['createdBy'] = sqlResult['created_by']
            row['valData']['reportTitle'] = sqlResult['report_title']
            row['valData']['status'] = sqlResult['status']
            row['valData']['projectName'] = sqlResult['project_name']
            row['valData']['ticketNum'] = sqlResult['ticket_num']
            row['valData']['supplier'] = sqlResult['supplier']
            row['valData']['truckNum'] = sqlResult['truck_num']
            row['valData']['loadNum'] = sqlResult['load_num']
            row['valData']['contractor'] = sqlResult['contractor']
            row['valData']['sampledFrom'] = sqlResult['sampled_from']
            row['valData']['mixID'] = sqlResult['mix_id']
            row['valData']['mouldType'] = sqlResult['mould_type']
            row['valData']['poNum'] = sqlResult['po_num']
            row['valData']['placementType'] = sqlResult['placement_type']
            row['valData']['cementType'] = sqlResult['cement_type']
            row['valData']['volume'] = sqlResult['load_volume']
            row['valData']['volumeUnits'] = sqlResult['load_volume_units']
            row['valData']['castDate'] = sqlResult['date_cast']
            row['valData']['castTime'] = sqlResult['time_cast']
            row['valData']['batchTime'] = sqlResult['time_batch']
            row['valData']['sampleTime'] = sqlResult['time_sample']
            row['valData']['dateTransported'] = sqlResult['date_transported']
            row['valData']['dateReceived'] = sqlResult['date_received']

            row['valData']['notes'] = sqlResult['notes']
            row['valData']['isScc'] = sqlResult['is_scc']

            # Do some processing for the checkbox
            if (sqlResult['date_received_equal'] == 1):
                row['valData']['dateReceivedEqual'] = 'checked'
            else:
                row['valData']['dateReceivedEqual'] = ''




        return formData

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
        sqlResult = copy.deepcopy(sqlResult)

        '''
        if (not editing):
            # Looping backwards, drop any entries that are 0 up until the first entry with nonzero data
            for i in range(len(sqlResult) - 1, 0, -1):
                if (sqlResult[i]['target_strength'] == None and sqlResult[i]['target_days'] == None):
                    sqlResult.pop(i)
                else:
                    break

        '''


        #Ensure all None values are removed
        sqlResult = replaceNone(sqlResult)


        #Populate the strTable with the SQL results
        for i in range(len(sqlResult)):
            strTable[i]['valData']['strength'] = sqlResult[i]['target_strength']
            strTable[i]['valData']['days'] = sqlResult[i]['target_days']
            strTable[i]['valData']['visible'] = sqlResult[i]['target_visible']
            strTable[i]['valData']['autoID'] = sqlResult[i]['auto_id']
            strList.append(strTable[i])

        #Ensure the first entry is visible
        strList[0]['valData']['visible'] = 1

        return strList

    @classmethod
    def __sql_to_html_con(self, sqlResult, formTable):
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
                    row['valData']['cylReportID'] = sql['cyl_report_id']
                    row['valData']['autoID'] = sql['auto_id']
                    break

        return newFormTable

    @classmethod
    def __sql_to_html_cyl_items(self, sqlResult, formTable):
        sqlResult = HLP.replaceNone(sqlResult)

        newFormTable = []

        for i, row in enumerate(sqlResult):
            newFormTable.append(copy.deepcopy(formTable[0])) #copy the form table (which is only 1 row) as many times as there is SQL data

            newFormTable[i]['valData']['itemID'] = row['item_id']
            newFormTable[i]['valData']['dateReceived'] = row['date_received']
            newFormTable[i]['valData']['dateTested'] = row['date_tested']
            newFormTable[i]['valData']['age'] = row['age']
            newFormTable[i]['valData']['diameter'] = row['diameter']
            newFormTable[i]['valData']['length'] = row['length']
            newFormTable[i]['valData']['area'] = row['area']
            newFormTable[i]['valData']['weight'] = row['weight']
            newFormTable[i]['valData']['strength'] = row['strength']
            newFormTable[i]['valData']['breakType'] = row['break_type']
            newFormTable[i]['valData']['percentStrength'] = row['percent_strength']
            newFormTable[i]['valData']['initials'] = row['initials']

            newFormTable[i]['valData']['autoID'] = row['auto_id']


        return newFormTable


    #Read form data and create SQL entry
    def submit_form(self):
        fieldData = HLP.get_form_values(self.field_table)
        fieldDataClean = self.__field_form_to_sql(fieldData)
        cylID = HLP.sql_insert(self.TB_REPORT_DATA, fieldDataClean)

        self.id = cylID #Populate submitted_id so the newly inserted cylinder can be loaded back from the DB

        strengthData = HLP.get_form_values(self.strength_table)
        strDataClean = self.__strength_form_to_sql(strengthData, cylID)
        HLP.sql_insert(self.TB_STR_REQ, strDataClean)

        conData = HLP.get_form_values(self.conditions_table)

        conDataClean = self.__con_form_to_sql(conData, cylID)
        HLP.sql_insert(self.TB_CONDITIONS, conDataClean)

    def submit_edit(self):
        fieldData = HLP.get_form_values(self.field_table)

        fieldDataClean = self.__field_form_to_sql(fieldData)
        HLP.sql_update(self.TB_REPORT_DATA, fieldDataClean)

        strengthData = HLP.get_form_values(self.strength_table)
        strDataClean = self.__strength_form_to_sql(strengthData, self.id)
        HLP.sql_update(self.TB_STR_REQ, strDataClean)

        conData = HLP.get_form_values(self.conditions_table)
        conDataClean = self.__con_form_to_sql(conData, self.id)
        HLP.sql_update(self.TB_CONDITIONS, conDataClean)

    def delete(self):
        HLP.sql_delete(self.TB_REPORT_DATA, self.id)


    def __field_form_to_sql(self, fieldData):
        sqlData = copy.deepcopy(self.SQL_REPORT_PROPERTIES)

        #Grab the only key
        key = next(iter(fieldData))

        sqlData['project_id']['data'] = fieldData[key]['valData']['projectID']

        sqlData['date_created']['data'] = fieldData[key]['valData']['dateCreated']
        sqlData['created_by']['data'] = fieldData[key]['valData']['createdBy']
        sqlData['report_title']['data'] = fieldData[key]['valData']['reportTitle']
        sqlData['status']['data'] = fieldData[key]['valData']['status']
        sqlData['is_scc']['data'] = fieldData[key]['valData']['isScc']
        sqlData['ticket_num']['data'] = fieldData[key]['valData']['ticketNum']
        sqlData['project_name']['data'] = fieldData[key]['valData']['projectName']
        sqlData['supplier']['data'] = fieldData[key]['valData']['supplier']
        sqlData['load_num']['data'] = fieldData[key]['valData']['loadNum']
        sqlData['truck_num']['data'] = fieldData[key]['valData']['truckNum']
        sqlData['contractor']['data'] = fieldData[key]['valData']['contractor']
        sqlData['sampled_from']['data'] = fieldData[key]['valData']['sampledFrom']
        sqlData['mould_type']['data'] = fieldData[key]['valData']['mouldType']
        sqlData['mix_id']['data'] = fieldData[key]['valData']['mixID']
        sqlData['po_num']['data'] = fieldData[key]['valData']['poNum']
        sqlData['placement_type']['data'] = fieldData[key]['valData']['placementType']
        sqlData['cement_type']['data'] = fieldData[key]['valData']['cementType']
        sqlData['load_volume']['data'] = fieldData[key]['valData']['volume']
        sqlData['load_volume_units']['data'] =  fieldData[key]['valData']['volumeUnits']
        sqlData['date_cast']['data'] = fieldData[key]['valData']['castDate']
        sqlData['time_batch']['data'] = fieldData[key]['valData']['batchTime']
        sqlData['time_sample']['data'] = fieldData[key]['valData']['sampleTime']
        sqlData['time_cast']['data'] = fieldData[key]['valData']['castTime']
        sqlData['date_transported']['data'] = fieldData[key]['valData']['dateTransported']
        sqlData['notes']['data'] = fieldData[key]['valData']['notes']

        sqlData['auto_id']['data'] = fieldData[key]['valData']['cylinderID']


        #Processing date received checkbox. 'on' is what a checked checkbox returns if no value specified
        if(fieldData[key]['valData']['dateReceivedEqual'] == 'on'):
            sqlData['date_received_equal']['data'] = 1
            sqlData['date_received']['data'] = fieldData[key]['valData']['dateTransported']
        else:
            sqlData['date_received_equal']['data'] = 0
            sqlData['date_received']['data'] = fieldData[key]['valData']['dateReceived']

        #Convert to list
        dataList = []
        dataList.append(sqlData)

        dataList = HLP.sql_sanitize(dataList)

        return dataList

    def __con_form_to_sql(self, conData, cylID):
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

            sqlData['cyl_report_id']['data'] = cylID
            sqlData['property']['data'] = conData[key]['property']
            sqlData['val_actual']['data'] = conData[key]['valData']['actual']
            sqlData['val_min']['data'] = conData[key]['valData']['min']
            sqlData['val_max']['data'] = conData[key]['valData']['max']
            sqlData['notes']['data'] = conData[key]['valData']['notes']
            sqlData['auto_id']['data'] = conData[key]['valData']['autoID']

            dataList.append(sqlData)

        dataList = HLP.sql_sanitize(dataList)

        return dataList

    def __strength_form_to_sql(self, strData, cylID):
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
        dataList = []

        for key, val in strData.items():
            sqlData = copy.deepcopy(self.SQL_STR_REQ_PROPERTIES.copy())

            sqlData['cyl_report_id']['data'] = cylID
            sqlData['target_strength']['data'] = strData[key]['valData']['strength']
            sqlData['target_days']['data'] = strData[key]['valData']['days']
            sqlData['target_visible']['data'] = strData[key]['valData']['visible']
            sqlData['auto_id']['data'] = strData[key]['valData']['autoID']
            dataList.append(sqlData)

        dataList = HLP.sql_sanitize(dataList)

        #Ensure the first item of the strength table is always visible
        dataList[0]['target_visible']['data'] = 1

        return dataList


    #Convert object dict
    def to_dict(self):

        objectData = {
            "id":self.id,   #id is also in 'fieldTable', but this allows quick acccess
            "fieldTable":self.field_table[0], #Return 0th item because even though it is a list it only has 1 entry
            "strTable": self.strength_table,
            "conditionsTable": self.conditions_table,
            "cylItemsTable": self.cyl_items_table
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



