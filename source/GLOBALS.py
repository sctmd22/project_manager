HTML_TIME_FORMAT = "%H:%M"
HTML_TIME_FORMAT_S = HTML_TIME_FORMAT + ":%S"

HTML_DATE_FORMAT = "%Y-%m-%d"


PROJECT_STATUS = {
    'active': "Active",
    'complete': "Complete",
    'deleted': "Deleted",
    'canceled': "Canceled"
}

CYL_MOULD_TYPES = {
    "100x200_plastic":"100x200 Plastic",
    "150x300_plastic":"150x300 Plastic",
}

CYL_LOAD_VOLUME_UNITS = {
    "meters":"m",
    "yards":"yd"
}

CYL_NUM_STR_TARGETS = 5


CYL_SCC_RADIO = {
    'no':'No',
    'yes':'Yes'
}



CYL_FORM_FIELD_LIST = [
    'cylinderID',
    'dateCreated',
    'createdBy',
    'cylTitle',
    'cylStatus',
    'cylProject',
    'cylTicket',
    'cylSupplier',
    'cylLoadNum',
    'cylTruckNum',
    'cylContractor',
    'cylSampled',
    'cylMix',
    'cylMouldType',
    'cylPONum',
    'cylPlacement',
    'cylCement',
    'cylVolume',
    'cylVolumeUnits',
    'cylCastDate',
    'cylCastTime',
    'cylBatchTime',
    'cylSampleTime',
    'cylDateTransported',
    'cylNotes',
    'cylSCC'
]


CYL_CONDITIONS_SUFFIX ={
    'actual':'Actual',
    'min':'Min',
    'max':'Max',
    'notes':'Notes',
    'id':'ID'
}


CYL_CONDITIONS_TABLE = [
    {'title':'Flow (mm)',                           'property':'flow',          'name':'cylConFlow',            'SCC':True, 'CYL': False, 'suffix':CYL_CONDITIONS_SUFFIX},
    {'title':'T<sub>50</sub>(s)',                   'property':'t_50',          'name':'cylConT50',             'SCC':True, 'CYL': False, 'suffix':CYL_CONDITIONS_SUFFIX},
    {'title':'VSI',                                 'property':'vsi',           'name':'cylConVSI',             'SCC':True, 'CYL': False, 'suffix':CYL_CONDITIONS_SUFFIX},
    {'title':'Slump (mm)',                          'property':'slump',         'name':'cylConSlump',           'SCC':False, 'CYL':True, 'suffix':CYL_CONDITIONS_SUFFIX},
    {'title':'Air (%)',                             'property':'air',           'name':'cylConAir',             'SCC':True, 'CYL':True, 'suffix':CYL_CONDITIONS_SUFFIX},
    {'title':'Unit Density (kg/m<sup>3</sup>)',     'property':'density',       'name':'cylConDensity',         'SCC':True, 'CYL': True, 'suffix':CYL_CONDITIONS_SUFFIX},
    {'title':'Sample Temp (&deg;C)',                'property':'sampleTemp',    'name':'cylConSampleTemp',      'SCC':True, 'CYL': True, 'suffix':CYL_CONDITIONS_SUFFIX},
    {'title':'Ambient Temp (&deg;C)',               'property':'ambientTemp',   'name':'cylConAmbientTemp',     'SCC':True, 'CYL': True, 'suffix':CYL_CONDITIONS_SUFFIX},
    {'title':'Initial Curing Conditions (&deg;C)',  'property':'initialTemp',   'name':'cylConInitialTemp',     'SCC':True, 'CYL': True, 'suffix':CYL_CONDITIONS_SUFFIX},
]

