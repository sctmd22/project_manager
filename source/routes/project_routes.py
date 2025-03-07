from datetime import datetime
from flask import render_template, request, redirect, url_for, Blueprint
from db.database import db_connect
import GLOBALS as GB
from helpers.helpers import generateBreadcrumbs

#Define blueprint for projects.py
projects_bp = Blueprint('projects_bp', __name__, url_prefix='/projects')

TB_PROJECTS = "project_master"

pageData = {}
pageData['navItemID'] = "projects_menu"

@projects_bp.route("/")
def projects():
    breadCrumbs = generateBreadcrumbs()

    pageData["pageTitle"] = "Projects"
    pageData["bcTitle"] = pageData["pageTitle"]
    pageData["navLinkID"] = ""

    dbCon = db_connect()
    cursor = dbCon.cursor(dictionary=True)

    SQL_PROJECT_GET_ALL = (f"SELECT * FROM {TB_PROJECTS} ORDER BY date_started DESC")

    cursor.execute(SQL_PROJECT_GET_ALL)
    result = cursor.fetchall()

    cursor.close()
    dbCon.close() #return connection to pool

    return render_template("projects/projects.html", data=result, breadCrumbs=breadCrumbs, pageData=pageData)


@projects_bp.route("/new")
def new_project():
    breadCrumbs = generateBreadcrumbs()

    editing = True
    newProject = True

    #default values
    data = {
        "id": -1,
        "status": 0,
        "date_started": datetime.today(),
        "title":"New Project",
        "date_created":datetime.today(),
        "contractor": "",
        "location": "",
        "description": "",
        "created_by":"admin"
    }

    #return render_template("projects/view_project.html", data=data, breadcrumb=bcData)

    return render_template("projects/view_project.html", data=data, breadCrumbs=breadCrumbs, editData=editing, statusData = GB.PROJECT_STATUS, newProject = newProject)


#Handle new project submission then redirect to the project template page
@projects_bp.route("/new/submit", methods=["POST"])
def submit_project():

    #dateCreated = datetime.strptime(rawDateCreated, "%Y-%m-%d %H:%M:%S.%f")
    dateCreated = request.form['dateCreated']
    createdBy = request.form['createdBy']
    status = request.form['projectStatus']
    title = request.form['projectTitle']
    contractor = request.form['projectContractor']
    location = request.form['projectLocation']
    description = request.form['projectDescription']
    dateStarted = request.form['projectDateStarted']

    if(dateStarted == ""):
        dateStarted = datetime.today().strftime("%Y-%m-%d")

    data = (dateCreated, title, createdBy, contractor, status, description, location, dateStarted)

    dbCon = db_connect()
    cursor = dbCon.cursor()


    SQL_PROJECT_INSERT = (f"INSERT INTO {TB_PROJECTS} (date_created, title, created_by, contractor, status, description, location, date_started) VALUES "
                      f"(%s, %s, %s, %s, %s, %s, %s, %s)")

    cursor.execute(SQL_PROJECT_INSERT, data)

    dbCon.commit()

    # Get the auto-increment ID
    id = cursor.lastrowid

    cursor.close()
    dbCon.close() #return connection to pool


    return redirect(url_for("projects_bp.view_project", project_id=id))


@projects_bp.route("/update", methods=['POST'])
def update_project():
    id = request.form['project_id']
    title = request.form['projectTitle']
    contractor = request.form['projectContractor']
    description = request.form['projectDescription']
    location = request.form['projectLocation']
    dateStarted = request.form['projectDateStarted']
    status = request.form['projectStatus']

    dbCon = db_connect()
    cursor = dbCon.cursor()

    SQL_PROJECT_UPDATE = (
        f"UPDATE {TB_PROJECTS} SET "
            f"title='{title}', "
            f"contractor='{contractor}', "
            f"status='{status}', "
            f"description='{description}', "
            f"location='{location}', "
            f"date_started='{dateStarted}' "
        f"WHERE auto_id = %s")

    values = (id,)
    cursor.execute(SQL_PROJECT_UPDATE, values)
    dbCon.commit()

    cursor.close()
    dbCon.close() #return connection to pool


    return redirect(url_for("projects_bp.view_project", project_id=id))


@projects_bp.route("/<int:project_id>")
def view_project(project_id):
    breadCrumbs = generateBreadcrumbs()
    #Get url parameters
    get_edit = request.args.get('edit', default=False)

    editing = False

    if(not(get_edit == False)):
        if(get_edit.lower() == 'true'):
            editing = True

    dbCon = db_connect()
    cursor = dbCon.cursor(dictionary=True)

    SQL_PROJECT_GET = (f"SELECT * FROM {TB_PROJECTS} WHERE auto_id = %s")

    #Sending query as a tuple to reduce the risk of SQL injection
    values = (project_id,)
    cursor.execute(SQL_PROJECT_GET, values)

    result = cursor.fetchone()

    cursor.close()
    dbCon.close() #return connection to pool


    data = {
        "id":result['auto_id'],
        "title":result['title'],
        "date_started":result['date_started'],
        "date_created":result['date_created'],
        "contractor":result['contractor'],
        "description": result['description'],
        "created_by": result['created_by'],
        "status": result['status'],
        "location": result['location']
    }

    return render_template("projects/view_project.html", data=data, breadCrumbs=breadCrumbs, editData=editing, statusData = GB.PROJECT_STATUS)




@projects_bp.route("/delete/cancel/<int:project_id>")
def cancel_delete(project_id):

    return redirect(url_for("projects_bp.view_project", project_id=project_id))


@projects_bp.route("/delete/<int:project_id>")
def confirm_delete(project_id):

    data = {}
    data['id'] = project_id

    bcData = {}
    bcData['breadCrumbTitle'] = "Delete Project"

    return render_template("projects/delete_project.html", data=data, breadcrumb=bcData)

@projects_bp.route("/delete/submit", methods=["POST"])
def delete_project():
    if request.method == 'POST':

        project_id = request.form['project_id']

        dbCon = db_connect()
        cursor = dbCon.cursor(dictionary=True)

        SQL_PROJECT_GET = (f"DELETE FROM {TB_PROJECTS} WHERE auto_id = %s")

        # Sending query as a tuple to reduce the risk of SQL injection
        values = (project_id,)
        cursor.execute(SQL_PROJECT_GET, values)

        dbCon.commit()

        cursor.close()
        dbCon.close()  # return connection to pool

    return redirect(url_for("projects_bp.projects"))

