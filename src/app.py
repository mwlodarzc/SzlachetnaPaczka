from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from db import Database
from load import MockData

app = Flask(
    __name__,
    static_url_path="",
    template_folder="../templates",
    static_folder="../static",
)

db = Database()
MockData.load(db)
MockData.show(db)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
