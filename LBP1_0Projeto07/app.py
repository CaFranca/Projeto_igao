from flask import Flask, render_template, Blueprint
from controller.controller import blueprint_default

app = Flask(__name__)
app.register_blueprint(blueprint_default)

@app.route("/", methods=["GET"])
def hello_world():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
