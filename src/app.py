from flask import Flask, render_template, url_for, request, make_response, jsonify
import hashlib
headers = {'Content-Type': 'text/html'}

from db import Database
from load import MockData
from flask_cors import CORS, cross_origin
import json
import datetime
from load import MockData
 
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db = Database()

if db.is_empty('person'):
    MockData.load(db)

POINTS_MULTIPLIERS = {'low':3,'mid':4,'high':5}

@app.route("/signup", methods=['POST'])
def sign_up():
    if request.method == 'POST':
        data = json.loads(request.data)
        try:
            if data['role'] == 'caretaker':
                caretakerId = db.add_caretaker()
                userId = db.add_user_data(data['email'],'123456789',hashlib.md5(data['password'].encode()).hexdigest(),"2023-06-06","2023-06-06")
                db.add_person_caretaker(data['firstName'],data['lastName'],caretakerId,userId)
            elif data['role'] == 'donor':
                donorId = db.add_donor()
                userId = db.add_user_data(data['email'],'123456789',hashlib.md5(data['password'].encode()).hexdigest(),"2023-06-06","2023-06-06")
                db.add_person_donor(data['firstName'],data['lastName'],donorId,userId)
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
            user = db.select_email_passwd(data['email'],hashlib.md5(data['password'].encode()).hexdigest())

            if user == None:
                return make_response(jsonify(message="No user of given data found",success=False),401)
            
            person = db.select_ref_id("person","user_data",user[0])
            role = 'caretaker' if person[6] == None else 'donor'
            return make_response(jsonify(message="POST request accepted",success=True, personId=person[0], role=role),200)
        except Exception as e:
            print(e)
            return make_response(jsonify(message="Error logging in",success=False),401)
    else:
        return make_response(jsonify(message="POST request not returned",success=False),401)    

@app.route("/profile/<personId>", methods=['GET','PUT'])
def profile(personId):
    if request.method == 'GET':
        try:
            person = db.select_id("person",personId)
            user = db.select_id("user_data",person[9])

            userInfo = {'firstName':person[2],'lastName':person[3],'email':user[1],'phoneNumber':user[2]}

            if person[6] == None:
                caretaker = db.select_id("caretaker",person[8])
                # db.update('caretaker',caretaker[0],verified=True)
                userInfo['verified'] = caretaker[1] if caretaker[1] != None else ''
                userInfo['carOwner'] = caretaker[2] if caretaker[2] != None else ''
            else:
                donor = db.select_id("donor",person[6])
                userInfo['donationsSum'] = donor[1] if donor[1] != None else ''
                userInfo['points'] = donor[2] if donor[2] != None else ''

            return make_response(jsonify(userInfo),200)
        except Exception as e:
            print(e)
            return make_response(jsonify(message="Error profile",success=False),401)
    elif request.method == 'PUT':
        data = json.loads(request.data)
        try:
            db.update_selected(data['table'], personId, data['record'], data['content'])

            # todo -> update user, update donor, update caretaker

            return make_response(jsonify(message="PUT request accepted",success=True),200)
        except Exception as e:
            print(e)
            return make_response(jsonify(message="Error edit profile",success=False),401)
    else:
        return make_response(jsonify(message="PUT request not returned",success=False),401)
    
@app.route("/fundraisers", methods=['GET'])
def fundraisers():
    if request.method == 'GET':
        try:
            helpGroups = db.select_n("help_group",100)
            helpGroupsInfo = []
            for group in helpGroups:
                groupInfo = {'groupId':group[0], 'monetaryGoal': group[1],'finishDate': group[2].strftime('%m-%d-%Y'),'povertyLevel':group[3],}

                needsInfo = []
                needs = db.select_all_ref_id("needs","help_group",group[0])
                for _needs in needs:
                    if _needs != None:
                        product = db.select_id("product",_needs[0])
                        if product != None:
                            needsInfo.append( {
                                'product':product[1],
                                'price':product[2],
                                'count':_needs[1]
                            } )
                groupInfo['needs'] = needsInfo
                
                donationsInfo = []
                donationsSum = 0.0
                donations = db.select_all_ref_id("donation","help_group",group[0])
                for donation in donations:
                    if donation != None:
                        donor = db.select_id("donor",donation[4])
                        if donor != None:
                            donorPerson = db.select_ref_id("person","donor",donor[0])
                            if donorPerson != None:
                                donationsSum += round(donation[2],2)
                                donationsInfo.append( {
                                    'date':donation[1].strftime('%m-%d-%Y'),
                                    'amount':donation[2],
                                    'note':donation[3],
                                    'donator': " ".join((donorPerson[2],donorPerson[3]))
                                } )
                groupInfo['donations'] = donationsInfo
                groupInfo['goalPercentage'] = round( 100 * round(donationsSum,2) / round(group[1],2), 2)

                if group[4] != None:
                    caretaker = db.select_id("caretaker",group[4])
                    if caretaker != None:
                        caretakerPerson = db.select_ref_id("person","caretaker",caretaker[0])
                        if caretakerPerson != None:
                            groupInfo['caretaker'] = {
                                'fullName': " ".join((caretakerPerson[2],caretakerPerson[3]))
                            }

                helpGroupsInfo.append( groupInfo )
            return make_response(jsonify(helpGroups = helpGroupsInfo),200)
        except Exception as e:
            print(e)
            return make_response(jsonify(message="Error profile",success=False),401)
    else:
        return make_response(jsonify(message="PUT request not returned",success=False),401)
    
