from datetime import datetime
from enum import Enum

from filters import strip_date_f
from helpers import helpers as HLP
import db as db
import copy

from db import sql_data as SQL
from helpers.helpers import processSql

import GLOBALS as GLB

class Reports:
    STATUS_TABLE = {
        'active': "Active",
        'complete': "Complete",
        'deleted': "Deleted",
        'canceled': "Canceled"
    }

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

    SEPARATOR_OPTIONS = {
        '-':'-',
        '.':'.',
        'space':'Space',
    }

    SET_OPTIONS = {
        'a':'A',
        'b':'B',
        'c':'C',
        'd':'D',
        'e':'E',
        'f':'F',
        'none':'None'
    }

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


    FORM_LABELS = [
        {'label': 'projectID',          'dataType': None, 'size': None, 'sqlID':'project_id'},
        {'label': 'cylinderID',         'dataType': None, 'size': None, 'sqlID':'auto_id'},
        {'label': 'dateCreated',        'dataType': None, 'size': None, 'sqlID':'date_created'},
        {'label': 'createdBy',          'dataType': None, 'size': None, 'sqlID':'created_by'},
        {'label': 'reportTitle',        'dataType': GLB.VALIDATION_TYPES['TEXT'], 'size': 50, 'sqlID':'report_title'},
        {'label': 'status',             'dataType': None, 'size': None, 'sqlID':'status'},
        {'label': 'projectName',        'dataType': GLB.VALIDATION_TYPES['TEXT'], 'size': 50, 'sqlID':'project_name'},
        {'label': 'ticketNum',          'dataType': GLB.VALIDATION_TYPES['TEXT'], 'size': 25, 'sqlID':'ticket_num'},
        {'label': 'supplier',           'dataType': GLB.VALIDATION_TYPES['TEXT'], 'size': 25, 'sqlID':'supplier'},
        {'label': 'loadNum',            'dataType': GLB.VALIDATION_TYPES['TEXT'], 'size': 25, 'sqlID':'load_num'},
        {'label': 'truckNum',           'dataType': GLB.VALIDATION_TYPES['TEXT'], 'size': 25, 'sqlID':'truck_num'},
        {'label': 'contractor',         'dataType': GLB.VALIDATION_TYPES['TEXT'], 'size': 25, 'sqlID':'contractor'},
        {'label': 'sampledFrom',        'dataType': GLB.VALIDATION_TYPES['TEXT'], 'size': 25, 'sqlID':'sampled_from'},
        {'label': 'mixID',              'dataType': GLB.VALIDATION_TYPES['TEXT'], 'size': 25, 'sqlID':'mix_id'},
        {'label': 'mouldType',          'dataType': None, 'size': None, 'sqlID':'mould_type'},
        {'label': 'poNum',              'dataType': GLB.VALIDATION_TYPES['TEXT'], 'size': 25, 'sqlID':'po_num'},
        {'label': 'placementType',      'dataType': GLB.VALIDATION_TYPES['TEXT'], 'size': 25, 'sqlID':'placement_type'},
        {'label': 'cementType',         'dataType': GLB.VALIDATION_TYPES['TEXT'], 'size': 25, 'sqlID':'cement_type'},
        {'label': 'volume',             'dataType': GLB.VALIDATION_TYPES['TEXT'], 'size': 5, 'sqlID':'load_volume'},
        {'label': 'volumeUnits',        'dataType': None, 'size': None, 'sqlID':'volume_units'},
        {'label': 'castDate',           'dataType': None, 'size': None, 'sqlID':'date_cast'},
        {'label': 'castTime',           'dataType': None, 'size': None, 'sqlID':'time_cast'},
        {'label': 'batchTime',          'dataType': None, 'size': None, 'sqlID':'time_batch'},
        {'label': 'sampleTime',         'dataType': None, 'size': None, 'sqlID':'time_sample'},
        {'label': 'dateTransported',    'dataType': None, 'size': None, 'sqlID':'date_transported'},
        {'label': 'dateReceived',       'dataType': None, 'size': None, 'sqlID':'date_received'},
        {'label': 'dateReceivedEqual',  'dataType': None, 'size': None, 'sqlID':'date_received_equal'},
        {'label': 'dateSpecimen',       'dataType': None, 'size': None, 'sqlID':'date_specimen'},
        {'label': 'dateSpecimenEqual',  'dataType': None, 'size': None, 'sqlID':'date_specimen_equal'},
        {'label': 'notes',              'dataType': GLB.VALIDATION_TYPES['TEXT'], 'size': None, 'sqlID':'notes'},
        {'label': 'isScc',              'dataType': None, 'size': None, 'sqlID':'is_scc'},
    ]

    FORM_FIELD_TEMPLATE = [{
        'name': 'cyl', 'title': '',  'dataFields':{}
    }]


    """
    This structure is used in conjunction with a  FORM TEMPLATE to build a table which is used to create HTML
        elements with unique ID's and contain validation data for JavaScript to read, such as 'dataType' and 'size'
    The finished table is in the form:
        name:..., 
        title:..., 
        dataFields:
           strength: {label:..., val:..., dataType:..., size:..., errorLabel:...},
           days: {...},
    """
    STR_LABELS = [
        {'label':'strength',     'dataType':GLB.VALIDATION_TYPES['POS_INT'],        'size':{'min': 0, 'max': 999},      'sqlID':'target_strength'},
        {'label':'days',         'dataType':GLB.VALIDATION_TYPES['POS_INT'],        'size':{'min': 0, 'max': 999},      'sqlID':'target_days'},
        {'label':'visible',      'dataType':None,                                   'size': None,                       'sqlID':'target_visible'},
        {'label':'autoID',       'dataType':None,                                   'size': None,                       'sqlID':'auto_id'},
    ]

    FORM_STR_TEMPLATE = [
        {'name':'strTable',   'title':'Target {n}',   'dataFields':{}}
    ]


    CONDITIONS_LABELS = [
        {'label': 'actual',     'dataType': GLB.VALIDATION_TYPES['NUMBER'], 'size': 10},
        {'label': 'min',        'dataType': GLB.VALIDATION_TYPES['NUMBER'], 'size': 10},
        {'label': 'max',        'dataType': GLB.VALIDATION_TYPES['NUMBER'], 'size': 10},
        {'label': 'notes',      'dataType': GLB.VALIDATION_TYPES['TEXT'],   'size': 2000},
        {'label': 'cylReportID','dataType': None,                           'size': None},
        {'label': 'autoID',     'dataType': None,                           'size': None},
    ]

    #Template for field/measurement data and properties
        #'title': Used to output a text title in HTML
        #'property': These are stored as VARCHARs in SQL to keep track of each property. Also used to match the data when going from the HTML form to SQL and reverse
    FORM_CONDITIONS_TEMPLATE = [
        {'name':'cylConFlow',               'title':'Flow (mm)',                           'property':'flow',           'SCC':True, 'CYL': False,   'dataFields':{}},
        {'name':'cylConT50',                'title':'T<sub>50</sub>(s)',                   'property':'t_50',           'SCC':True, 'CYL': False,   'dataFields':{}},
        {'name':'cylConVSI',                'title':'VSI',                                 'property':'vsi',            'SCC':True, 'CYL': False,   'dataFields':{}},
        {'name':'cylConSlump',              'title':'Slump (mm)',                          'property':'slump',          'SCC':False, 'CYL':True,    'dataFields':{}},
        {'name':'cylConAir',                'title':'Air (%)',                             'property':'air',            'SCC':True, 'CYL':True,     'dataFields':{}},
        {'name':'cylConDensity',            'title':'Unit Density (kg/m<sup>3</sup>)',     'property':'density',        'SCC':True, 'CYL': True,    'dataFields':{}},
        {'name':'cylConSampleTemp',         'title':'Sample Temp (&deg;C)',                'property':'sampleTemp',     'SCC':True, 'CYL': True,    'dataFields':{}},
        {'name':'cylConAmbientTemp',        'title':'Ambient Temp (&deg;C)',               'property':'ambientTemp',    'SCC':True, 'CYL': True,    'dataFields':{}},
        {'name':'cylConInitialTemp',        'title':'Initial Curing Conditions (&deg;C)',  'property':'initialTemp',    'SCC':True, 'CYL': True,    'dataFields':{}},
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
        'name':'cylItem',   'title':'',   'labels': {},    'valueData':{}
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
        'date_specimen':               {'dataType': SQL.DATATYPES.DATETIME,    'size': None,                                    'data':None},
        'date_specimen_equal':         {'dataType': SQL.DATATYPES.BOOL,        'size': None,                                    'data':None},
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
        fieldTable = cls.__create_data_n_table(cls.FORM_FIELD_TEMPLATE, cls.FORM_LABELS)
        strTable = cls.__create_data_n_table(cls.FORM_STR_TEMPLATE, cls.STR_LABELS, cls.NUM_STR_TARGETS)
        conTable = cls.__create_data_n_table(cls.FORM_CONDITIONS_TEMPLATE, cls.CONDITIONS_LABELS)

        #Ensure first item is always visible
        strTable[0]['dataFields']['visible']['val'] = 1

        fieldTable = fieldTable[0]

        #Insert some default values
        fieldTable['dataFields']['projectID']['val'] = parent_id
        fieldTable['dataFields']['cylinderID']['val'] = cylinder_id
        fieldTable['dataFields']['dateCreated']['val'] = datetime.today()
        fieldTable['dataFields']['createdBy']['val'] = createdby
        fieldTable['dataFields']['reportTitle']['val'] = 'Report Title'
        fieldTable['dataFields']['status']['val'] = 'active'
        fieldTable['dataFields']['mouldType']['val'] = list(cls.MOULD_OPTIONS.keys())[0] #Get keys from dict, convert to list, get 0th item
        fieldTable['dataFields']['volumeUnits']['val'] = "meters"
        fieldTable['dataFields']['isScc']['val'] = "no"
        fieldTable['dataFields']['dateReceivedEqual']['val'] = "checked"
        fieldTable['dataFields']['dateSpecimenEqual']['val'] = "checked"


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
        report_sql = super().sql_fetchall(f"SELECT * FROM {cls.TB_REPORT_DATA} WHERE auto_id = %s", (id,)) #The (id,) is a tuple of values which corresponds to %s
        str_sql = super().sql_fetchall(f"SELECT * FROM {cls.TB_STR_REQ} WHERE cyl_report_id = %s ORDER BY auto_id ASC", (id,))
        con_sql = super().sql_fetchall(f"SELECT * FROM {cls.TB_CONDITIONS} WHERE cyl_report_id = %s ORDER BY auto_id ASC", (id,))
        cyl_items_sql = super().sql_fetchall(f"SELECT * FROM {cls.TB_CYLINDERS} WHERE cyl_report_id = %s ORDER BY auto_id ASC", (id,))

        fieldTable = cls.__create_data_n_table(cls.FORM_FIELD_TEMPLATE, cls.FORM_LABELS)
        strTable = cls.__create_data_n_table(cls.FORM_STR_TEMPLATE, cls.STR_LABELS, cls.NUM_STR_TARGETS)
        conTable = cls.__create_data_n_table(cls.FORM_CONDITIONS_TEMPLATE, cls.CONDITIONS_LABELS)
        cylTable = cls.__create_data_table(cls.FORM_ITEMS_TEMPLATE, cls.CYL_ITEMS_LABELS)

        field_result = cls.__sql_to_html_field(report_sql, fieldTable)
        str_result = cls.__sql_to_html_strength(str_sql, strTable, editing)
        con_result = cls.__sql_to_html_con(con_sql, conTable)
        cyl_items_result = cls.__sql_to_html_cyl_items(cyl_items_sql, cylTable)

        id = field_result['dataFields']['cylinderID']['val']

        data = {
            "fieldTable":field_result,
            "strTable": str_result,
            "conditionsTable": con_result,
            "cylItemsTable": cyl_items_result
        }

        return cls(data, id)

    @classmethod
    def __create_data_n_table(cls, formTemplate, formLabels, n = 1):
        '''
        Combine formTemplate with data from formLabels 'n' number of times, creating a list of dictionaries where each
        row is formatted to 'formTemplate'.

        -The 'name' key from formTemplate is combined with the 'label' keys from formLabels and assigned to the
        'dataFields' sub-dictionary of 'formTemplate'. They are combined in order to create unique identifiers for
            outputting to HTML. As the rows are outputted 'n' number of times, all values are appended with an index
            value starting at 0 or 1.

        :param formTemplate: A list of dictionary templates in the format below. Contains info about each row, with various
            properties such as name, title, and various custom fields.

         ex:    formTemplate = [
                    {'name': 'strTable', 'title': 'Title {n}', 'dataFields': {}}
                ]

        -'dataFields' has a key for each 'label' value of  formLabels
        -Each 'dataFields' key has the following sub-keys:
            label       The HTML name/ID
            val         Stored value if any
            dataType    Type of data used by JavaScript for realtime validation
            size        Size of the dataType
            errorLabel  The HTML name/ID of the element which outputs the error message

        :param formLabels: A list of dictionaries with several keys corresponding to HTML inputs. Each "row" of formTemplate
            will be populated and named with the info from formLabels

        [
          {'label':'strength',     'dataType':GLB.VALIDATION_TYPES['INT'],        'size':{'min': 0, 'max': 1000}},
          {'label':'days',         'dataType':GLB.VALIDATION_TYPES['INT'],        'size':{'min': 0, 'max': 1000}},
          {...},
        ]

        :param n: An integer specifying the number of rows to create
        :return: A unique (no references) list of dictionaries similar to the format of formTemplate. Each dictionary
            corresponds to a row to be output on the HTML page.
            [
                {
                    'name': 'strTable1',
                    'title': 'Target 1',
                    'dataFields': {
                        'strength':     {'label': 'strTableStrength1', 'val': None, 'dataType': 1, 'size': {'min': 0, 'max': 1000}, 'errorLabel': 'errorStrTableStrength1'},
                        'reportTitle':  {'label': 'strTableDays1', 'val': None, 'dataType': 1, 'size': {'min': 0, 'max': 1000}, 'errorLabel': 'errorStrTableDays1'},
                }
                {
                    'name': 'strTable2',
                    'title': '',
                    'dataFields': { ... }
                }
                {
                    'strTable3'
                }
            ]
        '''

        FUNC_NAME = " __create_data_n_table(cls, formTemplate, formLabels, n):"

        if(isinstance(n, int)):
            if(n < 0):
                print(f"Error: {FUNC_NAME}: n = {n} is < 0")
                return False
        else:
            print(f"Error: {FUNC_NAME}: n = {n} is not an integer")
            return False

        startVal = 1  #Start at 0 or 1

        dataList = []

        for i in range(n):
            #Don't include index value if only one loop
            if(n == 1):
                index = ''
            else:
                index = str(i + startVal)

            #Iterate through each row of the template and append values
            for item in formTemplate:
                data = copy.deepcopy(item) #Deepcopy the row
                data['title'] = data['title'].replace('{n}', index)   #Replace any instances of {n} in 'title' with index

                name = data['name']
                data['name'] = name + index #Concatenate the index value to the name

                for row in formLabels:
                    key = row['label']  #The key to be used with the 'data' dict is simply the 'label' key from the formLabels row
                    label = HLP.capitalizeFirst(key)
                    fullLabel = name + label + index
                    fieldData = {}  #Create a new dict to hold the curren key values

                    #Assign the key values to fieldData
                    fieldData['label'] = fullLabel
                    fieldData['val'] = ''
                    fieldData['dataType'] = row['dataType']
                    fieldData['size'] = copy.deepcopy(row['size'])
                    fieldData['errorLabel'] = 'error' + HLP.capitalizeFirst(fullLabel)

                    data['dataFields'][key] = fieldData

                dataList.append(data)

        return dataList

    @classmethod
    def __create_data_table(cls, template, formLabels):
        dataList = []

        for row in template:
            newRow = copy.deepcopy(row) #copy.deepcopy(): copies nested dicts as copy() alone passes references to nested dicts

            for key in formLabels:
                label = HLP.capitalizeFirst(key)
                newRow['labels'][key] = row['name'] + label
                newRow['valueData'][key] = ''

            dataList.append(newRow)

        return dataList

    @classmethod
    def __sql_to_html_field(self, sqlResult, formTable):
        formData = copy.deepcopy(formTable[0])
        sqlResult = processSql(sqlResult[0])

        #Assign the 'dataFields' sub-dict to dataFields (passes a reference so changes to dataFields will change formData)
        dataFields = formData['dataFields']

        dataFields['projectID']['val'] = sqlResult['project_id']
        dataFields['cylinderID']['val'] = sqlResult['auto_id']
        dataFields['dateCreated']['val'] = sqlResult['date_created']
        dataFields['createdBy']['val'] = sqlResult['created_by']
        dataFields['reportTitle']['val'] = sqlResult['report_title']
        dataFields['status']['val'] = sqlResult['status']
        dataFields['projectName']['val'] = sqlResult['project_name']
        dataFields['ticketNum']['val'] = sqlResult['ticket_num']
        dataFields['supplier']['val'] = sqlResult['supplier']
        dataFields['truckNum']['val'] = sqlResult['truck_num']
        dataFields['loadNum']['val'] = sqlResult['load_num']
        dataFields['contractor']['val'] = sqlResult['contractor']
        dataFields['sampledFrom']['val'] = sqlResult['sampled_from']
        dataFields['mixID']['val'] = sqlResult['mix_id']
        dataFields['mouldType']['val'] = sqlResult['mould_type']
        dataFields['poNum']['val'] = sqlResult['po_num']
        dataFields['placementType']['val'] = sqlResult['placement_type']
        dataFields['cementType']['val'] = sqlResult['cement_type']
        dataFields['volume']['val'] = sqlResult['load_volume']
        dataFields['volumeUnits']['val'] = sqlResult['load_volume_units']
        dataFields['castDate']['val'] = sqlResult['date_cast']
        dataFields['castTime']['val'] = sqlResult['time_cast']
        dataFields['batchTime']['val'] = sqlResult['time_batch']
        dataFields['sampleTime']['val'] = sqlResult['time_sample']
        dataFields['dateTransported']['val'] = sqlResult['date_transported']
        dataFields['dateReceived']['val'] = sqlResult['date_received']
        dataFields['dateSpecimen']['val'] = sqlResult['date_specimen']

        dataFields['notes']['val'] = sqlResult['notes']
        dataFields['isScc']['val'] = sqlResult['is_scc']

        # Do some processing for the dateReceivedEqual checkbox
        if (sqlResult['date_received_equal'] == 1):
            dataFields['dateReceivedEqual']['val'] = 'checked'
        else:
            dataFields['dateReceivedEqual']['val'] = ''

        # Do some processing for the dateSpecimenEqual
        if (sqlResult['date_specimen_equal'] == 1):
            dataFields['dateSpecimenEqual']['val'] = 'checked'
        else:
            dataFields['dateSpecimenEqual']['val'] = ''

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

        strenTable = copy.deepcopy(formTable)
        sqlResult = copy.deepcopy(sqlResult)

        #Ensure all None values are removed
        sqlResult = processSql(sqlResult)


        #Populate the strenTable with the SQL results
        for i, row in enumerate(sqlResult):
            data = strenTable[i]['dataFields']
            sqlData = sqlResult[i]
            data['strength']['val'] = sqlData['target_strength']
            data['days']['val'] = sqlData['target_days']

            # Ensure the first entry is visible
            if (i == 0):
                targetVisible = 1
            else:
                targetVisible = sqlData['target_visible']

            data['visible']['val'] = targetVisible
            data['autoID']['val'] = sqlData['auto_id']

            strList.append(strenTable[i])

        for item in strList:
            print(item)

        return strList

    @classmethod
    def __sql_to_html_con(self, sqlResult, formTable):
        newFormTable = copy.deepcopy(formTable)

        #Ensure all None values are removed
        sqlResult = processSql(sqlResult)

        #Ensure the 'property' fields match and populate the table
        for row in newFormTable:
            dataFields = row['dataFields']
            for sql in sqlResult:
                if(row['property'] == sql['property']):
                    dataFields['actual']['val'] = sql['val_actual']
                    dataFields['min']['val'] = sql['val_min']
                    dataFields['max']['val'] = sql['val_max']
                    dataFields['notes']['val'] = sql['notes']
                    dataFields['cylReportID']['val'] = sql['cyl_report_id']
                    dataFields['autoID']['val'] = sql['auto_id']
                    break

        return newFormTable

    @classmethod
    def __sql_to_html_cyl_items(self, sqlResult, formTable):
        sqlResult = processSql(sqlResult)

        newFormTable = []

        for i, row in enumerate(sqlResult):
            newFormTable.append(copy.deepcopy(formTable[0])) #copy the form table (which is only 1 row) as many times as there is SQL data

            newFormTable[i]['valueData']['itemID'] = row['item_id']
            newFormTable[i]['valueData']['dateReceived'] = row['date_received']
            newFormTable[i]['valueData']['dateTested'] = row['date_tested']
            newFormTable[i]['valueData']['age'] = row['age']
            newFormTable[i]['valueData']['diameter'] = row['diameter']
            newFormTable[i]['valueData']['length'] = row['length']
            newFormTable[i]['valueData']['area'] = row['area']
            newFormTable[i]['valueData']['weight'] = row['weight']
            newFormTable[i]['valueData']['strength'] = row['strength']
            newFormTable[i]['valueData']['breakType'] = row['break_type']
            newFormTable[i]['valueData']['percentStrength'] = row['percent_strength']
            newFormTable[i]['valueData']['initials'] = row['initials']

            newFormTable[i]['valueData']['autoID'] = row['auto_id']


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

        fieldData = fieldData[0]

        fieldData = fieldData['dataFields']

        sqlData['project_id']['data'] = fieldData['projectID']['val']
        sqlData['date_created']['data'] = fieldData['dateCreated']['val']
        sqlData['created_by']['data'] = fieldData['createdBy']['val']
        sqlData['report_title']['data'] = fieldData['reportTitle']['val']
        sqlData['status']['data'] = fieldData['status']['val']
        sqlData['is_scc']['data'] = fieldData['isScc']['val']
        sqlData['ticket_num']['data'] = fieldData['ticketNum']['val']
        sqlData['project_name']['data'] = fieldData['projectName']['val']
        sqlData['supplier']['data'] = fieldData['supplier']['val']
        sqlData['load_num']['data'] = fieldData['loadNum']['val']
        sqlData['truck_num']['data'] = fieldData['truckNum']['val']
        sqlData['contractor']['data'] = fieldData['contractor']['val']
        sqlData['sampled_from']['data'] = fieldData['sampledFrom']['val']
        sqlData['mould_type']['data'] = fieldData['mouldType']['val']
        sqlData['mix_id']['data'] = fieldData['mixID']['val']
        sqlData['po_num']['data'] = fieldData['poNum']['val']
        sqlData['placement_type']['data'] = fieldData['placementType']['val']
        sqlData['cement_type']['data'] = fieldData['cementType']['val']
        sqlData['load_volume']['data'] = fieldData['volume']['val']
        sqlData['load_volume_units']['data'] =  fieldData['volumeUnits']['val']
        sqlData['date_cast']['data'] = fieldData['castDate']['val']
        sqlData['time_batch']['data'] = fieldData['batchTime']['val']
        sqlData['time_sample']['data'] = fieldData['sampleTime']['val']
        sqlData['time_cast']['data'] = fieldData['castTime']['val']
        sqlData['date_transported']['data'] = fieldData['dateTransported']['val']
        sqlData['date_specimen']['data'] = fieldData['dateSpecimen']['val']
        sqlData['notes']['data'] = fieldData['notes']['val']

        sqlData['auto_id']['data'] = fieldData['cylinderID']['val']


        #Processing dateReceived checkbox. 'on' is what a checked checkbox returns if no value specified
        if(fieldData['dateReceivedEqual']['val'] == 'on'):
            sqlData['date_received_equal']['data'] = 1
            sqlData['date_received']['data'] = fieldData['dateTransported']['val']
        else:
            sqlData['date_received_equal']['data'] = 0
            sqlData['date_received']['data'] = fieldData['dateReceived']['val']

        #Processing dateSpecimen checkbox. 'on' is what a checked checkbox returns if no value specified
        if(fieldData['dateSpecimenEqual']['val'] == 'on'):
            sqlData['date_specimen_equal']['data'] = 1
            sqlData['date_specimen']['data'] = fieldData['castDate']['val']
        else:
            sqlData['date_specimen_equal']['data'] = 0
            sqlData['date_specimen']['data'] = fieldData['dateSpecimen']['val']



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

        :param conData: A list of dictionaries where each main key's value corresponds to HTML form input data. There is a 'valueData'
            sub-dictionary which will be populated with key:values which correspond to some SQL database columns
        :return: A list of dictionaries which correspond to a specific SQL table with clean data ready to be inserted into the
            database
        """

        dataList = []

        for row in conData:
            sqlData = copy.deepcopy(self.SQL_CONDITIONS_PROPERTIES)

            sqlData['cyl_report_id']['data'] = cylID
            sqlData['property']['data'] = row['property']
            sqlData['val_actual']['data'] = row['dataFields']['actual']['val']
            sqlData['val_min']['data'] = row['dataFields']['min']['val']
            sqlData['val_max']['data'] = row['dataFields']['max']['val']
            sqlData['notes']['data'] = row['dataFields']['notes']['val']
            sqlData['auto_id']['data'] = row['dataFields']['autoID']['val']
            dataList.append(sqlData)


        dataList = HLP.sql_sanitize(dataList)

        return dataList

    def __strength_form_to_sql(self, strData, cylID):
        """
        1. Assign the values from the 'strData' parameter to a specific SQL table
        2. Convert the result to a list
        3. Sanitize the data with a helper function
        4. Return the list

        :param strData: A lis of dictionaries corresponding to HTML form input data
        :return: A list of dictionaries which correspond to a specific SQL table with clean data ready to be inserted into the
            database
        """
        dataList = []

        for row in strData:
            sqlData = copy.deepcopy(self.SQL_STR_REQ_PROPERTIES.copy())
            dataFields = row['dataFields']

            sqlData['cyl_report_id']['data'] = cylID
            sqlData['target_strength']['data'] = dataFields['strength']['val']
            sqlData['target_days']['data'] = dataFields['days']['val']
            sqlData['target_visible']['data'] = dataFields['visible']['val']
            sqlData['auto_id']['data'] = dataFields['autoID']['val']
            dataList.append(sqlData)

        dataList = HLP.sql_sanitize(dataList)


        #Ensure the first item of the strength table is always visible
        dataList[0]['target_visible']['data'] = 1

        for row in dataList:
            print(row)

        return dataList

    #Convert object dict
    def to_dict(self):

        objectData = {
            "id":self.id,   #id is also in 'fieldTable', but this allows quick access
            "fieldTable":self.field_table,
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
            "statusData": self.STATUS_TABLE,
            "separatorData": self.SEPARATOR_OPTIONS,
            "setData": self.SET_OPTIONS
        }

        return dataTables
