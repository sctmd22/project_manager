from _datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from datetime import date

import mysql.connector
from mysql.connector import Error

GLB_db_config = {
    "host":"localhost",
    "user":"root",
    "password":"jqHRAK&WCK5iuQ4MP%",
    "database":"project_manager_db"
}


GLB_table_projects = "project_master"

app = Flask(__name__)

GLB_TODAY = datetime.today()

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/projects")
def projects():
    return render_template("projects/projects.html")


@app.route("/projects/new_project")
def new_project():

    #default values
    defaults = {
        "title":"New Project",
        "date":GLB_TODAY.strftime('%Y-%m-%d'),
        "contractor": "",
        "location": "",
        "description": ""
    }

    return render_template("projects/new_project.html", data=defaults)

#Handle new project submission then redirect to the project template page
@app.route("/projects/new_project/submit", methods=["POST"])
def submit_project():

    pCreatedBy = "admin"
    pStatus = 1
    pTitle = request.form['projectTitle']
    pDate = request.form['projectDate']
    pContractor = request.form['projectContractor']
    pLocation = request.form['projectLocation']
    pDescription = request.form['projectDescription']

    dbCon = mysql.connector.connect(**GLB_db_config)

    cursor = dbCon.cursor(dictionary=True)

    SQL_PROJECT_INSERT = (f"INSERT INTO {GLB_table_projects} (date_created, date_project, title, created_by, contractor, status, description) VALUES "
                      f"('{pDate}', '{pDate}', '{pTitle}', '{pCreatedBy}', '{pContractor}', {pStatus}, '{pDescription}')")

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
    dbCon.close()


    return redirect(url_for("view_project", project_id=id))


@app.route("/projects/<int:project_id>")
def view_project(project_id):

    data = {
        'id':project_id
    }

    return render_template("projects/view_project.html", data=data)

@app.route("/projects/edit/<int:project_id>")
def edit_project(project_id):


    return render_template("projects/edit_project.html")

    return redirect(url_for("projects"))


@app.route("/projects/cancel_new_project")
def cancel_project():
    return redirect(url_for("projects"))


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='192.168.0.194')

