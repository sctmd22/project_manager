from flask import render_template, request, redirect, url_for, Blueprint
from helpers import helpers as HLP
from classes import CylinderReport
import db as db

TB_REPORT_DATA = "cyl_report_data"
TB_STR_REQ = "cyl_str_req"
TB_CYLINDERS = "cyl_items"
TB_CONDITIONS = "cyl_conditions_table"

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

    cylReport.form_submit()

    bcData = {}
    bcData['breadCrumbTitle'] = "Cylinder Report"

    return redirect(url_for("cylinders_bp.view_cylinder", cylinder_id=cylReport.submitted_id))



@bp.route("/update", methods=['POST'])
def update_cylinder():





    fieldData = HLP.get_cyl_field_data()
    strengthData = HLP.get_cyl_str_data()
    measurementData = HLP.get_cyl_conditions_data(fieldData['cylSCC'])

    for row in measurementData:
        print(row)

    SQL_CYL_REPORT_UPDATE = (f"""
        UPDATE {TB_REPORT_DATA} SET
            date_created = %s, 
            created_by = %s,
            report_title = %s,
            status = %s,
            project_name = %s,
            ticket_num = %s,
            supplier = %s,
            load_num = %s,
            truck_num = %s,
            contractor = %s,
            sampled_from = %s,
            mix_id = %s,
            mould_type = %s,
            po_num = %s,
            placement_type = %s,
            cement_type = %s,
            load_volume = %s,
            load_volume_units = %s,
            date_cast = %s,
            time_batch = %s,
            time_sample = %s,
            time_cast = %s,
            date_transported = %s,
            notes = %s,
            is_scc = %s

        WHERE auto_id = %s
        """)


    fieldDataList = [
        fieldData['dateCreated'],
        fieldData['createdBy'],
        fieldData['cylTitle'],
        fieldData['cylStatus'],
        fieldData['cylProject'],
        fieldData['cylTicket'],
        fieldData['cylSupplier'],
        fieldData['cylLoadNum'],
        fieldData['cylTruckNum'],
        fieldData['cylContractor'],
        fieldData['cylSampled'],
        fieldData['cylMix'],
        fieldData['cylMouldType'],
        fieldData['cylPONum'],
        fieldData['cylPlacement'],
        fieldData['cylCement'],
        fieldData['cylVolume'],
        fieldData['cylVolumeUnits'],
        fieldData['cylCastDate'],
        fieldData['cylBatchTime'],
        fieldData['cylSampleTime'],
        fieldData['cylCastTime'],
        fieldData['cylDateTransported'],
        fieldData['cylNotes'],
        fieldData['cylSCC'],


        fieldData['cylinderID']
    ]


    dbCon = db.db_connect()
    cursor = dbCon.cursor()

    cursor.execute(SQL_CYL_REPORT_UPDATE, fieldDataList)
    dbCon.commit()

    SQL_CYL_STR_UPDATE = (f"""
        UPDATE {TB_STR_REQ} SET 
            target_strength = %s, 
            target_days = %s 
        WHERE auto_id = %s
        """)

    for row in strengthData:
        cursor.execute(SQL_CYL_STR_UPDATE, (row['strength'], row['days'], row['id']))
        dbCon.commit()


    SQL_CYL_CON_UPDATE = (f"""
        UPDATE {TB_CONDITIONS} SET 
            property = %s, 
            val_actual = %s,
            val_min = %s,
            val_max = %s,
            notes = %s,
            val_actual_precision = %s,
            val_min_precision = %s,
            val_max_precision = %s
        WHERE auto_id = %s
        """)


    for row in measurementData:
        cursor.execute(SQL_CYL_CON_UPDATE, (row['property'], row['val_actual'], row['val_min'], row['val_max'], row['notes'], 1, 1, 1, row['auto_id']))
        dbCon.commit()



    dbCon.close()  # return connection to pool

    bcData = {}
    bcData['breadCrumbTitle'] = "Cylinder Report"

    return redirect(url_for("cylinders_bp.view_cylinder", cylinder_id=fieldData['cylinderID']))


@bp.route("/delete/<int:cylinder_id>")
def confirm_delete(cylinder_id):

    data = {}
    data['id'] = cylinder_id

    bcData = {}
    bcData['breadCrumbTitle'] = "Delete Cylinder"

    return render_template("cylinders/delete_cylinder.html", data=data, breadcrumb=bcData)


@bp.route("/delete/submit", methods=["POST"])
def delete_cylinder():
    if request.method == 'POST':

        cylinder_id = request.form['cylinder_id']

        dbCon = db.db_connect()
        cursor = dbCon.cursor(dictionary=True)

        SQL_PROJECT_GET = (f"DELETE FROM {TB_REPORT_DATA} WHERE auto_id = %s")

        # Sending query as a tuple to reduce the risk of SQL injection
        values = (cylinder_id,)
        cursor.execute(SQL_PROJECT_GET, values)

        dbCon.commit()

        cursor.close()
        dbCon.close()  # return connection to pool

    return redirect(url_for("cylinders_bp.cylinders"))


@bp.route("/delete/cancel/<int:cylinder_id>")
def cancel_delete(cylinder_id):

    return redirect(url_for("cylinders_bp.view_cylinder", cylinder_id = cylinder_id))