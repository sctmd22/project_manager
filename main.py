
from flask import Flask, render_template, request, redirect, url_for

#Custom file routes
from routes import project_routes, cylinder_routes

from helpers import GLB_project_status

app = Flask(__name__)

#Register custom routes as blueprints
app.register_blueprint(project_routes.bp)
app.register_blueprint(cylinder_routes.bp)


@app.template_filter('start_date_format')
def strip_time_filter(date):
    """Custom Jinja filter to format start_dates in project reports"""

    try:
        newDate = date.strftime('%B %d, %Y (%Y-%m-%d)')

    except:
        return ""

    return newDate

@app.template_filter('strip_time')
def strip_time_filter(date):
    """Custom Jinja filter to strip time from a datetime."""
    try:
        timeless = date.strftime('%Y-%m-%d')

    except:
        return ""

    return timeless

@app.template_filter('short_description')
def short_description(description):
    charLimit = 50

    if(description == ""):
        return ""

    return description[0:charLimit] + "..."


@app.template_filter('project_status')
def project_status(status):
    try:
        statusText = GLB_project_status[status]

    except:
        return status

    return statusText



@app.route("/")
def home():

    bcData = {}
    bcData['breadCrumbTitle'] = "Dashboard"

    return render_template("index.html", breadcrumb=bcData)

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='192.168.0.194')

