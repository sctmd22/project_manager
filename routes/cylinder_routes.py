from datetime import datetime
from email.policy import default

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
    for i in range(GB.CYL_NUM_STR_TARGETS):
        str_list.append({"auto_id": -1, "target_strength": "", "target_days": ""})

    conditions_table = GB.CYL_CONDITIONS_TABLE.copy()

    for index, row in enumerate(GB.CYL_CONDITIONS_TABLE):
        conditions_table[index]['data'] = {
            "val_actual":0,
            "val_min":0,
            "val_max":0,
            "notes":""
        }


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
        "isSCC": "no",

        "createdBy": "admin",

        "str_table": str_list,

        "statusData":GB.PROJECT_STATUS,
        "mouldData":GB.MOULD_TYPES,
        "loadVolumeData":GB.LOAD_VOLUME_UNITS,
        "conditionsTableData": conditions_table,
        "sccData":GB.SCC_RADIO

    }

    bcData = {}
    bcData['breadCrumbTitle'] = "Cylinders"

    return render_template("cylinders/view_cylinder.html", data=data, breadcrumb=bcData, editData=editing, newCylinder=newCylinder)


@bp.route("/<int:cylinder_id>")
def view_cylinder(cylinder_id):
    FUNC_NAME = "view_cylinder()"

    editing = False

    get_edit = request.args.get('edit', default='false')

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


    SQL_CYLINDER_CONDITIONS_GET = (f"SELECT * FROM {TB_CONDITIONS} WHERE cyl_report_id = %s ORDER BY auto_id ASC")
    values = (cylinder_id,)
    cursor.execute(SQL_CYLINDER_CONDITIONS_GET, values)

    conditions_result = cursor.fetchall()

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
        "isSCC":result['is_scc'],

        "createdBy":"admin",

        "str_table":str_result,
        "statusData":GB.PROJECT_STATUS,
        "mouldData":GB.MOULD_TYPES,
        "loadVolumeData":GB.LOAD_VOLUME_UNITS,
        "conditionsTableData":conditions_table,
        "sccData":GB.SCC_RADIO


    }


    bcData = {}
    bcData['breadCrumbTitle'] = "Cylinder Report"

    return render_template("cylinders/view_cylinder.html", breadcrumb=bcData, editData = editing, data=data)


@bp.route("/submit", methods=['POST'])
def submit_cylinder():

    fieldData = HLP.get_cyl_field_data()
    strengthData = HLP.get_cyl_str_data()
    measurementData = HLP.get_cyl_conditions_data()

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
        fieldData['cylSCC']
    ]


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
            notes,
            is_scc
      )
      
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """)
             #1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25


    dbCon = DB.db_connect()
    cursor = dbCon.cursor()

    cursor.execute(SQL_CYLINDERS_INSERT, fieldDataList)
    dbCon.commit()

    # Get the auto-increment ID
    id = cursor.lastrowid


    SQL_CYLINDERS_STR_INSERT = (f"""
        INSERT INTO {TB_STR_REQ} 
        (
            cyl_report_id,
            target_strength,
            target_days
        ) 
        VALUES (%s, %s, %s)
        """)


    for row in strengthData:
        cursor.execute(SQL_CYLINDERS_STR_INSERT, (id, row['strength'], row['days']))
        dbCon.commit()


    SQL_CYLINDERS_MEASURE_INSERT = (f"""
           INSERT INTO {TB_CONDITIONS} 
           (
               cyl_report_id,
               property,
               val_actual,
               val_min,
               val_max,
               notes,
               val_actual_precision,
               val_min_precision,
               val_max_precision
           ) 
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
           """)


    for row in measurementData:
        cursor.execute(SQL_CYLINDERS_MEASURE_INSERT, (id, row['property'], row['val_actual'], row['val_min'], row['val_max'], row['notes'], 1, 1, 1))
        dbCon.commit()


    cursor.close()
    dbCon.close()  # return connection to pool

    bcData = {}
    bcData['breadCrumbTitle'] = "Cylinder Report"

    return redirect(url_for("cylinders_bp.view_cylinder", cylinder_id=id))



@bp.route("/update", methods=['POST'])
def update_cylinder():
    fieldData = HLP.get_cyl_field_data()
    strengthData = HLP.get_cyl_str_data()
    measurementData = HLP.get_cyl_conditions_data()

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


    dbCon = DB.db_connect()
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