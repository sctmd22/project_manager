from _datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, Blueprint

import GLOBALS as GB
import helpers as HLP
import db as DB

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

    dbCon = DB.db_connect();
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
    for i in range(HLP.num_str_targets()):
        str_list.append({"auto_id": -1, "target_strength": "", "target_days": ""})

    #numTargets = 1

    data = {
        "id":-1,
        "dateCreated": datetime.today(),
        "title": "Report Title",
        "status": "active",
        "projectName": "",
        "ticketNum": "",
        "supplier": "",
        "loadNum": "",
        "truckNum": "",
        "contractor": "",
        "sampledFrom": "",
        "mixId": "",
        "mouldType": "100x200_plastic",
        "poNum": "",
        "placementType": "",
        "cementType": "",
        "loadVolume": "",
        "loadVolumeUnits": "meters",
        "dateCast": "",
        "batchTime": "",
        "sampleTime": "",
        "castTime": "",
        "dateTransported": "",
        "notes": "",

        "createdBy": "admin",

        "str_table": str_list,

        "statusData":GB.PROJECT_STATUS,
        "mouldData":GB.MOULD_TYPES,
        "loadVolumeData":GB.LOAD_VOLUME_UNITS


    }

    bcData = {}
    bcData['breadCrumbTitle'] = "Cylinders"

    return render_template("cylinders/view_cylinder.html", data=data, breadcrumb=bcData, editData=editing, newCylinder = newCylinder)


@bp.route("/<int:cylinder_id>")
def view_cylinder(cylinder_id):

    get_edit = request.args.get('edit', default=False)

    editing = False

    if(not(get_edit == False)):
        if(get_edit.lower() == 'true'):
            editing = True

    dbCon = DB.db_connect()
    cursor = dbCon.cursor(dictionary=True)

    SQL_CYLINDER_GET = (f"SELECT * FROM {TB_REPORT_DATA} WHERE auto_id = %s")

    #Sending query as a tuple to reduce the risk of SQL injection
    values = (cylinder_id,)
    cursor.execute(SQL_CYLINDER_GET, values)

    result = cursor.fetchone()

    #Get strength table data
    SQL_CYLINDER_STR_GET = (f"SELECT * FROM {TB_STR_REQ} WHERE cyl_report_id = %s")
    values = (cylinder_id,)
    cursor.execute(SQL_CYLINDER_STR_GET, values)

    str_result = cursor.fetchall()

    if(not editing):
        #Looping backwards, drop any entries that are 0 up up until the first entry with nonzero data
        for i in range(len(str_result)-1, 0, -1):
            if(str_result[i]['target_strength'] == 0 and  str_result[i]['target_days'] == 0):
                str_result.pop(i)
            else:
                break


    SQL_CYLINDER_CONDITIONS_GET = (f"SELECT * FROM {TB_CONDITIONS} WHERE cyl_report_id = %s")
    values = (cylinder_id,)
    cursor.execute(SQL_CYLINDER_CONDITIONS_GET, values)



    conditions_result = cursor.fetchall()

    print(conditions_result)


    conditions_table = GB.CYL_CONDITIONS_TABLE.copy()
    #Build conditions table. Match database results to stored conditions table
    for i, conditions in enumerate(conditions_table):


        for j, conditions_row in enumerate(conditions_result):
            if(conditions['property'] == conditions_row['property']):
                conditions_table[i]['data'] = conditions_row
                conditions_result.pop(j) #Shorten the list each match to improve speed
                break


    #Prevent HTML errors from None types being in time inputs
    batchTime = HLP.removeNone(result['time_batch'])
    sampleTime = HLP.removeNone(result['time_sample'])
    castTime = HLP.removeNone(result['time_cast'])

    #Get measuerment/conditions table data


    '''
    print(f"batchTime type from batchTime: {type(batchTime)}")
    print(f"loadvolume type from myssql: {type(sampleTime)}")
    print(f"dateCast type from myssql: {type(result['date_cast'])}")
    print(f"dateTransported type from myssql: {type(result['date_transported'])}")
    '''

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
        "loadVolumeUnits":result['load_volume_units'],
        "dateCast":result['date_cast'],
        "batchTime":batchTime,
        "sampleTime":sampleTime,
        "castTime":castTime,
        "dateTransported":result['date_transported'],
        "notes":result['notes'],

        "createdBy":"admin",

        "str_table":str_result,
        "statusData":GB.PROJECT_STATUS,
        "mouldData":GB.MOULD_TYPES,
        "loadVolumeData":GB.LOAD_VOLUME_UNITS,
        "conditionsTableData":conditions_table


    }


    bcData = {}
    bcData['breadCrumbTitle'] = "Cylinder Report"

    return render_template("cylinders/view_cylinder.html", breadcrumb=bcData, editData = editing, data=data)


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
    loadVolumeUnits = request.form['cylVolumeUnits']
    dateCast = request.form['cylCastDate']
    batchTime = request.form['cylBatchTime']
    sampleTime = request.form['cylSampleTime']
    castTime = request.form['cylCastTime']
    dateTransported = request.form['cylDateTransported']
    notes = request.form['cylNotes']



    str_table_strength = request.form.getlist('str_table_strength')
    str_table_days = request.form.getlist('str_table_days')

    #Convert string dates to datetime objects
    dateTransported = HLP.formToDate(dateTransported)
    dateCast = HLP.formToDate(dateCast)

    #Convert string times to datetime objects (MYSQL could handle strings but this is stricter)
    batchTime = HLP.formToTime(batchTime)
    sampleTime = HLP.formToTime(sampleTime)
    castTime = HLP.formToTime(castTime)


    #loadVolume = HLP.strToFloat(loadVolume)

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
        loadVolumeUnits,
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
            load_volume_units,
            date_cast,
            time_batch,
            time_sample,
            time_cast,
            date_transported,
            notes
      )
      
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """)
             #1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19  20  21  22  23  24


    dbCon = DB.db_connect()
    cursor = dbCon.cursor()

    cursor.execute(SQL_CYLINDERS_INSERT, data)
    dbCon.commit()

    # Get the auto-increment ID
    id = cursor.lastrowid

    str_table_data = HLP.create_str_table(str_table_strength, str_table_days, id)

    #print(str_table_data)

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
    loadVolumeUnits = request.form['cylVolumeUnits']
    dateCast = request.form['cylCastDate']
    dateTransported = request.form['cylDateTransported']
    batchTime = request.form['cylBatchTime']
    sampleTime = request.form['cylSampleTime']
    castTime = request.form['cylCastTime']
    notes = request.form['cylNotes']

    str_table_str = request.form.getlist('str_table_strength')
    str_table_days = request.form.getlist('str_table_days')
    str_table_id = request.form.getlist('str_table_id')

    dateTransported = HLP.formToDate(dateTransported)
    dateCast = HLP.formToDate(dateCast)

    batchTime = HLP.formToTime(batchTime)
    sampleTime = HLP.formToTime(sampleTime)
    castTime = HLP.formToTime(castTime)

    #loadVolume = HLP.strToFloat(loadVolume)

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
            load_volume_units = %s,
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
        loadVolumeUnits,
        dateCast,
        batchTime,
        sampleTime,
        castTime,
        notes,
        dateTransported,
        report_id
    )


    dbCon = DB.db_connect()
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

    #print(str_table_data)

    for row in str_table_data:
        #print(f"Row: {row}")
        cursor.execute(SQL_CYL_STR_UPDATE, row)
        dbCon.commit()


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

        dbCon = DB.db_connect()
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