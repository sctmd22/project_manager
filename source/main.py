from flask import Flask, render_template, request, redirect, url_for

#Custom file routes
from routes import project_routes, cylinder_routes, cube_routes

#Custom flask filters
from filters import filters
from helpers.helpers import generateBreadcrumbs

app = Flask(__name__)

#Register custom routes as blueprints
app.register_blueprint(project_routes.bp)
app.register_blueprint(cylinder_routes.bp)
app.register_blueprint(cube_routes.bp)

#Register custom filters
for name,func in filters.items():
    app.jinja_env.filters[name] = func

@app.route("/")
def home():
    breadCrumbs = generateBreadcrumbs()

    return render_template("index.html", breadCrumbs=breadCrumbs)


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='192.168.0.203')

