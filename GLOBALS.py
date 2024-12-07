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

LOAD_VOLUME_UNITS = [
    "meters",
    "yards"
]


PROJECT_STATUS = {
    'active': "Active",
    'complete': "Complete",
    'deleted': "Deleted",
    'canceled': "Canceled"
}


''''
#Define an enum for project status. 
class PROJECT_STATUS(Enum):
    ACTIVE = 'active'
    COMPLETE = 'complete'
    DELETED = 'deleted'
    CANCELED = 'canceled'


PROJECT_STATUS_OPTIONS = {
    PROJECT_STATUS.ACTIVE: "Active",
    PROJECT_STATUS.COMPLETE: "Complete",
    PROJECT_STATUS.DELETED: "Deleted",
    PROJECT_STATUS.CANCELED: "Canceled"
}
'''
