from flask import Flask,request, render_template, redirect, url_for,make_response,send_from_directory,send_file
from flask import Response
from flask import jsonify
import urllib.request
import requests
import sys
import time
from zeep import Client
import zeep
from zeep.wsse.username import UsernameToken

import json
from fullcontact import FullContact


import urllib.request, json


import pyodbc
server = 'dbserveranasight.database.windows.net'
database = 'warehouse'
username = 'anasight@dbserveranasight'
password = 'Root@12345'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()


fc = FullContact('0DHVXQOcAgZzZbUPTeTQ83AakHlzIE8L')
APIKey='0DHVXQOcAgZzZbUPTeTQ83AakHlzIE8L'
app = Flask(__name__)

#************ Get Contact details By Email *******
@app.route("/person_enrich", methods=['POST','GET'])
def person_enrich():
    if request.method == 'POST':
        jsonData = request.get_json(force=True)
        email1 =jsonData['email']
        if email1 == "" :
            return jsonify({'type': 'validation','message': 'Email is required','status': 0})
            sys.exit()

        if  email1 !="":
            headers = {
                'Authorization': 'Bearer '+APIKey,
            }
            params = {
                'email': email1,
            }
            payload = {

                'email': email1,
            }
            url = 'https://api.fullcontact.com/v3/person.enrich'
            response = requests.post(url, headers=headers, params=params,
                                     data=json.dumps(payload))
            response.raise_for_status()
            res=response.json()

            generate_insert_query('fullcontact_person_enrich', res, cursor)
            personalData={
                'fullName':res['fullName'],
                'ageRange': res['ageRange'],
                'gender': res['gender'],
                'location': res['location'],
                'title': res['title'],
                'organization': res['organization'],
                'twitter': res['twitter'],
                'facebook': res['facebook'],
                'avatar': res['avatar'],
                'website': res['website'],
                'updated': res['updated'],
                'bio': res['bio'],
                'linkedin': res['linkedin'],

            }
            dataAddOnsArr=res['dataAddOns']
            detailsArr = res['details']
            return jsonify({'detailsArr':detailsArr,'dataAddOnsArr':dataAddOnsArr,'personalData':personalData})
            sys.exit()



        else:
            return jsonify({'message':'validation Error','status':0})
            sys.exit()
    return jsonify({'error': 'Method are not allowed', 'status': 0})
    sys.exit()
#************ Get Contact details By Email End*******


#************ Get Contact details By Phone *******
@app.route("/phone_details", methods=['POST','GET'])
def phone_details():
    if request.method == 'POST':
        jsonData = request.get_json(force=True)
        phone = jsonData['phone']
        if phone == "" :
            return jsonify({'type': 'validation','message': 'phone is required','status': 0})
            sys.exit()
        if  phone !="":

            url = 'https://api.fullcontact.com/v2/person.json?phone='+str(phone)
            header = {"X-FullContact-APIKey": APIKey}
            r = requests.post(url, headers=header)
            # print(r.json())
            return jsonify(r.json())
            sys.exit()
        else:
            return jsonify({'type': 'server','message': 'Something Went wrong: Internal Server Error','status': 500})
            sys.exit()
    return jsonify({'type': 'Request error','message': 'Method not allowed','status': 401})
#************ Get Contact details By Email End*******




#************ Get Contact details By Phone *******
@app.route("/twitter_details", methods=['POST','GET'])
def twitter_details():
    if request.method == 'POST':
        jsonData = request.get_json(force=True)
        twitter = jsonData['twitter']
        if twitter == "" :
            return jsonify({'type': 'validation','message': 'phone is required','status': 0})
            sys.exit()
        if  twitter !="":
            url = 'https://api.fullcontact.com/v2/person.json?twitter='+str(twitter)
            header = {"X-FullContact-APIKey": APIKey}
            r = requests.post(url, headers=header)
            # print(r.json())
            return jsonify(r.json())
            sys.exit()
        else:
            return jsonify({'type': 'server','message': 'Something Went wrong: Internal Server Error','status': 500})
            sys.exit()
    return jsonify({'type': 'Request error','message': 'Method not allowed','status': 401})
#************ Get Contact details By Email End*******


#************ lookpu by domain *******
@app.route("/company_details", methods=['POST','GET'])
def company_details():
    if request.method == 'POST':
        jsonData = request.get_json(force=True)
        domain = jsonData['domain']
        if domain == "" :
            return jsonify({'type': 'validation','message': 'domain is required','status': 0})
            sys.exit()
        if  domain !="":
            url = 'https://api.fullcontact.com/v2/company/lookup.json?domain='+str(domain)
            header = {"X-FullContact-APIKey": APIKey}
            # data={
            #     'domain':'fullcontact.com'
            # }
            r = requests.get(url,headers=header)
            # print(r.json())
            return jsonify(r.json())
            sys.exit()
        else:
            return jsonify({'type': 'server','message': 'Something Went wrong: Internal Server Error','status': 500})
            sys.exit()
    return jsonify({'type': 'Request error','message': 'Method not allowed','status': 401})
#************ Get Contact details By Email End*******


#************ lookpu by company name *******
@app.route("/company_name", methods=['POST','GET'])
def company_name():
    if request.method == 'POST':
        jsonData = request.get_json(force=True)
        company_name = jsonData['company_name']
        if company_name == "" :
            return jsonify({'type': 'validation','message': 'domain is required','status': 0})
            sys.exit()
        if  company_name !="":
            url = 'https://api.fullcontact.com/v2/company/search.json?companyName=='+str(company_name)
            header = {"X-FullContact-APIKey": APIKey}
            r = requests.get(url,headers=header)
            # print(r.json())
            return jsonify(r.json())
            sys.exit()
        else:
            return jsonify({'type': 'server','message': 'Something Went wrong: Internal Server Error','status': 500})
            sys.exit()
    return jsonify({'type': 'Request error','message': 'Method not allowed','status': 401})
#************ Get Contact details By Email End*******

def generate_insert_query(table, dictionary, cursor):

    input_dict = zeep.helpers.serialize_object(dictionary)
    output_dict = json.loads(json.dumps(input_dict))

    # Get all "keys" inside "values" key of dictionary (column names)
    columns = ', '.join([key for key, value in output_dict.items()])
    values = ', '.join(["'" + json.dumps(value)  if isinstance(value, list) else value.replace("'", "") + "'" for key, value in output_dict.items()])


    queryBuilder = "INSERT INTO " + table + " (" + columns + ") VALUES (" + values + ")"


    retry_flag = True
    retry_count = 0
    while retry_flag and retry_count < 5:
        try:
            result = cursor.execute(queryBuilder)
            cnxn.commit()
            retry_flag = False
        except:
            print
            "Retry after 1 sec"
            retry_count = retry_count + 1
            time.sleep(1)

if __name__=="__main__":

    app.run(host='10.1.1.210', port='8008', debug=True)

