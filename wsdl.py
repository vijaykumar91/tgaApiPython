from flask import Flask,request,jsonify
import sys
import time
# import MsSqlConnect
import json
app = Flask(__name__)

from zeep import Client
import zeep
from zeep.wsse.username import UsernameToken

client = Client('https://ws.staging.training.gov.au/Deewr.Tga.WebServices/OrganisationServiceV7.svc?wsdl', wsse=UsernameToken('WebService.Read', 'Asdf098'))

import pyodbc
server = 'dbserveranasight.database.windows.net'
database = 'warehouse'
username = 'anasight@dbserveranasight'
password = 'Root@12345'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

# print ('Reading data from table')
# tsql = "SELECT * FROM jobready_parties;"
# with cursor.execute(tsql):
#     row = cursor.fetchone()
#     print(row)
#Get server Time
@app.route("/getServerTime",methods = ['POST', 'GET'])
def getServerTime():
    if request.method == 'GET':
        return jsonify({'type': 'Get Server Time', 'responseData': client.service.GetServerTime(), 'status': 1})
    else:
        return jsonify({'type': 'request','message': 'Sorry! Method Not Allowed','status': '0'})

#search Result
@app.route("/searchResult", methods=['POST', 'GET'])
def searchResult():
    if request.method == 'GET':
        jsonData = request.get_json(force=True)
        getServerTime=client.service.Search()

        return jsonify({'type': 'search Result', 'responseData': getServerTime, 'status': 1})
    else:
        return jsonify({'type': 'request', 'message': 'Sorry! Method Not Allowed', 'status': '0'})


#Get Address States
@app.route("/GetAddressStates",methods = ['POST', 'GET'])
def GetAddressStates():
    if request.method == 'GET':
        addressStates=[]
        addressStates=client.service.GetAddressStates()
        #Generate QUERY for each dictionary inside data list

        for query in addressStates:
            generate_insert_query('tga_address_states',query,cursor)

        return jsonify({'type': 'Get Address States', 'responseData': str(addressStates), 'status': 1})

    else:
        return jsonify({'type': 'request','message': 'Sorry! Method Not Allowed','status': '0'})


#Get Classification Purposes
@app.route("/GetClassificationPurposes",methods = ['POST', 'GET'])
def GetClassificationPurposes():
    if request.method == 'GET':
        addressStates=[]
        classificationPurposes=client.service.GetClassificationPurposes()
        for query in classificationPurposes:
            generate_insert_query('tga_classification_purposes', query, cursor)

        return jsonify({'type': 'Get Classification Purposes', 'responseData': str(classificationPurposes), 'status': 1})
    else:
        return jsonify({'type': 'request','message': 'Sorry! Method Not Allowed','status': '0'})

#Get Classification Schemes
@app.route("/GetClassificationSchemes",methods = ['POST', 'GET'])
def GetClassificationSchemes():
    if request.method == 'GET':
        addressStates=[]
        classificationSchemes=client.service.GetClassificationSchemes()
        print(classificationSchemes)
        sys.exit()
        return jsonify({'type': 'Get Classification Schemes', 'responseData': str(classificationSchemes), 'status': 1})
    else:
        return jsonify({'type': 'request','message': 'Sorry! Method Not Allowed','status': '0'})

#Get Contact Roles
@app.route("/GetContactRoles",methods = ['POST', 'GET'])
def GetContactRoles():
    if request.method == 'GET':
        addressStates=[]
        contactRoles=client.service.GetContactRoles()

        return jsonify({'type': 'Get Contact Roles', 'responseData': str(contactRoles), 'status': 1})
    else:
        return jsonify({'type': 'request','message': 'Sorry! Method Not Allowed','status': '0'})

#Get Data Managers
@app.route("/GetDataManagers",methods = ['POST', 'GET'])
def GetDataManagers():
    if request.method == 'GET':
        addressStates=[]
        dataManagers=client.service.GetDataManagers()

        for query in dataManagers:
            generate_insert_query('tga_data_managers', query, cursor)

        return jsonify({'type': 'Get Data Managers', 'responseData': str(dataManagers), 'status': 1})
    else:
        return jsonify({'type': 'request','message': 'Sorry! Method Not Allowed','status': '0'})

#Get Details
@app.route("/GetDetails",methods = ['POST', 'GET'])
def GetDetails():
    if request.method == 'GET':
        addressStates=[]
        details=client.service.GetDetails()
        print(details)
        sys.exit()
        for query in dataManagers:
            generate_insert_query('tga_data_managers', query, cursor)

        return jsonify({'type': 'Get Details', 'responseData': str(details), 'status': 1})
    else:
        return jsonify({'type': 'request','message': 'Sorry! Method Not Allowed','status': '0'})

#Get Lookup
@app.route("/GetLookup",methods = ['POST', 'GET'])
def GetLookup():
    if request.method == 'GET':
        addressStates=[]
        lookup=client.service.GetLookup()
        print(lookup)
        sys.exit()
        return jsonify({'type': 'Get Data Managers', 'responseData': str(lookup), 'status': 1})
    else:
        return jsonify({'type': 'request','message': 'Sorry! Method Not Allowed','status': '0'})

#Get Lookup
@app.route("/GetRegistrationManagers",methods = ['POST', 'GET'])
def GetRegistrationManagers():
    if request.method == 'GET':
        addressStates=[]
        registrationManagers=client.service.GetRegistrationManagers()

        for query in registrationManagers:
            generate_insert_query('tga_registration_managers', query, cursor)

        return jsonify({'type': 'Get Registration Managers', 'responseData': str(registrationManagers), 'status': 1})
    else:
        return jsonify({'type': 'request','message': 'Sorry! Method Not Allowed','status': '0'})

#Get Lookup
@app.route("/GetValidationCodes",methods = ['POST', 'GET'])
def GetValidationCodes():
    if request.method == 'GET':
        addressStates=[]
        validationCodes=client.service.GetValidationCodes()

        for query in validationCodes:
            generate_insert_query('tga_validation_codes', query, cursor)

        return jsonify({'type': 'Get Validation Codes', 'responseData': str(validationCodes), 'status': 1})
    else:
        return jsonify({'type': 'request','message': 'Sorry! Method Not Allowed','status': '0'})

#Get Lookup
@app.route("/Search",methods = ['POST', 'GET'])
def Search():
    if request.method == 'GET':
        addressStates=[]
        search=client.service.Search()
        print(search)
        sys.exit()
        return jsonify({'type': 'search', 'responseData': str(search), 'status': 1})
    else:
        return jsonify({'type': 'request','message': 'Sorry! Method Not Allowed','status': '0'})


#Get Lookup
@app.route("/TransferDataManager",methods = ['POST', 'GET'])
def TransferDataManager():
    if request.method == 'GET':
        addressStates=[]
        transferDataManager=client.service.TransferDataManager()

        return jsonify({'type': 'search', 'responseData': str(transferDataManager), 'status': 1})
    else:
        return jsonify({'type': 'request','message': 'Sorry! Method Not Allowed','status': '0'})


def generate_insert_query(table, dictionary, cursor):
    input_dict = zeep.helpers.serialize_object(dictionary)
    output_dict = json.loads(json.dumps(input_dict))

    # Get all "keys" inside "values" key of dictionary (column names)
    columns = ', '.join([key for key, value in output_dict.items()])
    values = ', '.join(["'" + value.replace("'", "") + "'" for key, value in output_dict.items()])


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



app.run(host='10.1.1.210',port='8000',debug=True)