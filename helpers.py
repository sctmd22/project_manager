from _datetime import datetime

GLB_project_status = {
    0: "Active",
    1: "Completed",
    2: "Deleted",
    3: "Canceled"
}

SQL_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

def get_SQL_timestamp():
    return datetime.today().strftime(SQL_TIME_FORMAT)

