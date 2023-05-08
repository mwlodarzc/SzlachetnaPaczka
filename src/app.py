from flask import Flask, render_template, url_for
from db import Database

app = Flask(
    __name__,
    static_url_path="",
    template_folder="../templates",
    static_folder="../static",
)

_db = Database()

t = _db.add_user(
    "123456@pwr.edu.pl",
    "123456789",
    "0" * 33,
    "2022-04-29",
    "2022-04-29",
)


p = _db.add_person(
    "81010200141",
    "Łukasz",
    "Brzęczyszczykiewicz",
    "Akacjowa 77 Wrocław",
    "1987-07-01",
)

# print(_db.select_id("user_data", t))
# print(_db.select_id("person", p))
# _db.update("person", p, person_user_data_ref_id=t)
# print(_db.select_id("person", p))


@app.route("/", methods=['GET'])
def index():
    user1 = _db.select_id("person",1)
    return render_template("index.html", user=user1)


if __name__ == "__main__":
    app.run(debug=True)
