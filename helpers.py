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