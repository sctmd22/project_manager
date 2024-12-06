from _datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, Blueprint

from helpers import GLB_project_status, num_str_targets, create_str_table, convertToInt

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
    for i in range(num_str_targets()):
        str_list.append({"auto_id": -1, "target_strength": "", "target_days": ""})

    #numTargets = 1

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

    print(str_result)

    if(not editing):
        #Iterate through the strength table backwards and remove any that meet the criteria
        for i in range(len(str_result)-1, 0, -1):
            if(str_result[i]['target_strength'] == 0 and str_result[i]['target_days'] == 0):
                str_result.pop(i)
                print(str_result)


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
    #str_table_ids = request.form.getlist('str_table_id')


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

    SQL_CYLINDERS_INSERT = (f"""
        INSERT INTO {TB_REPORT_DATA} 
        (
            date_created,
            created_by,
            report_title,
            status,
            project_name,
            ticket_num,
            supplier,
            load_num,
            truck_num,
            contractor,
            sampled_from,
            mix_id,
            mould_type,
            po_num,
            placement_type,
            cement_type,
            load_volume,
            date_cast,
            time_batch,
            time_sample,
            time_cast,
            date_transported,
            notes
      )
      
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """)
               # 1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19  20  21  22  23


    dbCon = db_connect()
    cursor = dbCon.cursor()

    cursor.execute(SQL_CYLINDERS_INSERT, data)
    dbCon.commit()

    # Get the auto-increment ID
    id = cursor.lastrowid

    str_table_data = create_str_table(str_table_strength, str_table_days, id)



    print(str_table_data)

    SQL_CYLINDERS_STR_INSERT = (f"""
        INSERT INTO {TB_STR_REQ} 
        (
            cyl_report_id,
            target_strength,
            target_days
        ) 
        VALUES (%s, %s, %s)
        """)


    cursor.executemany(SQL_CYLINDERS_STR_INSERT, str_table_data)
    dbCon.commit()


    cursor.close()
    dbCon.close()  # return connection to pool

    bcData = {}
    bcData['breadCrumbTitle'] = "Cylinder Report"

    return redirect(url_for("cylinders_bp.view_cylinder", cylinder_id=id))



@bp.route("/update", methods=['POST'])
def update_cylinder():
    report_id = request.form['cylinder_id']

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

    str_table_str = request.form.getlist('str_table_strength')
    str_table_days = request.form.getlist('str_table_days')
    str_table_id = request.form.getlist('str_table_id')

    str_table_str = convertToInt(str_table_str)
    str_table_days = convertToInt(str_table_days)
    str_table_id = convertToInt(str_table_id)

    print(f"str_table_str: {str_table_id}")

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

    SQL_CYL_REPORT_UPDATE = (f"""
        UPDATE {TB_REPORT_DATA} SET
            date_created = %s, 
            report_title = %s,
            status = %s,
            created_by = %s,
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
            date_cast = %s,
            time_batch = %s,
            time_sample = %s,
            time_cast = %s,
            notes = %s,
            date_transported = %s
        WHERE auto_id = %s
        """)


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
        report_id
    )


    dbCon = db_connect()
    cursor = dbCon.cursor()

    cursor.execute(SQL_CYL_REPORT_UPDATE, values)
    dbCon.commit()



    SQL_CYL_STR_UPDATE = (f"""
        UPDATE {TB_STR_REQ} SET 
            target_strength = %s, 
            target_days = %s 
        WHERE auto_id = %s
        """)

    #str_table_data = create_str_table(str_table_str, str_table_days, id)
    str_table_data = list(zip(str_table_str, str_table_days, str_table_id))

    print(str_table_data)

    for row in str_table_data:
        print(f"Row: {row}")
        cursor.execute(SQL_CYL_STR_UPDATE, row)



    dbCon.close()  # return connection to pool

    bcData = {}
    bcData['breadCrumbTitle'] = "Cylinder Report"

    return redirect(url_for("cylinders_bp.view_cylinder", cylinder_id=report_id))


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