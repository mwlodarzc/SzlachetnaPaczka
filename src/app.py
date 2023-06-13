from flask import Flask, render_template, url_for, request, make_response, jsonify
import hashlib
headers = {'Content-Type': 'text/html'}

from db import Database
from load import MockData
from flask_cors import CORS, cross_origin
import json
import datetime
 
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

_db = Database()


if _db.is_empty('person'):
    MockData.load(_db)

# todo 
# email sie powtarza z innym w bazie + ewentualnie telefon
@app.route("/signup", methods=['POST'])
def sign_up():
    if request.method == 'POST':
        data = json.loads(request.data)
        try:
            if data['role'] == 'caretaker':
                caretakerId = _db.add_caretaker_empty()
                userId = _db.add_user_data(data['email'],'123456789',hashlib.md5(data['password'].encode()).hexdigest(),"2023-06-06","2023-06-06")
                _db.add_person_caretaker(data['firstName'],data['lastName'],caretakerId,userId)
            elif data['role'] == 'donor':
                donorId = _db.add_donor(0,0,0)
                userId = _db.add_user_data(data['email'],'123456789',hashlib.md5(data['password'].encode()).hexdigest(),"2023-06-06","2023-06-06")
                _db.add_person_donor(data['firstName'],data['lastName'],donorId,userId)
            else:
                return make_response(jsonify(message="Error adding user",success=False),401)
        except Exception as e:
            print(e)
            return make_response(jsonify(message="Error adding user",success=False),401)
        return make_response(jsonify(message="POST request accepted",success=True),200)
    else:
        return make_response(jsonify(message="POST request not returned",success=False),401)

@app.route("/signin", methods=['POST'])
def sign_in():
    if request.method == 'POST':
        data = json.loads(request.data)
        try:
            user = _db.select_email_passwd(data['email'],hashlib.md5(data['password'].encode()).hexdigest())

            if user == None:
                return make_response(jsonify(message="No user of given data found",success=False),401)
            
            person = _db.select_ref_id("person","user_data",user[0])
            role = 'caretaker' if person[6] == None else 'donor'
            return make_response(jsonify(message="POST request accepted",success=True, personId=person[0], role=role),200)
        except Exception as e:
            return make_response(jsonify(message="Error logging in",success=False),401)
    else:
        return make_response(jsonify(message="POST request not returned",success=False),401)    

@app.route("/profile/<personId>", methods=['GET','PUT'])
def profile(personId):
    if request.method == 'GET':
        try:
            person = _db.select_id("person",personId)
            user = _db.select_id("user_data",person[9])

            userInfo = {'firstName':person[2],'lastName':person[3],'email':user[1],'phoneNumber':user[2]}

            if person[6] == None:
                caretaker = _db.select_id("caretaker",person[8])
                userInfo['donationPlace'] = caretaker[1] if caretaker[1] != None else ''
                userInfo['carOwner'] = caretaker[2] if caretaker[2] != None else ''
                userInfo['activeHoursStart'] = caretaker[3] if caretaker[3] != None else ''
                userInfo['activeHoursEnd'] = caretaker[4] if caretaker[4] != None else ''
            else:
                donor = _db.select_id("donor",person[6])
                userInfo['packCount'] = donor[1] if donor[1] != None else ''
                userInfo['donationsSum'] = donor[2] if donor[2] != None else ''
                userInfo['points'] = donor[3] if donor[3] != None else ''

            return make_response(jsonify(userInfo),200)
        except Exception as e:
            return make_response(jsonify(message="Error profile",success=False),401)
    elif request.method == 'PUT':
        data = json.loads(request.data)
        try:
            _db.update_selected(data['table'], personId, data['record'], data['content'])

            # todo -> update user, update donor, update caretaker

            return make_response(jsonify(xd="xd"),200)
        except Exception as e:
            return make_response(jsonify(message="Error edit profile",success=False),401)
    else:
        return make_response(jsonify(message="PUT request not returned",success=False),401)
    
@app.route("/fundraisers", methods=['GET'])
def fundraisers():
    if request.method == 'GET':
        try:
            helpGroups = _db.select_all("help_group")
            helpGroupsJSON = []
            for group in helpGroups:
                needs = _db.select_id("needs",group[0])
                product = _db.select_id("product",needs[0])

                donation = _db.select_id("donations",group[0])
                donor = _db.select_id("donor",group[0])
                donorPerson = _db.select_ref_id("person","donor",donor[0])
                caretaker = _db.select_id("caretaker",group[2])
                caretakerPerson = _db.select_ref_id("person","caretaker",caretaker[0])

                helpGroupsJSON.append( {
                    'groupId':group[0],
                    'povertyLevel':group[1],
                    'needs': {
                        'product':product[1] if product != None else '',
                        'count':needs[1] if needs != None else ''
                    },
                    'donation': {
                        'date':donation[1].strftime('%m-%d-%Y'),
                        'note':donation[2],
                        'donator': " ".join((donorPerson[2],donorPerson[3]))
                    },
                    'caretaker': {
                        'fullName': " ".join((caretakerPerson[2],caretakerPerson[3])),
                        'activeHoursStart':caretaker[3].strftime('%H:%M:%S'),
                        'activeHoursEnd':caretaker[4].strftime('%H:%M:%S')
                    }
                } )

            return make_response(jsonify(helpGroups = helpGroupsJSON),200)
        except Exception as e:
            print(e)
            return make_response(jsonify(message="Error profile",success=False),401)
    else:
        return make_response(jsonify(message="PUT request not returned",success=False),401)

if __name__ == "__main__":
    app.run(port=5000,debug=True)
    
