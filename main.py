from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify

#Custom file routes
from routes import project_routes, cylinder_routes
import GLOBALS as GB

#Custom flask filters
from filters import filters

app = Flask(__name__)

#Register custom routes as blueprints
app.register_blueprint(project_routes.bp)
app.register_blueprint(cylinder_routes.bp)

#Register custom filters
for name,func in filters.items():
    app.jinja_env.filters[name] = func


@app.route("/test")
def test():

    return render_template("test.html")


@app.route("/test/submit", methods=['POST'])
def test_submit():
    print(request.form)

    return redirect(url_for("test"))


@app.route("/")
def home():

    bcData = {}
    bcData['breadCrumbTitle'] = "Dashboard"

    return render_template("index.html", breadcrumb=bcData)





if __name__ == "__main__":
    app.run(debug=True, port=5000, host='192.168.0.194')

