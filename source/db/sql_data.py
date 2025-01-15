from enum import Enum

class SQL_DATATYPES(Enum):
    VARCHAR = 1,
    TEXT = 2,
    INT = 3,
    TINY_INT = 4,
    SMALL_INT = 5,
    DATETIME = 6,
    TIME = 7,
    ENUM = 8

SQL_INT_SIZES = {
    'TINY_INT':     {'MIN':0, 'MAX':255},
    'SMALL_INT':    {'MIN':-32768, 'MAX':32767},
    'INT':          {'MIN':-2147483648, 'MAX':2147483647}
}

SQL_TEXT_SIZES = {
    'TEXT':65535,
    'MEDIUM_TEXT':16777215,
    'LONGTEXT':4294967295
}

class CYL_STATUS(Enum):
    ACTIVE = 'active',
    COMPLETE = 'complete',
    CANCELED = 'canceled',
    DELETED = 'deleted'

class CYL_SCC(Enum):
    YES = 'yes',
    NO = 'no'

class CYL_MOULDS(Enum):
    NORMAL = '100x200_plastic',
    LARGE = '150x300_plastic'

class CYL_UNITS(Enum):
    METERS = 'meters',
    YARDS = 'yards'


SQL_CON_DATA_COLS = [
    'cyl_report_id',
    'property',
    'val_actual',
    'val_min',
    'val_max',
    'notes',
    'val_actual_precision',
    'val_min_precision',
    'val_max_precision'
]


SQL_CYL_CONDITIONS_PROPERTIES = [
    {'column':'cyl_report_id',          'dataType':SQL_DATATYPES.INT,       'size': SQL_INT_SIZES['INT']},
    {'column':'property',               'dataType':SQL_DATATYPES.VARCHAR,   'size': 255},
    {'column':'val_actual',             'dataType':SQL_DATATYPES.VARCHAR,   'size': 15},
    {'column':'val_min',                'dataType':SQL_DATATYPES.VARCHAR,   'size': 15},
    {'column':'val_max',                'dataType':SQL_DATATYPES.VARCHAR,   'size': 15},
    {'column':'notes',                  'dataType':SQL_DATATYPES.VARCHAR,   'size': 1000},
    {'column': 'val_actual_precision',  'dataType':SQL_DATATYPES.TINY_INT,   'size': SQL_INT_SIZES['TINY_INT']},
    {'column': 'val_min_precision',     'dataType':SQL_DATATYPES.TINY_INT,   'size': SQL_INT_SIZES['TINY_INT']},
    {'column': 'val_max_precision',     'dataType':SQL_DATATYPES.TINY_INT,   'size': SQL_INT_SIZES['TINY_INT']},
]



SQL_CYL_REPORT_PROPERTIES = {
    'project_id':                  {'dataType': SQL_DATATYPES.INT,         'size': SQL_INT_SIZES['INT']},
    'date_created':                {'dataType': SQL_DATATYPES.DATETIME,    'size': None},
    'created_by':                  {'dataType': SQL_DATATYPES.VARCHAR,     'size': 50},
    'report_title':                {'dataType': SQL_DATATYPES.VARCHAR,     'size': 255},
    'status':                      {'dataType': SQL_DATATYPES.ENUM,        'size': None, 'enums': CYL_STATUS},
    'is_scc':                      {'dataType': SQL_DATATYPES.ENUM,        'size': None, 'enums': CYL_SCC},
    'ticket_num':                  {'dataType': SQL_DATATYPES.VARCHAR,     'size': 50},
    'project_name':                {'dataType': SQL_DATATYPES.VARCHAR,     'size': 50},
    'supplier':                    {'dataType': SQL_DATATYPES.VARCHAR,     'size': 50},
    'load_num':                    {'dataType': SQL_DATATYPES.VARCHAR,     'size': 50},
    'truck_num':                   {'dataType': SQL_DATATYPES.VARCHAR,     'size': 50},
    'contractor':                  {'dataType': SQL_DATATYPES.VARCHAR,     'size': 50},
    'sampled_from':                {'dataType': SQL_DATATYPES.VARCHAR,     'size': 50},
    'mould_type':                  {'dataType': SQL_DATATYPES.ENUM,        'size': None, 'enums': CYL_MOULDS},
    'mix_id':                      {'dataType': SQL_DATATYPES.VARCHAR,     'size': 50},
    'po_num':                      {'dataType': SQL_DATATYPES.VARCHAR,     'size': 50},
    'placement_type':              {'dataType': SQL_DATATYPES.VARCHAR,     'size': 50},
    'cement_type':                 {'dataType': SQL_DATATYPES.VARCHAR,     'size': 50},
    'load_volume':                 {'dataType': SQL_DATATYPES.VARCHAR,     'size': 50},
    'load_volume_units':           {'dataType': SQL_DATATYPES.ENUM,        'size': None, 'enums': CYL_UNITS},
    'date_cast':                   {'dataType': SQL_DATATYPES.VARCHAR,     'size': 50},
    'time_batch':                  {'dataType': SQL_DATATYPES.TIME,        'size': None},
    'time_sample':                 {'dataType': SQL_DATATYPES.TIME,        'size': None},
    'time_cast':                   {'dataType': SQL_DATATYPES.TIME,        'size': None},
    'date_transported':            {'dataType': SQL_DATATYPES.DATETIME,    'size': None},
    'notes':                       {'dataType': SQL_DATATYPES.TEXT,        'size': SQL_TEXT_SIZES['TEXT']}
}



