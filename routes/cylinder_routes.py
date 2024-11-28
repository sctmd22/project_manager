from flask import Flask, render_template, request, redirect, url_for, Blueprint

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

    return render_template("cylinders/cylinders.html", breadcrumb=bcData)


