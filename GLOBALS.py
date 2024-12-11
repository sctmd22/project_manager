from enum import Enum

SQL_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
SIMPLE_DATE_FORMAT = '%Y-%m-%d'
SQL_TIME_FORMAT = "%H:%M:%S"

HTML_TIME_FORMAT = "%H:%M"
HTML_DATE_FORMAT = "%Y-%m-%d"



MOULD_TYPES = {
    "100x200_plastic":"100x200 Plastic",
    "150x300_plastic":"150x300 Plastic",
}

LOAD_VOLUME_UNITS = {
    "meters":"m",
    "yards":"yd"
}

#Number of decimals to display when viewing a report
    #As of 2024-12-10 it is stored in myssql as 3 digits
LOAD_VOLUME_PRECISION = 1

PROJECT_STATUS = {
    'active': "Active",
    'complete': "Complete",
    'deleted': "Deleted",
    'canceled': "Canceled"
}



#Max characters for each VARCHAR type
CYL_DATA_LIMITS = {
    'created_by':50,
    'report_title':255,
    'ticket_num':50,
    'project_name':50,
    'supplier':50,
    'load_num':50,
    'truck_num':50,
    'contractor':50,
    'sampled_from':50,
    'mix_id':50,
    'po_num':50,
    'placement_type':50,
    'cement_type':50,
    'load_volume':50

}


CYL_CONDITIONS_TABLE = [
    {'name':'Flow (mm)', 'property': 'flow', 'id':'cylConFlow', 'notesID':'cylConFlowNotes', 'SCC':True, 'CYL': False},
    {'name':'T<sub>50</sub>(s)', 'property': 't_50', 'id':'cylConT50', 'notesID':'cylConT50Notes', 'SCC':True, 'CYL': False},
    {'name':'VSI', 'property': 'vsi', 'id':'cylConVSI', 'notesID':'cylConVSINotes', 'SCC':True, 'CYL': False},
    {'name':'Slump (mm)', 'property': 'slump', 'id':'cylConSlump', 'notesID':'cylConSlumpNotes', 'SCC':False, 'CYL':True},
    {'name':'Air (%)', 'property':'air', 'id':'cylConAir', 'notesID':'cylConAirNotes', 'SCC':True, 'CYL':True},
    {'name':'Unit Density (kg/m<sup>3</sup>)', 'property':'density', 'id':'cylConDensity', 'notesID':'cylConDensityNotes', 'SCC':True, 'CYL': True},
    {'name':'Sample Temp (&deg;C)', 'property':'sampleTemp', 'id':'cylConSampleTemp', 'notesID':'cylConSampleTempNotes', 'SCC':True, 'CYL': True},
    {'name':'Ambient Temp (&deg;C)', 'property':'ambientTemp', 'id':'cylConAmbientTemp', 'notesID':'cylConAmbientTempNotes', 'SCC':True, 'CYL': True},
    {'name':'Initial Curing Conditions (&deg;C)', 'property':'initialTemp', 'id':'cylConInitialTemp', 'notesID':'cylConInitialTempNotes', 'SCC':True, 'CYL': True},
]

