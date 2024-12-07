from datetime import datetime

from GLOBALS import HTML_TIME_FORMAT
from flask import Flask, render_template, request, redirect, url_for

#Custom file routes
from routes import project_routes, cylinder_routes
import GLOBALS as GB

app = Flask(__name__)

#Register custom routes as blueprints
app.register_blueprint(project_routes.bp)
app.register_blueprint(cylinder_routes.bp)

@app.template_filter('strip_date')
def strip_date_filter(date):
    if(date == None):
        return ""

    try:
        newDate = date.strftime('%I:%M')

    except:
        return date

    return newDate

@app.template_filter('date_created_format')
def date_created_format(date):
    """Custom Jinja filter to format start_dates in project reports"""

    try:
        newDate = date.strftime('%B %d, %Y - %I:%M:%S %p')

    except:
        return date

    return newDate


@app.template_filter('start_date_format')
def strip_time_filter(date):
    """Custom Jinja filter to format start_dates in project reports"""

    try:
        newDate = date.strftime('%B %d, %Y (%Y-%m-%d)')

    except:
        return date

    return newDate

@app.template_filter('strip_time')
def strip_time_filter(date):
    """Custom Jinja filter to strip time from a datetime."""
    if(date == None):
        return ""

    try:
        timeless = date.strftime('%Y-%m-%d')

    except:
        return date

    return timeless

@app.template_filter('short_description')
def short_description(description):
    charLimit = 50

    if(description == ""):
        return ""

    return description[0:charLimit] + "..."


@app.template_filter('project_status')
def project_status(status):
    '''Convert status into to text'''
    try:
        statusText = GB.PROJECT_STATUS[status]

    except:
        return status

    return statusText

@app.template_filter('strip_seconds')
def strip_seconds(inputTime):

    strTime = str(inputTime)

    lenTime = len(strTime)

    if(lenTime == 8):
        return strTime[:5]

    return ""



@app.template_filter('mould_format')
def mould_format(mould):
    if(not mould):
        return ""

    return GB.MOULD_TYPES[mould]



@app.route("/")
def home():

    bcData = {}
    bcData['breadCrumbTitle'] = "Dashboard"

    return render_template("index.html", breadcrumb=bcData)



if __name__ == "__main__":
    app.run(debug=True, port=5000, host='192.168.0.194')

