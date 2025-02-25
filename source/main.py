from flask import Flask, render_template, request, redirect, url_for


from routes.project_routes import projects_bp

from routes.reports.cylinder_routes import cylinders_bp
from routes.reports.cube_routes import cubes_bp
from routes.reports.prism_routes import prisms_bp

from routes.settings_routes import settings_bp

#Custom flask filters
from filters import filters
from helpers.helpers import generateBreadcrumbs

app = Flask(__name__)

app.register_blueprint(projects_bp)

app.register_blueprint(cylinders_bp)
app.register_blueprint(cubes_bp)
app.register_blueprint(prisms_bp)

app.register_blueprint(settings_bp)

#Register custom filters
for name,func in filters.items():
    app.jinja_env.filters[name] = func

pageData = {}
pageData['navItemID'] = ""


@app.route("/")
def home():
    breadCrumbs = generateBreadcrumbs()

    pageData["pageTitle"] = "Home"
    pageData["bcTitle"] = pageData["pageTitle"]

    return render_template("index.html", breadCrumbs=breadCrumbs, pageData=pageData)


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='192.168.0.203')

