from flask import render_template, request, redirect, url_for, Blueprint
from helpers import helpers as HLP
from classes import CylinderReport
import db as db
from helpers.helpers import generateBreadcrumbs

TB_REPORT_DATA = "cyl_report_data"

#Define blueprint for cylinder_routes.py
bp = Blueprint('cylinders_bp', __name__, url_prefix='/cylinders')

pageData = {}
pageData['navItemID'] = "reports_menu"
pageData["navLinkID"] = "cylinders_bp"

@bp.route("/")
def cylinders():
    breadCrumbs = generateBreadcrumbs()

    pageData["pageTitle"] = "Cylinder Reports"
    pageData["bcTitle"] = pageData["pageTitle"]

    dbCon = db.db_connect()
    cursor = dbCon.cursor(dictionary=True)

    SQL_PROJECT_GET_ALL = f"SELECT * FROM {TB_REPORT_DATA} ORDER BY date_created DESC"

    cursor.execute(SQL_PROJECT_GET_ALL)

    result = cursor.fetchall()

    cursor.close()
    dbCon.close()  # return connection to pool

    return render_template("cylinders/cylinders.html", breadCrumbs=breadCrumbs, data=result, pageData=pageData)


@bp.route("/new")
def new_cylinder():
    breadCrumbs = generateBreadcrumbs()

    pageData['editing'] = True
    pageData['newCylinder'] = True
    pageData["pageTitle"] = "New Cylinder Report"
    pageData["bcTitle"] = pageData["pageTitle"]

    #Create the CylinderReport object with defaults
    cylReport = CylinderReport.create_default()

    return render_template("cylinders/view_cylinder.html", data=cylReport.to_dict(), tables=cylReport.tables_to_dict(), breadCrumbs=breadCrumbs, pageData=pageData)

@bp.route("/<int:cylinder_id>")
def view_cylinder(cylinder_id):
    breadCrumbs = generateBreadcrumbs()

    # Check the GET request to see if 'edit' is set
    editing = HLP.get_edit()

    pageData["pageTitle"] = "Cylinder Report"
    pageData["bcTitle"] = pageData["pageTitle"]
    pageData["editing"] = editing


    #Create the CylinderReport object loading the data from the database
    cylReport = CylinderReport.create_from_db(cylinder_id, editing)

    return render_template("cylinders/view_cylinder.html", data=cylReport.to_dict(), tables = cylReport.tables_to_dict(), breadCrumbs=breadCrumbs, pageData=pageData)


@bp.route("/submit", methods=['POST'])
def submit_cylinder():

    #Create the CylinderReport object with defaults
    cylReport = CylinderReport.create_default()

    print(f"Debugging? submit_cylinder(): cylReport.id = {cylReport.id}")

    cylReport.submit_form()

    return redirect(url_for("cylinders_bp.view_cylinder", cylinder_id=cylReport.id))



@bp.route("/update", methods=['POST'])
def update_cylinder():
    cylinder_id = request.form['cylinderID']

    cylReport = CylinderReport.create_from_db(cylinder_id, True)    #Set editing to True so the strength table creates the full table before submission

    cylReport.submit_edit()

    return redirect(url_for("cylinders_bp.view_cylinder", cylinder_id=cylinder_id))

@bp.route("/<int:cylinder_id>/delete")
def confirm_delete(cylinder_id):
    breadCrumbs = generateBreadcrumbs()

    pageData["pageTitle"] = "Delete Cylinder Report"
    pageData["bcTitle"] = pageData["pageTitle"]

    data = {}
    data['id'] = cylinder_id #Need to pass the id to a hidden input so the actual delete function can read it back

    return render_template("cylinders/delete_cylinder.html", data=data, breadCrumbs=breadCrumbs, pageData=pageData)


@bp.route("/delete/submit", methods=["POST"])
def delete_cylinder():
    cylinder_id = request.form['cylinder_id']

    cylReport = CylinderReport.create_from_db(cylinder_id, True)
    cylReport.delete()

    return redirect(url_for("cylinders_bp.cylinders"))


@bp.route("/delete/<int:cylinder_id>/cancel")
def cancel_delete(cylinder_id):

    return redirect(url_for("cylinders_bp.view_cylinder", cylinder_id = cylinder_id))