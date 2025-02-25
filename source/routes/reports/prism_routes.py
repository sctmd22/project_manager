from flask import render_template, request, redirect, url_for, Blueprint
from helpers import helpers as HLP
import db as db
from helpers.helpers import generateBreadcrumbs

#Define blueprint for cylinder_routes.py
prisms_bp = Blueprint('prisms_bp', __name__, url_prefix='/reports/prisms')

pageData = {}
pageData['navItemID'] = "reports_menu"
pageData["navLinkID"] = "prisms_bp"

@prisms_bp.route("/")
def prisms():
    breadCrumbs = generateBreadcrumbs()

    pageData["pageTitle"] = "Prism Reports"
    pageData["bcTitle"] = pageData["pageTitle"]

    result = {}


    return render_template("reports/prisms/prisms.html", breadCrumbs=breadCrumbs, data=result, pageData=pageData)

