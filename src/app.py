from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="../templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite'


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
