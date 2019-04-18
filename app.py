from flask import Flask,request, render_template, redirect, url_for,make_response,send_from_directory,send_file
from flask import Response
from flask import jsonify
import urllib.request
import requests
import sys
import json
from fullcontact import FullContact

fc = FullContact('wPKNrAJna1Yv8KOaXroqyaDiYUslX6LB')
APIKey='wPKNrAJna1Yv8KOaXroqyaDiYUslX6LB'
app = Flask(__name__)

#************ Get Contact details By Email *******
@app.route("/conatct_details", methods=['POST','GET'])
def conatct_details():
    if request.method == 'POST':
        jsonData = request.get_json(force=True)
        email1 =jsonData['email']

        if email1 == "" :

            return jsonify({'type': 'validation','message': 'Email is required','status': 0})
            sys.exit()
        if  email1 !="":
                r = fc.person(email=email1)
                return jsonify(r.json())
                sys.exit()
        else:
            return jsonify(userRequired)
            sys.exit()
    return jsonify(status)
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

if __name__=="__main__":

    app.run(host='10.0.0.171',port=8083)

