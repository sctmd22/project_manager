from datetime import datetime
import json

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

    AIR_OPTIONS = {
        'custom':'As Measured',
        'natural':'Natural Air',
        'none':'No Air Spec'
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
        {'label': 'projectID'},
        {'label': 'cylinderID'},
        {'label': 'dateCreated'},
        {'label': 'createdBy'},
        {'label': 'reportTitle',        'dataType': GLB.VALIDATION_TYPES['TEXT'], 'maxlength': 255},
        {'label': 'status'},
        {'label': 'projectName',        'dataType': GLB.VALIDATION_TYPES['TEXT'], 'maxlength': 25},
        {'label': 'ticketNum',          'dataType': GLB.VALIDATION_TYPES['TEXT'], 'maxlength': 25},
        {'label': 'supplier',           'dataType': GLB.VALIDATION_TYPES['TEXT'], 'maxlength': 25},
        {'label': 'loadNum',            'dataType': GLB.VALIDATION_TYPES['TEXT'], 'maxlength': 25},
        {'label': 'truckNum',           'dataType': GLB.VALIDATION_TYPES['TEXT'], 'maxlength': 25},
        {'label': 'contractor',         'dataType': GLB.VALIDATION_TYPES['TEXT'], 'maxlength': 25},
        {'label': 'sampledFrom',        'dataType': GLB.VALIDATION_TYPES['TEXT'], 'maxlength': 25},
        {'label': 'mixID',              'dataType': GLB.VALIDATION_TYPES['TEXT'], 'maxlength': 25},
        {'label': 'mouldType',                                                                    },
        {'label': 'poNum',              'dataType': GLB.VALIDATION_TYPES['TEXT'], 'maxlength': 25},
        {'label': 'placementType',      'dataType': GLB.VALIDATION_TYPES['TEXT'], 'maxlength': 25},
        {'label': 'cementType',         'dataType': GLB.VALIDATION_TYPES['TEXT'], 'maxlength': 25},
        {'label': 'volume',             'dataType': GLB.VALIDATION_TYPES['NUMBER'], 'maxlength': 5, 'precision':2},
        {'label': 'volumeUnits',                                                                  },
        {'label': 'castDate',                                                                     },
        {'label': 'castTime',                                                                     },
        {'label': 'batchTime',                                                                    },
        {'label': 'sampleTime',                                                                   },
        {'label': 'dateTransported',                                                              },
        {'label': 'dateReceived',                                                                 },
        {'label': 'dateReceivedEqual',                                                            },
        {'label': 'dateSpecimen',                                                                 },
        {'label': 'dateSpecimenEqual',                                                            },
        {'label': 'notes',              'dataType': GLB.VALIDATION_TYPES['TEXT'], 'maxlength': 2000},
        {'label': 'isScc',                                                                         },
        {'label': 'airOptions',                                                                    },
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
        {'label':'visible', 'sqlID':'target_visible'},
        {'label':'autoID',  'sqlID':'auto_id'},
    ]

    FORM_STR_TEMPLATE = [
        {'name':'strTable',   'title':'Target {n}',   'dataFields':{}}
    ]


    CONDITIONS_LABELS = [
        {'label': 'actual',     'dataType': GLB.VALIDATION_TYPES['NUMBER'], 'maxlength': 7},
        {'label': 'min',        'dataType': GLB.VALIDATION_TYPES['NUMBER'], 'maxlength': 7},
        {'label': 'max',        'dataType': GLB.VALIDATION_TYPES['NUMBER'], 'maxlength': 7},
        {'label': 'notes',      'dataType': GLB.VALIDATION_TYPES['TEXT'],   'maxlength': 500},
        {'label': 'autoID'},
    ]

    #Template for field/measurement data and properties
        #'title': Used to output a text title in HTML
        #'property': These are stored as VARCHARs in SQL to keep track of each property. Also used to match the data when going from the HTML form to SQL and reverse
    FORM_CONDITIONS_TEMPLATE = [
        {'name':'cylConFlow',               'title':'Flow (mm)',                           'property':'flow',           'SCC':True, 'CYL': False,   'dataFields':{}, 'precision':{'actual': 0, 'min': 0, 'max': 0}},
        {'name':'cylConT50',                'title':'T<sub>50</sub>(s)',                   'property':'t_50',           'SCC':True, 'CYL': False,   'dataFields':{}, 'precision':{'actual': 0, 'min': 0, 'max': 0}},
        {'name':'cylConVSI',                'title':'VSI',                                 'property':'vsi',            'SCC':True, 'CYL': False,   'dataFields':{}, 'precision':{'actual': 0, 'min': 0, 'max': 0}},
        {'name':'cylConSlump',              'title':'Slump (mm)',                          'property':'slump',          'SCC':False, 'CYL':True,    'dataFields':{}, 'precision':{'actual': 0, 'min': 0, 'max': 0}},
        {'name':'cylConAir',                'title':'Air (%)',                             'property':'air',            'SCC':True, 'CYL':True,     'dataFields':{}, 'precision':{'actual': 1, 'min': 0, 'max': 0}},
        {'name':'cylConDensity',            'title':'Unit Density (kg/m<sup>3</sup>)',     'property':'density',        'SCC':True, 'CYL': True,    'dataFields':{}, 'precision':{'actual': 1, 'min': 0, 'max': 0}},
        {'name':'cylConSampleTemp',         'title':'Sample Temp (&deg;C)',                'property':'sampleTemp',     'SCC':True, 'CYL': True,    'dataFields':{}, 'precision':{'actual': 1, 'min': 0, 'max': 0}},
        {'name':'cylConAmbientTemp',        'title':'Ambient Temp (&deg;C)',               'property':'ambientTemp',    'SCC':True, 'CYL': True,    'dataFields':{}, 'precision':{'actual': 1, 'min': 0, 'max': 0}},
        {'name':'cylConInitialTemp',        'title':'Initial Curing Conditions (&deg;C)',  'property':'initialTemp',    'SCC':True, 'CYL': True,    'dataFields':{}, 'precision':{'actual': 1, 'min': 0, 'max': 0}},
    ]


    CYL_ITEMS_LABELS = [
        {'label': 'itemID',             'dataType': GLB.VALIDATION_TYPES['TEXT'],   'maxlength': 16},
        {'label': 'dateReceived',       'dataType': GLB.VALIDATION_TYPES['TEXT'],   'maxlength': 10},
        {'label': 'dateTested',         'dataType': GLB.VALIDATION_TYPES['TEXT'],   'maxlength': 10},
        {'label': 'age',                'dataType': GLB.VALIDATION_TYPES['TEXT'],   'maxlength': 3},
        {'label': 'diameter',           'dataType': GLB.VALIDATION_TYPES['NUMBER'], 'maxlength': 3, 'precision':0},
        {'label': 'length',             'dataType': GLB.VALIDATION_TYPES['NUMBER'], 'maxlength': 3, 'precision':0},
        {'label': 'area',               'dataType': GLB.VALIDATION_TYPES['NUMBER'], 'maxlength': 5, 'precision':0, 'disabled':True},
        {'label': 'weight',             'dataType': GLB.VALIDATION_TYPES['NUMBER'], 'maxlength': 6, 'precision':1},
        {'label': 'strength',           'dataType': GLB.VALIDATION_TYPES['NUMBER'], 'maxlength': 6, 'precision':2},
        {'label': 'breakType',          'dataType': GLB.VALIDATION_TYPES['NUMBER'], 'maxlength': 1, 'precision':0},
        {'label': 'requiredStrength',   'dataType': GLB.VALIDATION_TYPES['NUMBER'], 'maxlength': 6, 'precision':0, 'disabled':True},
        {'label': 'percentStrength',    'dataType': GLB.VALIDATION_TYPES['NUMBER'], 'maxlength': 4, 'precision':0, 'disabled':True},
        {'label': 'initials',           'dataType': GLB.VALIDATION_TYPES['TEXT'],   'maxlength': 3},
        {'label': 'autoID'},

    ]


    FORM_ITEMS_TEMPLATE = [
        {'name':'cylItem',   'title':'',   'dataFields':{}}
    ]

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
        'load_volume':                 {'dataType': SQL.DATATYPES.VARCHAR_DECIMAL,     'size': 10,                              'data':None},
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
        'air_options':                 {'dataType': SQL.DATATYPES.ENUM,        'size': None, 'enums':AIR_OPTIONS,               'data':None},
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
        self.cyl_items_table_template = data['cylItemsTableTemplate']

    #Create a new cylinder report with default values
    @classmethod
    def create_default(cls):
        parent_id = None
        cylinder_id = 0
        createdby = 'admin'

        #Create data tables from templates
        fieldTable = cls.__create_data_n_table(cls.FORM_FIELD_TEMPLATE, cls.FORM_LABELS)
        strTable = cls.__create_data_n_table(cls.FORM_STR_TEMPLATE, cls.STR_LABELS, cls.NUM_STR_TARGETS)
        conTable = cls.__create_data_n_table(cls.FORM_CONDITIONS_TEMPLATE, cls.CONDITIONS_LABELS)
        cylTable = cls.__create_data_n_table(cls.FORM_ITEMS_TEMPLATE, cls.CYL_ITEMS_LABELS)

        #Ensure first item is always visible
        strTable[0]['dataFields']['visible']['val'] = 1

        #Re-assign list as dict
        fieldTable = fieldTable[0]

        #Insert some default values
        fieldTable['dataFields']['projectID']['val'] = parent_id
        fieldTable['dataFields']['cylinderID']['val'] = cylinder_id
        fieldTable['dataFields']['dateCreated']['val'] = HLP.dateToStr(datetime.today(), GLB.DATE_FORMATS.ISO_DATE_FORMAT.value)
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
            "cylItemsTable": cylTable,
            "cylItemsTableTemplate": cylTable
        }

        #Call the CylinderReport constructor to create a class instance with the default data
        return cls(defaultData, cylinder_id)

    @classmethod
    def create_from_db(cls, id):
        #Get database values
        report_sql = super().sql_fetchall(f"SELECT * FROM {cls.TB_REPORT_DATA} WHERE auto_id = %s", (id,)) #The (id,) is a tuple of values which corresponds to %s
        str_sql = super().sql_fetchall(f"SELECT * FROM {cls.TB_STR_REQ} WHERE cyl_report_id = %s ORDER BY auto_id ASC", (id,))
        con_sql = super().sql_fetchall(f"SELECT * FROM {cls.TB_CONDITIONS} WHERE cyl_report_id = %s ORDER BY auto_id ASC", (id,))
        cyl_items_sql = super().sql_fetchall(f"SELECT * FROM {cls.TB_CYLINDERS} WHERE cyl_report_id = %s ORDER BY auto_id ASC", (id,))

        fieldTable = cls.__create_data_n_table(cls.FORM_FIELD_TEMPLATE, cls.FORM_LABELS)
        strTable = cls.__create_data_n_table(cls.FORM_STR_TEMPLATE, cls.STR_LABELS, cls.NUM_STR_TARGETS)
        conTable = cls.__create_data_n_table(cls.FORM_CONDITIONS_TEMPLATE, cls.CONDITIONS_LABELS)
        cylTable = cls.__create_data_n_table(cls.FORM_ITEMS_TEMPLATE, cls.CYL_ITEMS_LABELS)

        field_result = cls.__sql_to_html_field(report_sql, fieldTable)
        str_result = cls.__sql_to_html_strength(str_sql, strTable)
        con_result = cls.__sql_to_html_con(con_sql, conTable)
        cyl_items_result = cls.__sql_to_html_cyl_items(cyl_items_sql, cylTable)

        id = field_result['dataFields']['cylinderID']['val']

        data = {
            "fieldTable":field_result,
            "strTable": str_result,
            "conditionsTable": con_result,
            "cylItemsTable": cyl_items_result,
            "cylItemsTableTemplate":cylTable
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
                    'name': 'strTableRow1',
                    'title': 'Target 1',
                    'dataFields': {
                        'strength':     {'label': 'strTableStrength1', 'val': None, 'dataType': 1, 'size': {'min': 0, 'max': 1000}, 'errorLabel': 'errorStrTableStrength1'},
                        'reportTitle':  {'label': 'strTableDays1', 'val': None, 'dataType': 1, 'size': {'min': 0, 'max': 1000}, 'errorLabel': 'errorStrTableDays1'},
                }
                {
                    'name': 'strTableRow2',
                    'title': '',
                    'dataFields': { ... }
                }
                {
                    'strTableRow3'
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
                data['name'] = name + "Row" + index #Concatenate 'Row' and the index value to the name. Can be used as for each row name/ID

                precisionData = None

                #Precision precedence: Row/template > col/Labels. If precision is specified on the row (template) level, populate
                    #the 'precision' properties for each individual label with those values
                if('precision' in data):
                    precisionData = data['precision']
                    data.pop('precision') #remove precision date from the row


                for row in formLabels:
                    key = row['label']  #The key to be used with the 'data' dict is simply the 'label' key from the formLabels row
                    label = HLP.capitalizeFirst(key)
                    fullLabel = name + label + index
                    fieldData = {}  #Create a new dict to hold the curren key values

                    #Assign the key values to fieldData
                    fieldData['label'] = fullLabel
                    fieldData['val'] = ''

                    if ('size' in row):
                        fieldData['size'] = copy.deepcopy(row['size'])
                    else:
                        fieldData['size'] = None

                    if ('maxlength' in row):
                        fieldData['maxlength'] = row['maxlength']
                    else:
                        fieldData['maxlength'] = None

                    if ('dataType' in row):
                        fieldData['dataType'] = row['dataType']
                    else:
                        fieldData['dataType'] = None

                    #Use row/template precision data first
                    if(precisionData):
                        if(key in precisionData):
                            fieldData['precision'] = precisionData[key]

                    #Use col/label precision second
                    elif('precision' in row):
                        fieldData['precision'] = row['precision']
                    else:
                        fieldData['precision'] = None

                    if('disabled' in row):
                        fieldData['disabled'] = 'disabled'
                    else:
                        fieldData['disabled'] = ''


                    fieldData['errorLabel'] = 'error' + HLP.capitalizeFirst(fullLabel)

                    data['dataFields'][key] = fieldData


                dataList.append(data)



        return dataList

    @classmethod
    def __sql_to_html_field(self, sqlResult, formTable):
        '''
            Assign sqlResult data to the formTable template
        :param sqlResult: A list which should only ever contain 1 dictionary
        :param formTable:
        :return:
        '''
        formData = copy.deepcopy(formTable[0])
        sqlResult = processSql(sqlResult[0])

        #Assign the 'dataFields' sub-dict to dataFields (passes a reference so changes to dataFields will change formData)
        dataFields = formData['dataFields']

        dateCreated = HLP.dateToStr(sqlResult['date_created'], GLB.DATE_FORMATS.ISO_DATE_FORMAT.value)

        dateTransported = HLP.dateToStr(sqlResult['date_transported'], GLB.DATE_FORMATS.SIMPLE_DATE_FORMAT.value)
        dateCast = HLP.dateToStr(sqlResult['date_cast'], GLB.DATE_FORMATS.SIMPLE_DATE_FORMAT.value)
        dateReceived = HLP.dateToStr(sqlResult['date_received'], GLB.DATE_FORMATS.SIMPLE_DATE_FORMAT.value)
        dateSpecimen = HLP.dateToStr(sqlResult['date_specimen'], GLB.DATE_FORMATS.SIMPLE_DATE_FORMAT.value)

        dataFields['projectID']['val'] = sqlResult['project_id']
        dataFields['cylinderID']['val'] = sqlResult['auto_id']
        dataFields['dateCreated']['val'] = dateCreated
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
        dataFields['castDate']['val'] = dateCast
        dataFields['castTime']['val'] = sqlResult['time_cast']
        dataFields['batchTime']['val'] = sqlResult['time_batch']
        dataFields['sampleTime']['val'] = sqlResult['time_sample']
        dataFields['dateTransported']['val'] = dateTransported
        dataFields['dateReceived']['val'] = dateReceived
        dataFields['dateSpecimen']['val'] = dateSpecimen
        dataFields['airOptions']['val'] = sqlResult['air_options']

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
    def __sql_to_html_strength(self, sqlResult, formTable):
        """
        Assign SQL data to FORM template

        :param sqlResult: List of SQL results as dictionaries.
        :param formTable: List of HTML form values and properties as dictionaries. Each row corresponds to a group of
            HTML input elements and properties.
        :param editing: Boolean. True if the form is being edited, false otherwise
        :return: A list dictionaries, each dictioanry corresponding to HTML form values and properties
        """
        strList = []

        strenTable = copy.deepcopy(formTable)
        sqlResult = copy.deepcopy(sqlResult)

        sqlResult = processSql(sqlResult)

        #Populate the strenTable with the SQL results
        for i, sqlRow in enumerate(sqlResult):
            data = strenTable[i]['dataFields']  #data takes a reference to strenTable[i]['dataFields']

            data['strength']['val'] = sqlRow['target_strength']
            data['days']['val'] = sqlRow['target_days']

            # Ensure the first entry is visible
            if (i == 0):
                targetVisible = 1
            else:
                targetVisible = sqlRow['target_visible']

            data['visible']['val'] = targetVisible
            data['autoID']['val'] = sqlRow['auto_id']

            strList.append(strenTable[i])

        return strList

    @classmethod
    def __sql_to_html_con(self, sqlResult, formTable):
        newFormTable = copy.deepcopy(formTable)

        sqlResult = processSql(sqlResult)

        #Ensure the 'property' fields match and populate the table
        for row in newFormTable:
            dataFields = row['dataFields'] #assign dataFields a reference to row['dataFields']
            for sqlRow in sqlResult:
                if(row['property'] == sqlRow['property']):
                    dataFields['actual']['val'] = sqlRow['val_actual']
                    dataFields['min']['val'] = sqlRow['val_min']
                    dataFields['max']['val'] = sqlRow['val_max']
                    dataFields['notes']['val'] = sqlRow['notes']
                    dataFields['autoID']['val'] = sqlRow['auto_id']
                    break

        return newFormTable

    @classmethod
    def __sql_to_html_cyl_items(self, sqlResult, formTable):
        '''

        :param sqlResult: A list of dicts, where each dictionary corresponds to individual cylinder data
        :param formTable: A list containing a single dict which is a template corresponding to HTML outputs and properties
            to be populated with sqlResult data.

        :return: A list of dicts
        '''

        sqlResult = processSql(sqlResult)

        newFormTable = []

        for sqlRow in sqlResult:
            newRow = copy.deepcopy(formTable[0])  #copy the formTable template as many times as there is SQL data
            dataFields = newRow['dataFields']   #assign dataFields a reference to newRow['dataFields']

            dateReceived = HLP.dateToStr(sqlRow['date_received'], GLB.DATE_FORMATS.SIMPLE_DATE_FORMAT.value)
            dateTested = HLP.dateToStr(sqlRow['date_tested'], GLB.DATE_FORMATS.SIMPLE_DATE_FORMAT.value)

            dataFields['itemID']['val'] = sqlRow['item_id']
            dataFields['dateReceived']['val'] = dateReceived
            dataFields['dateTested']['val'] = dateTested
            dataFields['age']['val'] = sqlRow['age']
            dataFields['diameter']['val'] = sqlRow['diameter']
            dataFields['length']['val'] = sqlRow['length']
            dataFields['area']['val'] = sqlRow['area']
            dataFields['weight']['val'] = sqlRow['weight']
            dataFields['strength']['val'] = sqlRow['strength']
            dataFields['breakType']['val'] = sqlRow['break_type']
            dataFields['percentStrength']['val'] = sqlRow['percent_strength']
            dataFields['initials']['val']= sqlRow['initials']

            dataFields['autoID']['val'] = sqlRow['auto_id']
            newFormTable.append(newRow)


        return newFormTable

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
        sqlData['air_options']['data'] = fieldData['airOptions']['val']

        sqlData['auto_id']['data'] = fieldData['cylinderID']['val']

        self.airOptionVal = fieldData['airOptions']['val']

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
            property = row['property']

            minVal = row['dataFields']['min']['val']
            maxVal = row['dataFields']['max']['val']

            if(property == 'air'):
                if(not self.airOptionVal == 'custom'):
                    minVal = None
                    maxVal = None

            sqlData['property']['data'] = property
            sqlData['val_actual']['data'] = row['dataFields']['actual']['val']
            sqlData['val_min']['data'] = minVal
            sqlData['val_max']['data'] = maxVal
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

        return dataList

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

    #Convert object dict
    def to_dict(self):

        objectData = {
            "id":self.id,   #id is also in 'fieldTable', but this allows quick access
            "fieldTable":self.field_table,
            "strTable": self.strength_table,
            "conditionsTable": self.conditions_table,
            "cylItemsTable": self.cyl_items_table,
            "cylItemsTableTemplate":self.cyl_items_table_template
        }

        return objectData


    def to_json(self):
        data = self.to_dict()

        return json.dumps(data)


    #Return data tables as dicts
    def tables_to_dict(self):
        dataTables = {
            "loadVolumeData": self.UNITS_OPTIONS,
            "mouldData": self.MOULD_OPTIONS,
            "sccData": self.SCC_OPTIONS,
            "statusData": self.STATUS_TABLE,
            "separatorData": self.SEPARATOR_OPTIONS,
            "setData": self.SET_OPTIONS,
            "airOptions":self.AIR_OPTIONS,
        }

        return dataTables
