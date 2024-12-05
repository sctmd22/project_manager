from _datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, Blueprint

from helpers import GLB_project_status, num_str_targets

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

    SQL_PROJECT_GET_ALL = (f"SELECT * FROM {TB_REPORT_DATA} ORDER BY date_created DESC")

    cursor.execute(SQL_PROJECT_GET_ALL)

    result = cursor.fetchall()

    cursor.close()
    dbCon.close()  # return connection to pool

    return render_template("cylinders/cylinders.html", breadcrumb=bcData, data=result)



@bp.route("/new")
def new_cylinder():

    editing = True
    newCylinder = True

    str_list = []
    str_list.append({"target_strength": 0, "target_days": 0})
    numStrTargets = 1


    data = {
        "id":-1,
        "dateCreated": datetime.today(),
        "title": "Report Title",
        "status": 0,
        "projectName": "",
        "ticketNum": "",
        "supplier": "",
        "loadNum": "",
        "truckNum": "",
        "contractor": "",
        "sampledFrom": "",
        "mixId": "",
        "mouldType": "",
        "poNum": "",
        "placementType": "",
        "cementType": "",
        "loadVolume": "",
        "dateCast": "",
        "batchTime": "",
        "sampleTime": "",
        "castTime": "",
        "dateTransported": "",
        "notes": "",

        "createdBy": "admin",

        "numStrTargets": numStrTargets,
        "str_table": str_list


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
    cursor.execute(SQL_CYLINDER_GET, values)

    result = cursor.fetchone()


    SQL_CYLINDER_STR_GET = (f"SELECT * FROM {TB_STR_REQ} WHERE cyl_report_id = %s")
    values = (cylinder_id,)
    cursor.execute(SQL_CYLINDER_STR_GET, values)

    str_result = cursor.fetchall()

    numStrTargets = len(str_result)

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

        "createdBy":"admin",

        "numStrTargets":numStrTargets,
        "str_table":str_result

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
    dateTransported = request.form['cylDateTransported']
    notes = request.form['cylNotes']

    print(request.form)

    str_table_strength = request.form.getlist('str_table_strength')
    str_table_days = request.form.getlist('str_table_days')


    print(str_table_strength)
    print(str_table_days)

    if(dateTransported == ""):
        dateTransported = None

    if(dateCast == ""):
        dateCast = None

    if(batchTime == ""):
        batchTime = None

    if(sampleTime == ""):
        sampleTime = None

    if(castTime == ""):
        castTime = None

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
         # 1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19  20  21  22  23


    dbCon = db_connect()
    cursor = dbCon.cursor()

    cursor.execute(SQL_CYLINDERS_INSERT, data)
    dbCon.commit()

    # Get the auto-increment ID
    id = cursor.lastrowid

    str_targets_len = len(str_table_strength)
    str_cyl_id = [id] * str_targets_len #Create a list of id's which will be the length of (str_table_strength)

    #Zip the data (typles and lists) to create a list of tuples to be added to the mysql database in one query
    str_table_data = list(zip(str_cyl_id, str_table_strength, str_table_days))


    SQL_CYLINDERS_STR_INSERT = (
        f"INSERT INTO {TB_STR_REQ} ("
        f"  cyl_report_id, "
        f"  target_strength, "
        f"  target_days "
        f"  ) VALUES (%s, %s, %s)")


    cursor.executemany(SQL_CYLINDERS_STR_INSERT, str_table_data)
    dbCon.commit()


    cursor.close()
    dbCon.close()  # return connection to pool

    bcData = {}
    bcData['breadCrumbTitle'] = "Cylinder Report"

    return redirect(url_for("cylinders_bp.view_cylinder", cylinder_id=id))



@bp.route("/update", methods=['POST'])
def update_cylinder():
    id = request.form['cylinder_id']

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
    dateTransported = request.form['cylDateTransported']
    batchTime = request.form['cylBatchTime']
    sampleTime = request.form['cylSampleTime']
    castTime = request.form['cylCastTime']
    notes = request.form['cylNotes']

    str_table_str = request.form.getlist('str_table_str')
    str_table_days = request.form.getlist('str_table_days')

    if(dateTransported == ""):
        dateTransported = None

    if(dateCast == ""):
        dateCast = None

    if(batchTime == ""):
        batchTime = None

    if(sampleTime == ""):
        sampleTime = None

    if(castTime == ""):
        castTime = None

    if(loadVolume == ""):
        loadVolume = 0

    SQL_CYL_REPORT_UPDATE = (
        f"UPDATE {TB_REPORT_DATA} SET "
        f"date_created = %s, "
        f"report_title = %s, "
        f"status = %s, "
        f"created_by = %s, "
        f"project_name = %s, "
        f"ticket_num = %s, "
        f"supplier = %s, "
        f"load_num = %s, "
        f"truck_num = %s, "
        f"contractor = %s, "
        f"sampled_from = %s, "
        f"mix_id = %s, "
        f"mould_type = %s, "
        f"po_num = %s, "
        f"placement_type = %s, "
        f"cement_type = %s, "
        f"load_volume = %s, "
        f"date_cast = %s, "
        f"time_batch = %s, "
        f"time_sample = %s, "
        f"time_cast = %s, "
        f"notes = %s, "
        f"date_transported = %s "
        f"WHERE auto_id = %s")


    values = (
        dateCreated,
        title,
        status,
        createdBy,
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
        notes,
        dateTransported,
        id
    )


    dbCon = db_connect()
    cursor = dbCon.cursor()

    cursor.execute(SQL_CYL_REPORT_UPDATE, values)
    dbCon.commit()


    dbCon.close()  # return connection to pool

    bcData = {}
    bcData['breadCrumbTitle'] = "Cylinder Report"

    return redirect(url_for("cylinders_bp.view_cylinder", cylinder_id=id))


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