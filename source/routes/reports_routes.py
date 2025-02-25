from flask import Flask, render_template, request, redirect, url_for, Blueprint

#Define blueprint for projects.py
reports_bp = Blueprint('reports_bp', __name__, url_prefix='/reports')


pageData = {}
pageData['navItemID'] = "reports_menu"


