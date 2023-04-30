from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from db import Database


app = Flask(
    __name__,
    static_url_path="",
    template_folder="../templates",
    static_folder="../static",
)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres@localhost:5432/test"
db = SQLAlchemy(app)

_db = Database()
print(
    t := _db.add_user(
        "123456@pwr.edu.pl",
        "123456789",
        "0" * 33,
        "2022-04-29",
        "2022-04-29",
    )
)
print(_db.select_user(t))


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
