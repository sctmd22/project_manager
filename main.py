from _datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from datetime import date

import mysql.connector
from mysql.connector import Error, pooling

from enum import Enum

class project_status(Enum):
    Active = 1
    Completed = 2
    Deleted = 3
    Canceled = 4


class Project:

    def __init__(self, title):
        self.title = title



'''
GLB_db_config = {
    "host":"localhost",
    "user":"root",
    "password":"jqHRAK&WCK5iuQ4MP%",
    "database":"project_manager_db"
}
'''

# Create a connection pool at the application level
GLB_connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    host="localhost",
    user="root",
    password="jqHRAK&WCK5iuQ4MP%",
    database="project_manager_db"
)

GLB_table_projects = "project_master"

app = Flask(__name__)

@app.route("/")
def home():

    bcData = {}
    bcData['breadCrumbTitle'] = "Dashboard"

    return render_template("index.html", breadcrumb=bcData)


@app.route("/projects")
def projects():
    dbCon = GLB_connection_pool.get_connection()
    cursor = dbCon.cursor(dictionary=True)

    SQL_PROJECT_GET_ALL = (f"SELECT * FROM {GLB_table_projects} ORDER BY date_created DESC")

    cursor.execute(SQL_PROJECT_GET_ALL)
    result = cursor.fetchall()

    cursor.close()
    dbCon.close() #return connection to pool

    bcData = {}
    bcData['breadCrumbTitle'] = "Projects"

    return render_template("projects/projects.html", data=result, breadcrumb=bcData)


@app.route("/projects/new")
def new_project():

    #default values
    data = {
        "title":"New Project",
        "date":datetime.today().strftime('%Y-%m-%d'),
        "contractor": "",
        "location": "",
        "description": ""
    }

    bcData = {}
    bcData['breadCrumbTitle'] = "Create New Project"

    return render_template("projects/new_project.html", data=data, breadcrumb=bcData)

#Handle new project submission then redirect to the project template page
@app.route("/projects/new/submit", methods=["POST"])
def submit_project():

    createdBy = "admin"
    status = 1
    title = request.form['projectTitle']
    dateCreated = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    contractor = request.form['projectContractor']
    location = request.form['projectLocation']
    description = request.form['projectDescription']

    dbCon = GLB_connection_pool.get_connection()
    cursor = dbCon.cursor(dictionary=True)

    SQL_PROJECT_INSERT = (f"INSERT INTO {GLB_table_projects} (date_created, title, created_by, contractor, status, description, location) VALUES "
                      f"('{dateCreated}', '{title}', '{createdBy}', '{contractor}', {status}, '{description}', '{location}')")

    try:
        cursor.execute(SQL_PROJECT_INSERT)

        dbCon.commit()

    except Error as e:
        print(f"Error: {e}")

    else:
        print(f"SQL Insertion Success")

    # Get the auto-increment ID
    id = cursor.lastrowid

    cursor.close()
    dbCon.close() #return connection to pool


    return redirect(url_for("view_project", project_id=id))


@app.route("/projects/update", methods=['POST'])
def update_project():
    id = request.form['project_id']
    title = request.form['projectTitle']
    contractor = request.form['projectContractor']
    status = 1
    location = request.form['projectLocation']

    dbCon = GLB_connection_pool.get_connection()
    cursor = dbCon.cursor(dictionary=True)

    SQL_PROJECT_UPDATE = (
        f"UPDATE {GLB_table_projects} SET "
            f"title='{title}', "
            f"contractor='{contractor}', "
            f"status='{status}', "
            f"description='{status}', "
            f"location='{location}' "
        f"WHERE auto_id = %s")

    values = (id,)
    cursor.execute(SQL_PROJECT_UPDATE, values)

    cursor.close()
    dbCon.close()


    return redirect(url_for("view_project", project_id=id))


@app.route("/projects/<int:project_id>")
def view_project(project_id):
    #Get url parameters
    get_edit = request.args.get('edit', default=False)

    editing = False

    if(not(get_edit == False)):
        if(get_edit.lower() == 'true'):
            editing = True

    dbCon = GLB_connection_pool.get_connection()
    cursor = dbCon.cursor(dictionary=True)

    SQL_PROJECT_GET = (f"SELECT * FROM {GLB_table_projects} WHERE auto_id = %s")

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

    bcData = {}
    bcData['breadCrumbTitle'] = "View Project"

    return render_template("projects/view_project.html", data=data, breadcrumb=bcData, editData=editing)



@app.route("/projects/new_project/cancel")
def cancel_new_project():
    return redirect(url_for("projects"))


@app.route("/projects/delete/cancel/<int:project_id>")
def cancel_project_delete(project_id):

    return redirect(url_for("view_project", project_id=project_id))


@app.route("/projects/delete/<int:project_id>")
def confirm_project_delete(project_id):

    data = {}


    data['id'] = project_id

    bcData = {}
    bcData['breadCrumbTitle'] = "Delete Project"

    return render_template("projects/delete_project.html", data=data, breadcrumb=bcData)

@app.route("/projects/delete/submit", methods=["POST"])
def delete_project():
    if request.method == 'POST':

        project_id = request.form['project_id']

        dbCon = GLB_connection_pool.get_connection()
        cursor = dbCon.cursor(dictionary=True)

        SQL_PROJECT_GET = (f"DELETE FROM {GLB_table_projects} WHERE auto_id = %s")

        # Sending query as a tuple to reduce the risk of SQL injection
        values = (project_id,)
        cursor.execute(SQL_PROJECT_GET, values)

        dbCon.commit()

        cursor.close()
        dbCon.close()  # return connection to pool

    return redirect(url_for("projects"))


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='192.168.0.194')