@app.route("/fundraisers/help-group/<groupId>/caretaker/<personId>", methods=['PUT'])
def fundraisers_put(groupId,personId):
    if request.method == 'PUT':
        try:
            person = db.select_id("person",personId)
            caretaker = db.select_id("caretaker",person[8])
            db.update('help_group',groupId,help_group_caretaker_ref_id=caretaker[0])
            return make_response(jsonify(message="PUT request accepted",success=True),200)
        except Exception as e:
            print(e)
            return make_response(jsonify(message="Error taking care",success=False),401)
        
@app.route("/fundraisers/help-group/<groupId>/donor/<personId>", methods=['POST'])
def fundraisers_post(groupId,personId):
    if request.method == 'POST':
        data = json.loads(request.data)
        try:
            person = db.select_id("person",personId)
            donor = db.select_id("donor",person[6])
            donationId = db.add_donation("2023-06-06",float(data['amount']),'')
            group = db.select_id('help_group',groupId)
            db.update('donor',donor[0], donations_sum = float(data['amount']) + donor[1], points=float(data['amount']) * POINTS_MULTIPLIERS[group[3]])
            db.update('donation',donationId,donation_donor_ref_id=donor[0],donation_help_group_ref_id=groupId)

            return make_response(jsonify(message="PUT request accepted",success=True),200)
        except Exception as e:
            print(e)
            return make_response(jsonify(message="Error taking care",success=False),401)

@app.route("/your-help-groups/<personId>", methods=['GET'])
def your_help_groups(personId):
    if request.method == 'GET':
        try:
            person = db.select_id("person",personId)
            caretaker = db.select_id("caretaker",person[8])
            yourHelpGroups = db.select_all_ref_id("help_group","caretaker",caretaker[0])

            helpGroupsInfo = []
            for group in yourHelpGroups:
                groupInfo = {'groupId':group[0], 'monetaryGoal': group[1],'finishDate': group[2].strftime('%m-%d-%Y'),'povertyLevel':group[3],}

                needsInfo = []
                needs = db.select_all_ref_id("needs","help_group",group[0])
                for _needs in needs:
                    if _needs != None:
                        product = db.select_id("product",_needs[0])
                        if product != None:
                            needsInfo.append( {
                                'product':product[1],
                                'price':product[2],
                                'count':_needs[1]
                            } )
                groupInfo['needs'] = needsInfo
                
                donationsInfo = []
                donationsSum = 0.0
                donations = db.select_all_ref_id("donation","help_group",group[0])
                for donation in donations:
                    if donation != None:
                        donor = db.select_id("donor",donation[5])
                        if donor != None:
                            donorPerson = db.select_ref_id("person","donor",donor[0])
                            if donorPerson != None:
                                donationsSum += round(donation[2],2)
                                donationsInfo.append( {
                                    'date':donation[1].strftime('%m-%d-%Y'),
                                    'amount':donation[2],
                                    'note':donation[3],
                                    'donator': " ".join((donorPerson[2],donorPerson[3]))
                                } )
                groupInfo['donations'] = donationsInfo
                groupInfo['goalPercentage'] = round( 100 * round(donationsSum,2) / round(group[1],2), 2)

                if group[4] != None:
                    caretaker = db.select_id("caretaker",group[4])
                    if caretaker != None:
                        caretakerPerson = db.select_ref_id("person","caretaker",caretaker[0])
                        if caretakerPerson != None:
                            groupInfo['caretaker'] = {
                                'fullName': " ".join((caretakerPerson[2],caretakerPerson[3]))
                            }

                helpGroupsInfo.append( groupInfo )
            
            return make_response(jsonify(yourHelpGroups = helpGroupsInfo),200)
        except Exception as e:
            print(e)
            return make_response(jsonify(message="Error profile",success=False),401)
    else:
        return make_response(jsonify(message="PUT request not returned",success=False),401)

@app.route("/your-help-groups/<groupId>", methods=['DELETE'])
def your_help_groups_delete(groupId):
    if request.method == 'DELETE':
        try:
            db.delete_ref_id("person","help_group",groupId)
            db.delete_ref_id("needs","help_group",groupId)
            db.delete_ref_id("donation","help_group",groupId)
            db.delete_id("help_group",groupId)

            return make_response(jsonify(message="DELETE request accepted",success=True),200)
        except Exception as e:
            print(e)
            return make_response(jsonify(message="Error confirming",success=False),401)

if __name__ == "__main__":
    app.run(port=5000,debug=True)
    
