from flask import render_template, request, redirect, url_for, Blueprint
from helpers import helpers as HLP
from classes import CylinderReport
import db as db

TB_REPORT_DATA = "cyl_report_data"

#Define blueprint for cylinder_routes.py
bp = Blueprint('cylinders_bp', __name__, url_prefix='/cylinders')


@bp.route("/")
def cylinders():
    bcData = {}
    bcData['breadCrumbTitle'] = "Cylinders"

    dbCon = db.db_connect()

    cursor = dbCon.cursor(dictionary=True)

    SQL_PROJECT_GET_ALL = f"SELECT * FROM {TB_REPORT_DATA} ORDER BY date_created DESC"

    cursor.execute(SQL_PROJECT_GET_ALL)

    result = cursor.fetchall()

    cursor.close()
    dbCon.close()  # return connection to pool

    return render_template("cylinders/cylinders.html", breadcrumb=bcData, data=result)



@bp.route("/new")
def new_cylinder():
    editing = True
    newCylinder = True

    #Create the CylinderReport object with defaults
    cylReport = CylinderReport.create_default()

    bcData = {}
    bcData['breadCrumbTitle'] = "Cylinders"

    return render_template("cylinders/view_cylinder.html", data=cylReport.to_dict(), tables=cylReport.tables_to_dict(), breadcrumb=bcData, editData=editing, newCylinder=newCylinder)


@bp.route("/<int:cylinder_id>")
def view_cylinder(cylinder_id):
    FUNC_NAME = "view_cylinder()"

    #Check the GET request to see if 'edit' is set
    editing = HLP.get_edit()

    #Create the CylinderReport object loading the data from the database
    cylReport = CylinderReport.create_from_db(cylinder_id, editing)

    bcData = {}
    bcData['breadCrumbTitle'] = "Cylinder Report"

    return render_template("cylinders/view_cylinder.html", data=cylReport.to_dict(), tables = cylReport.tables_to_dict(), breadcrumb=bcData, editData = editing)


@bp.route("/submit", methods=['POST'])
def submit_cylinder():

    #Create the CylinderReport object with defaults
    cylReport = CylinderReport.create_default()

    cylReport.submit_form()

    bcData = {}
    bcData['breadCrumbTitle'] = "Cylinder Report"

    return redirect(url_for("cylinders_bp.view_cylinder", cylinder_id=cylReport.id))



@bp.route("/update", methods=['POST'])
def update_cylinder():
    cylinder_id = request.form['cylinderID']

    cylReport = CylinderReport.create_from_db(cylinder_id, True)    #Set editing to True so the strength table creates the full table before submission

    cylReport.submit_edit()

    bcData = {}
    bcData['breadCrumbTitle'] = "Cylinder Report"

    return redirect(url_for("cylinders_bp.view_cylinder", cylinder_id=cylinder_id))

@bp.route("/delete/<int:cylinder_id>")
def confirm_delete(cylinder_id):

    data = {}
    data['id'] = cylinder_id #Need to pass the id to a hidden input so the actual delete function can read it back

    bcData = {}
    bcData['breadCrumbTitle'] = "Delete Cylinder"

    return render_template("cylinders/delete_cylinder.html", data=data, breadcrumb=bcData)


@bp.route("/delete/submit", methods=["POST"])
def delete_cylinder():
    cylinder_id = request.form['cylinder_id']

    cylReport = CylinderReport.create_from_db(cylinder_id, True)
    cylReport.delete()

    return redirect(url_for("cylinders_bp.cylinders"))


@bp.route("/delete/cancel/<int:cylinder_id>")
def cancel_delete(cylinder_id):

    return redirect(url_for("cylinders_bp.view_cylinder", cylinder_id = cylinder_id))