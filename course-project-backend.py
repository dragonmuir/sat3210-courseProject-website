from flask import Flask, request, jsonify
from flask_cors import CORS
import pyodbc

app = Flask(__name__)

#Allows HTML front end to call APIs

CORS(app)

#Configuration of MySQL connection

#SQL code for databases goes here (before db_config, after CORS(app))

#Configuration

conn = pyodbc.connect (
    driver= '{SQL Server}',
    server = '10.255.254.2\\SQLEXPRESS',
    database = 'IMS',
    UID = 'camdan',
    PWD = 'P@ssw0rd',
    TrustServerCertificate='yes',

)

#queries SQL database

def show_vendors(conn, query, t):
    cursor = conn.cursor()
    cursor.execute(query,(t))
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    data = []
    for row in rows:
        data.append(dict(zip(columns, row))) 
    
    return data
#selects what column to search for depending on the table
def get_column(tt):
    if (tt == "Client"):
        return "Client_ID"
    if (tt == "Device"):
        return "Device_ID"
    if (tt == "Employee"):
        return "Employee_ID"
    if (tt == "Location"):
        return "Location_ID"
    if (tt == "Software"):
        return "Software_ID"
    if (tt == "Software_Installed"):
        return "Device_ID"
    if (tt == "Vendor"):
        return "Vendor_ID"


#Runs SQL query and returns JSON data to the browser
#cursor.execute("SELECT * FROM instructor WHERE name = ?", (name))
@app.route('/search', methods=['GET'])
def search():

    #gets the thing being searched
    term = request.args.get('q', '')
    tempString = term
    tempString = tempString.split()

    #selects the table name
    tableTerm = tempString[-3]

    #Selects what the limit should be
    limitTerm = tempString[-1]

    #Selects whether exact or contains
    eORcTerm = tempString[-2]

    #removes the table name from the search query
    term = term.split(" ")[:-3]

    tableTerm = str(tableTerm)

    #removes chars from start and end because it was part of a list before
    term = str(term)
    term = term[:-2]
    term = term[2:]


    columnTerm = get_column(tableTerm)

    print(term)
    print(tableTerm)
    print(eORcTerm)
    print(limitTerm)
    print(columnTerm)
    
    #if exact or contains
    if (eORcTerm == "True"):
        term = "%" + term + "%"
        like = " like "
    else:
        like = ""
        term = term
    
    #make sure limit postive or set to positive
    if (int(limitTerm) <=-1):
        limitTerm = " "
    else: 
        limitTerm = " TOP " + limitTerm + " "

    queryString = "SELECT" + limitTerm + "* FROM " + tableTerm + " where " + columnTerm + " LIKE  ?"
    results = show_vendors(conn, queryString, term)
    print(queryString + term)
    return jsonify(results)

#Runs Flask server

if __name__ == '__main__':
    app.run(debug=True)

