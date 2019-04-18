import pyodbc
server = 'dbserveranasight.database.windows.net'
database = 'warehouse'
username = 'anasight@dbserveranasight'
password = 'Root@12345'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()


#Select Query
