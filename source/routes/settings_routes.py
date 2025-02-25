from flask import render_template, request, redirect, url_for, Blueprint
from helpers.helpers import generateBreadcrumbs

#Define blueprint
settings_bp = Blueprint('settings_bp', __name__, url_prefix='/settings')

pageData = {}
pageData['navItemID'] = "settings_menu"

@settings_bp.route("/user")
def user():
    breadCrumbs = generateBreadcrumbs()

    pageData["navLinkID"] = "settings-user"
    pageData["pageTitle"] = "User Settings"
    pageData["bcTitle"] = pageData["pageTitle"]

    result = {}

    return render_template("settings/user.html", breadCrumbs=breadCrumbs, data=result, pageData=pageData)


@settings_bp.route("/email_lists")
def email_lists():
    breadCrumbs = generateBreadcrumbs()

    pageData["navLinkID"] = "settings-email_lists"
    pageData["pageTitle"] = "Email Lists"
    pageData["bcTitle"] = pageData["pageTitle"]

    result = {}

    return render_template("settings/email_lists.html", breadCrumbs=breadCrumbs, data=result, pageData=pageData)


@settings_bp.route("/reports")
def reports():
    breadCrumbs = generateBreadcrumbs()

    pageData["navLinkID"] = "settings-reports"
    pageData["pageTitle"] = "Report Settings"
    pageData["bcTitle"] = pageData["pageTitle"]

    result = {}

    return render_template("settings/reports.html", breadCrumbs=breadCrumbs, data=result, pageData=pageData)