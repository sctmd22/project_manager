from _datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, Blueprint

from helpers import GLB_project_status

from db import db_connect

TB_REPORT_DATA = "cyl_report_data"
TB_STR_REQ = "cyl_str_req"
TB_CYLINDERS = "cyl_items"
TB_CONDITIONS = "cyl_conditions_table"

#Define blueprint for projects.py
bp = Blueprint('cylinders_bp', __name__, url_prefix='/cylinders')



@bp.route("/")
def cylinders():
    bcData = {}
    bcData['breadCrumbTitle'] = "Cylinders"

    dbCon = db_connect();
    cursor = dbCon.cursor(dictionary=True)

    SQL_PROJECT_GET_ALL = (f"SELECT * FROM {TB_REPORT_DATA} ORDER BY date_cast DESC")

    cursor.execute(SQL_PROJECT_GET_ALL)

    result = cursor.fetchall()

    cursor.close()
    dbCon.close()  # return connection to pool

    return render_template("cylinders/cylinders.html", breadcrumb=bcData, data=result)



@bp.route("/new")
def new_cylinder():

    editing = True
    newCylinder = True

    data = {
        "id": -1,
        "status": 0,
        "title":"",
        "date_created":datetime.today(),
        "contractor": "",
        "location": "",
        "description": "",
        "created_by":"admin"
    }

    bcData = {}
    bcData['breadCrumbTitle'] = "Cylinders"

    return render_template("cylinders/view_cylinder.html", data=data, breadcrumb=bcData, editData=editing, statusData = GLB_project_status, newCylinder = newCylinder)


@bp.route("/<int:cylinder_id>")
def view_cylinder(cylinder_id):

    get_edit = request.args.get('edit', default=False)

    editing = False

    if(not(get_edit == False)):
        if(get_edit.lower() == 'true'):
            editing = True

    dbCon = db_connect()
    cursor = dbCon.cursor(dictionary=True)

    SQL_CYLINDER_GET = (f"SELECT * FROM {TB_REPORT_DATA} WHERE auto_id = %s")

    #Sending query as a tuple to reduce the risk of SQL injection
    values = (cylinder_id,)
    cursor.execute(SQL_CYLINDER_GET , values)

    result = cursor.fetchone()

    cursor.close()
    dbCon.close() #return connection to pool

    data = {
        "id": result['auto_id'],
        "dateCreated": result['date_created'],
        "title":result['report_title'],
        "status": result['status'],
        "projectName":result['project_name'],
        "ticketNum":result['ticket_num'],
        "supplier":result['supplier'],
        "loadNum":result['load_num'],
        "truckNum":result['truck_num'],
        "contractor":result['contractor'],
        "sampledFrom":result['sampled_from'],
        "mixId":result['mix_id'],
        "mouldType":result['mould_type'],
        "poNum":result['po_num'],
        "placementType":result['placement_type'],
        "cementType":result['cement_type'],
        "loadVolume":result['load_volume'],
        "dateCast":result['date_cast'],
        "batchTime":result['time_batch'],
        "sampleTime":result['time_sample'],
        "castTime":result['time_cast'],
        "dateTransported":result['date_transported'],
        "notes":result['notes'],


        "createdBy":"admin"

    }



    bcData = {}
    bcData['breadCrumbTitle'] = "Cylinder Report"

    return render_template("cylinders/view_cylinder.html", breadcrumb=bcData, editData = editing, data=data, statusData = GLB_project_status)