'''
SQL_CYL_REPORT_PROPERTIES = [
    {'column': 'project_id',         'dataType': SQL_DATATYPES.INT,         'size':SQL_INT_SIZES['INT']},
    {'column': 'date_created',       'dataType': SQL_DATATYPES.DATETIME,    'size':None},
    {'column': 'created_by',         'dataType': SQL_DATATYPES.VARCHAR,     'size':50},
    {'column': 'report_title',       'dataType': SQL_DATATYPES.VARCHAR,     'size':255},
    {'column': 'status',             'dataType': SQL_DATATYPES.ENUM,        'size':None, 'enums':CYL_STATUS},
    {'column': 'is_scc',             'dataType': SQL_DATATYPES.ENUM,        'size':None, 'enums':CYL_SCC},
    {'column': 'ticket_num',         'dataType': SQL_DATATYPES.VARCHAR,     'size':50},
    {'column': 'project_name',       'dataType': SQL_DATATYPES.VARCHAR,     'size':50},
    {'column': 'supplier',           'dataType': SQL_DATATYPES.VARCHAR,     'size':50},
    {'column': 'load_num',           'dataType': SQL_DATATYPES.VARCHAR,     'size':50},
    {'column': 'truck_num',          'dataType': SQL_DATATYPES.VARCHAR,     'size':50},
    {'column': 'contractor',         'dataType': SQL_DATATYPES.VARCHAR,     'size':50},
    {'column': 'sampled_from',       'dataType': SQL_DATATYPES.VARCHAR,     'size':50},
    {'column': 'mould_type',         'dataType': SQL_DATATYPES.ENUM,        'size':None, 'enums':CYL_MOULDS},
    {'column': 'mix_id',             'dataType': SQL_DATATYPES.VARCHAR,     'size':50},
    {'column': 'po_num',             'dataType': SQL_DATATYPES.VARCHAR,     'size':50},
    {'column': 'placement_type',     'dataType': SQL_DATATYPES.VARCHAR,     'size':50},
    {'column': 'cement_type',        'dataType': SQL_DATATYPES.VARCHAR,     'size':50},
    {'column': 'load_volume',        'dataType': SQL_DATATYPES.VARCHAR,     'size':50},
    {'column': 'load_volume_units',  'dataType': SQL_DATATYPES.ENUM,        'size':None, 'enums':CYL_UNITS},
    {'column': 'date_cast',          'dataType': SQL_DATATYPES.VARCHAR,     'size':50},
    {'column': 'time_batch',         'dataType': SQL_DATATYPES.TIME,        'size':None},
    {'column': 'time_sample',        'dataType': SQL_DATATYPES.TIME,        'size':None},
    {'column': 'time_cast',          'dataType': SQL_DATATYPES.TIME,        'size':None},
    {'column': 'date_transported',   'dataType': SQL_DATATYPES.DATETIME,    'size':None},
    {'column': 'notes',              'dataType': SQL_DATATYPES.TEXT,        'size':None}

]
'''

SQL_CYL_STR_REQ_PROPERTIES = [
    {'column': 'cyl_report_id',      'dataType': SQL_DATATYPES.INT,     'size':SQL_INT_SIZES['INT']},
    {'column': 'target_strength',    'dataType': SQL_DATATYPES.INT,     'size':SQL_INT_SIZES['INT']},
    {'column': 'target_days',        'dataType': SQL_DATATYPES.INT,     'size':SQL_INT_SIZES['INT']},
    {'column': 'report_title',       'dataType': SQL_DATATYPES.INT,     'size':SQL_INT_SIZES['INT']},

]
