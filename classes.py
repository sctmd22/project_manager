from datetime import datetime
import db as DB


class Reports:
    STATUS_TABLE = {
        'active': "Active",
        'complete': "Complete",
        'deleted': "Deleted",
        'canceled': "Canceled"
    }


class CylinderReport(Reports):
    #Number of cylinder strength targets
    NUM_STR_TARGETS = 5

    TB_REPORT_DATA = "cyl_report_data"
    TB_STR_REQ = "cyl_str_req"
    TB_CYLINDERS = "cyl_items"
    TB_CONDITIONS = "cyl_conditions_table"

    CONDITIONS_SUFFIX = {
        'actual':'Actual',
        'min':'Min',
        'max':'Max',
        'notes':'Notes',
        'id':'ID'
    }

    CONDITIONS_DATA = {
        "val_actual": "",
        "val_min": "",
        "val_max": "",
        "notes": ""
    }

    MOULD_TYPES = {
        "100x200_plastic": "100x200 Plastic",
        "150x300_plastic": "150x300 Plastic",
    }

    LOAD_VOLUME_UNITS = {
        "meters": "m",
        "yards": "yd"
    }

    SCC_RADIO = {
        'no': 'No',
        'yes': 'Yes'
    }

    #Field/measurement data and properties for creation of the HTML table
    CONDITIONS_TABLE = [
        {'title':'Flow (mm)',                           'property':'flow',          'name':'cylConFlow',            'SCC':True, 'CYL': False, 'suffix':CONDITIONS_SUFFIX, 'data':CONDITIONS_DATA},
        {'title':'T<sub>50</sub>(s)',                   'property':'t_50',          'name':'cylConT50',             'SCC':True, 'CYL': False, 'suffix':CONDITIONS_SUFFIX, 'data':CONDITIONS_DATA},
        {'title':'VSI',                                 'property':'vsi',           'name':'cylConVSI',             'SCC':True, 'CYL': False, 'suffix':CONDITIONS_SUFFIX, 'data':CONDITIONS_DATA},
        {'title':'Slump (mm)',                          'property':'slump',         'name':'cylConSlump',           'SCC':False, 'CYL':True, 'suffix':CONDITIONS_SUFFIX, 'data':CONDITIONS_DATA},
        {'title':'Air (%)',                             'property':'air',           'name':'cylConAir',             'SCC':True, 'CYL':True, 'suffix':CONDITIONS_SUFFIX, 'data':CONDITIONS_DATA},
        {'title':'Unit Density (kg/m<sup>3</sup>)',     'property':'density',       'name':'cylConDensity',         'SCC':True, 'CYL': True, 'suffix':CONDITIONS_SUFFIX, 'data':CONDITIONS_DATA},
        {'title':'Sample Temp (&deg;C)',                'property':'sampleTemp',    'name':'cylConSampleTemp',      'SCC':True, 'CYL': True, 'suffix':CONDITIONS_SUFFIX, 'data':CONDITIONS_DATA},
        {'title':'Ambient Temp (&deg;C)',               'property':'ambientTemp',   'name':'cylConAmbientTemp',     'SCC':True, 'CYL': True, 'suffix':CONDITIONS_SUFFIX, 'data':CONDITIONS_DATA},
        {'title':'Initial Curing Conditions (&deg;C)',  'property':'initialTemp',   'name':'cylConInitialTemp',     'SCC':True, 'CYL': True, 'suffix':CONDITIONS_SUFFIX, 'data':CONDITIONS_DATA},
    ]



    #Constructor
    def __init__(self, data):


        self.id = data['id']
        self.date_created = data['dateCreated']
        self.title = data['title']
        self.status = data['status']
        self.project_name = data['projectName']
        self.ticket_num = data['ticketNum']
        self.supplier = data['supplier']
        self.load_num = data['loadNum']
        self.truck_num = data['truckNum']
        self.contractor = data['contractor']
        self.sampled_from = data['sampledFrom']
        self.mix_ID = data['mixId']
        self.mould_type = data['mouldType']
        self.po_num = data['poNum']
        self.placement_type = data['placementType']
        self.cement_type = data['cementType']
        self.load_volume = data['loadVolume']
        self.load_volume_units = data['loadVolumeUnits']
        self.date_cast = data['dateCast']
        self.batch_time = data['batchTime']
        self.sample_time = data['sampleTime']
        self.cast_time = data['castTime']
        self.date_transported = data['dateTransported']
        self.notes = data['notes']
        self.is_scc = data['isSCC']
        self.created_by = data['createdBy']

        self.strength_table = data['str_table']
        self.conditions_table = data['conditionsTableData']


    #Create a new cylinder report with default values
    @classmethod
    def create_default(cls):
        id = -1
        str_list = cls.__create_str_table(id)

        defaultData = {
            "id": id,
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
            "mouldType": list(cls.MOULD_TYPES.keys())[0],   #Get keys from dict, convert to list, get 0th item
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
            "conditionsTableData": cls.CONDITIONS_TABLE
        }

        #Call the CylinderReport constructor to create a class instance with the default data
        return cls(defaultData)



    @classmethod
    def create_from_db(cls, id, editing):

        #Get database values
        report_result = cls.__sql_fetchone(f"SELECT * FROM {cls.TB_REPORT_DATA} WHERE auto_id = %s", (id,)) #The (id,) is a tuple of values which corresponds to %s
        str_result = cls.__sql_fetchall(f"SELECT * FROM {cls.TB_STR_REQ} WHERE cyl_report_id = %s ORDER BY auto_id ASC", (id,))
        con_result = cls.__sql_fetchall(f"SELECT * FROM {cls.TB_CONDITIONS} WHERE cyl_report_id = %s ORDER BY auto_id ASC", (id,))

        if (not editing):
            # Looping backwards, drop any entries that are 0 up up until the first entry with nonzero data
            for i in range(len(str_result) - 1, 0, -1):
                if (str_result[i]['target_strength'] == 0 and str_result[i]['target_days'] == 0):
                    str_result.pop(i)
                else:
                    break



        conditions_table = cls.CONDITIONS_TABLE.copy()
        # Build conditions table. Match database results to stored conditions table
        for i, conditions in enumerate(conditions_table):
            for j, conditions_row in enumerate(con_result):
                if (conditions['property'] == conditions_row['property']):
                    conditions_table[i]['data'] = conditions_row
                    con_result.pop(j)  # Shorten the list each match to improve speed
                    break


        # Prevent HTML errors from None types being in time inputs
        batchTime = cls.__remove_none(report_result['time_batch'])
        sampleTime = cls.__remove_none(report_result['time_sample'])
        castTime = cls.__remove_none(report_result['time_cast'])

        data = {
            "id": report_result['auto_id'],
            "dateCreated": report_result['date_created'],
            "title": report_result['report_title'],
            "status": report_result['status'],
            "projectName": report_result['project_name'],
            "ticketNum": report_result['ticket_num'],
            "supplier": report_result['supplier'],
            "loadNum": report_result['load_num'],
            "truckNum": report_result['truck_num'],
            "contractor": report_result['contractor'],
            "sampledFrom": report_result['sampled_from'],
            "mixId": report_result['mix_id'],
            "mouldType": report_result['mould_type'],
            "poNum": report_result['po_num'],
            "placementType": report_result['placement_type'],
            "cementType": report_result['cement_type'],
            "loadVolume": report_result['load_volume'],
            "loadVolumeUnits": report_result['load_volume_units'],
            "dateCast": report_result['date_cast'],
            "batchTime": batchTime,
            "sampleTime": sampleTime,
            "castTime": castTime,
            "dateTransported": report_result['date_transported'],
            "notes": report_result['notes'],
            "isSCC": report_result['is_scc'],

            "createdBy": "admin",

            "str_table": str_result,
            "conditionsTableData": cls.CONDITIONS_TABLE



        }

        return cls(data)


    #Create the strength table using the class specified number of strength targets and id
    @classmethod
    def __create_str_table(cls, id):
        str_list = []
        for i in range(cls.NUM_STR_TARGETS):
            str_list.append({"auto_id": id, "target_strength": "", "target_days": ""})

        return str_list


    @classmethod
    def __sql_fetchone(cls, query, values=None):
        FUNC_NAME = "__sql_fetchone()"
        try:
            dbCon = DB.db_connect()
            cursor = dbCon.cursor(dictionary=True)

            if (values):
                cursor.execute(query, values)
            else:
                cursor.execute(query)

            result = cursor.fetchone()

            cursor.close()
            dbCon.close()  # return connection to pool

            return result

        except:
            print(f"Error: {FUNC_NAME}: Could not process provided query and or values")
            return None


    @classmethod
    def __sql_fetchall(cls, query, values=None):
        FUNC_NAME = "__sql_fetchall()"
        try:
            dbCon = DB.db_connect()
            cursor = dbCon.cursor(dictionary=True)

            if (values):
                cursor.execute(query, values)
            else:
                cursor.execute(query)

            result = cursor.fetchall()

            cursor.close()
            dbCon.close()  # return connection to pool

            return result

        except:
            print(f"Error: {FUNC_NAME}: Could not process provided query and or values")
            return None

    #Return a blank string if val is False/None
    @classmethod
    def __remove_none(cls, val):
        if(not val):
            return ""

        return val




    #Convert object dict for jinja
    def to_dict(self):
        objectData = {
            "id": self.id,
            "dateCreated": self.date_created,
            "title": self.title,
            "status": self.status,
            "projectName": self.project_name,
            "ticketNum": self.ticket_num,
            "supplier": self.supplier,
            "loadNum": self.load_num,
            "truckNum": self.truck_num,
            "contractor": self.contractor,
            "sampledFrom": self.sampled_from,
            "mixId": self.mix_ID,
            "mouldType": self.mould_type,
            "poNum": self.po_num,
            "placementType": self.placement_type,
            "cementType": self.cement_type,
            "loadVolume": self.load_volume,
            "loadVolumeUnits": self.load_volume_units,
            "dateCast": self.date_cast,
            "batchTime": self.batch_time,
            "sampleTime": self.sample_time,
            "castTime": self.cast_time,
            "dateTransported": self.date_transported,
            "notes": self.notes,
            "isSCC": self.is_scc,
            "createdBy": self.created_by,

            "str_table": self.strength_table,
            "conditionsTableData": self.conditions_table
        }

        return objectData

    #Return data tables as dicts
    def tables_to_dict(self):
        dataTables = {
            "loadVolumeData": self.LOAD_VOLUME_UNITS,
            "mouldData": self.MOULD_TYPES,
            "sccData": self.SCC_RADIO,
            "statusData": self.STATUS_TABLE,
            "conTable":self.CONDITIONS_TABLE
        }

        return dataTables