@bp.route("/submit", methods=['POST'])
def submit_cylinder():

    # dateCreated = datetime.strptime(rawDateCreated, "%Y-%m-%d %H:%M:%S.%f")
    dateCreated = request.form['dateCreated']
    title = request.form['cylTitle']
    status = request.form['cylStatus']
    createdBy = request.form['createdBy']
    projectName = request.form['cylProject']
    ticketNum = request.form['cylTicket']
    supplier = request.form['cylSupplier']
    loadNum = request.form['cylLoadNum']
    truckNum = request.form['cylTruckNum']
    contractor = request.form['cylContractor']
    sampledFrom = request.form['cylSampled']
    mixId = request.form['cylMix']
    mouldType = request.form['cylMouldType']
    poNum = request.form['cylPONum']
    placementType = request.form['cylPlacement']
    cementType = request.form['cylCement']
    loadVolume = request.form['cylVolume']
    dateCast = request.form['cylCastDate']
    batchTime = request.form['cylBatchTime']
    sampleTime = request.form['cylSampleTime']
    castTime = request.form['cylCastTime']
    #dateTransported = request.form['']
    notes = request.form['cylNotes']

    dateTransported = datetime.today().strftime("%Y-%m-%d")

    if (dateCreated == ""):
        dateCreated = datetime.today().strftime("%Y-%m-%d")

    if(dateCast == ""):
        dateCast = datetime.today().strftime("%Y-%m-%d")

    if(batchTime == ""):
        batchTime = datetime(2020, 5, 17, 0, 0, 0)

    if(sampleTime == ""):
        sampleTime = datetime(2020, 5, 17, 0, 0, 0)

    if(castTime == ""):
        castTime = datetime(2020, 5, 17, 0, 0, 0)

    if(loadVolume == ""):
        loadVolume = 0


    data = (
        dateCreated,
        createdBy,
        title,
        status,
        projectName,
        ticketNum,
        supplier,
        loadNum,
        truckNum,
        contractor,
        sampledFrom,
        mixId,
        mouldType,
        poNum,
        placementType,
        cementType,
        loadVolume,
        dateCast,
        batchTime,
        sampleTime,
        castTime,
        dateTransported,
        notes
    )
    dbCon = db_connect()
    cursor = dbCon.cursor()

    SQL_CYLINDERS_INSERT = (
        f"INSERT INTO {TB_REPORT_DATA} ("
        f"  date_created, "
        f"  created_by, "
        f"  report_title, "
        f"  status, "
        f"  project_name, "
        f"  ticket_num,"
        f"  supplier, "
        f"  load_num, "
        f"  truck_num, "
        f"  contractor, "
        f"  sampled_from, "
        f"  mix_id, "
        f"  mould_type, "
        f"  po_num, "
        f"  placement_type, "
        f"  cement_type, "
        f"  load_volume, "
        f"  date_cast, "
        f"  time_batch, "
        f"  time_sample, "
        f"  time_cast, "
        f"  date_transported, "
        f"  notes"
        f"  ) VALUES "
        f"(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    #       1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19  20  21 22   23

    cursor.execute(SQL_CYLINDERS_INSERT, data)

    dbCon.commit()

    # Get the auto-increment ID
    id = cursor.lastrowid

    cursor.close()
    dbCon.close()  # return connection to pool

    bcData = {}
    bcData['breadCrumbTitle'] = "Cylinder Report"

    return redirect(url_for("cylinders_bp.view_cylinder", cylinder_id=id))



@bp.route("/update", methods=['POST'])
def update_cylinder():
    dateCreated = request.form['dateCreated']
    title = request.form['cylTitle']
    status = request.form['cylStatus']
    createdBy = request.form['createdBy']
    projectName = request.form['cylProject']
    ticketNum = request.form['cylTicket']
    supplier = request.form['cylSupplier']
    loadNum = request.form['cylLoadNum']
    truckNum = request.form['cylTruckNum']
    contractor = request.form['cylContractor']
    sampledFrom = request.form['cylSampled']
    mixId = request.form['cylMix']
    mouldType = request.form['cylMouldType']
    poNum = request.form['cylPONum']
    placementType = request.form['cylPlacement']
    cementType = request.form['cylCement']
    loadVolume = request.form['cylVolume']
    dateCast = request.form['cylCastDate']
    batchTime = request.form['cylBatchTime']
    sampleTime = request.form['cylSampleTime']
    castTime = request.form['cylCastTime']
    # dateTransported = request.form['']
    notes = request.form['cylNotes']

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
    dbCon.close()  # return connection to pool

    bcData = {}
    bcData['breadCrumbTitle'] = "Cylinder Report"

    return redirect("view_cylinder", cylinder_id=id)


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

        dbCon = db_connect()
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