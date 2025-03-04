import datetime
import decimal

from datetime import datetime, timedelta

import GLOBALS as GB
import classes as CLS
from decimal import Decimal, ROUND_HALF_UP
from helpers import helpers as HLP

def strip_date_f(date):

    try:
        newDate = date.strftime('%I:%M')

    except:
        return date

    return newDate

def date_created_f(date):
    """Custom Jinja filter to format start_dates in project reports"""

    newDate = HLP.parseDate(date, GB.DATE_FORMATS)

    try:
        newDate = newDate.strftime('%B %d, %Y - %I:%M:%S %p')

    except:
        return date

    return newDate



def start_date_f(date):
    """Custom Jinja filter to format start_dates in project reports"""

    try:
        newDate = date.strftime('%B %d, %Y (%Y-%m-%d)')

    except:
        return date

    return newDate


def strip_time_f(date):
    """Custom Jinja filter to strip time from a datetime."""
    if(date == None):
        return ""

    try:
        timeless = date.strftime('%Y-%m-%d')

    except:
        return date

    return timeless


def short_description_f(description):
    charLimit = 50

    if(description == ""):
        return ""

    return description[0:charLimit] + "..."

def project_status_f(status):
    '''Convert status into to text'''
    try:
        statusText = CLS.Reports.STATUS_TABLE[status]


    except:
        return status

    return statusText

def strip_seconds_f(inputTime):

    strTime = str(inputTime)

    lenTime = len(strTime)

    if(lenTime == 8):
        return strTime[:5]

    return ""


def mould_f(mould):
    funcName = "mould_format() (filter)"
    if(not mould):
        return ""

    try:
        fMould = CLS.CylinderReport.MOULD_OPTIONS[mould]

    except:
        print(f"Error: {funcName}: No key matching '{mould}' from GB.MOULD_TYPES = {CLS.CylinderReport.MOULD_OPTIONS}")
        return mould


    return fMould

def  volume_units_f(units):
    funcName = "volume_units_format() (filter)"
    if(not units):
        return ""

    try:
        fUnits = CLS.CylinderReport.UNITS_OPTIONS[units]

    except:
        print(f"Error: {funcName}: No key matching '{units}' in GB.LOAD_VOLUME_UNITS = {CLS.CylinderReport.UNITS_OPTIONS}")
        return units

    return fUnits


def volume_precision_f(volume):
    funcName = "volume_precision_format() (filter)"

    return volume

def scc_f(str):

    try:
        fStr = CLS.CylinderReport.SCC_OPTIONS[str]

    except:
        return str

    return fStr

def round_val_f(val, precision=0):
    FUNC_NAME = "round_val_f(val, precision=0)"
    if(val == ''):
        return val

    if(not isinstance(precision, int)):
        print(f"Error: {FUNC_NAME}: precision is not an integer. precision = {precision}")
        return val

    try:
        num = Decimal(val)
        # Ensure 0.5 rounds to 1
        rounded_value = num.quantize(Decimal(f"1e-{precision}"), rounding=ROUND_HALF_UP)

        return rounded_value

    except ValueError as e:
        print(f"{e}")
        return val

    except decimal.InvalidOperation as e:
        print(f"{e}")



filters = {
    'strip_date_f': strip_date_f,
    'date_created_f': date_created_f,
    'start_date_f': start_date_f,
    'strip_time_f': strip_time_f,
    'short_description_f':short_description_f,
    'project_status_f':project_status_f,
    'strip_seconds_f':strip_seconds_f,
    'mould_f':mould_f,
    'volume_units_f':volume_units_f,
    'volume_precision_f':volume_precision_f,
    'scc_f':scc_f,
    'round_val_f':round_val_f
}
