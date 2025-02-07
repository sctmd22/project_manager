from flask import render_template, request, redirect, url_for, Blueprint
from helpers import helpers as HLP
import db as db
from helpers.helpers import generateBreadcrumbs

TB_REPORT_DATA = "cube_report_data"

#Define blueprint for cylinder_routes.py
bp = Blueprint('cubes_bp', __name__, url_prefix='/cubes')


@bp.route("/")
def cubes():
    breadCrumbs = generateBreadcrumbs()

    result = {}

    '''
    dbCon = db.db_connect()

    cursor = dbCon.cursor(dictionary=True)

    SQL_PROJECT_GET_ALL = f"SELECT * FROM {TB_REPORT_DATA} ORDER BY date_created DESC"

    cursor.execute(SQL_PROJECT_GET_ALL)

    result = cursor.fetchall()

    cursor.close()
    dbCon.close()  # return connection to pool
    '''

    return render_template("cubes/cubes.html", breadCrumbs=breadCrumbs, data=result)

