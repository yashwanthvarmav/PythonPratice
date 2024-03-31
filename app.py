from flask import Flask, render_template, request, jsonify
import mysql.connector
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# MySQL Instance configurations
# Change the HOST IP and Password to match your instance configurations
mysql = mysql.connector.connect(user='web', password='webPass', host='127.0.0.1', database='student')

@app.route("/test")  # URL leading to method
def test():  # Name of the method
    return "Hello World!<BR/>THIS IS ANOTHER TEST!"

@app.route("/yest")  # URL leading to method
def yest():  # Name of the method
    return "Hello World!<BR/>THIS IS YET ANOTHER TEST!"

@app.route("/add", methods=['POST'])  # Add Student
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        print(name, email)
        cur = mysql.cursor()  # create a connection to the MySQL instance
        s = '''INSERT INTO students(studentName, email) VALUES('{}','{}');'''.format(name, email)
        cur.execute(s)
        mysql.commit()
        cur.close()
        return jsonify({"Result": "Success"})
    else:
        return render_template('add.html')

@app.route("/")  # Default - Show Data
def hello():
    cur = mysql.cursor()  # create a connection to the MySQL instance
    cur.execute('''SELECT * FROM students''')  # execute an SQL statement
    rv = cur.fetchall()  # Retrieve all rows returned by the SQL statement
    Results = []
    for row in rv:  # Format the Output Results and add to return string
        Result = {}
        Result['Name'] = row[0].replace('\n', ' ')
        Result['Email'] = row[1]
        Result['ID'] = row[2]
        Results.append(Result)
    cur.close()
    response = {'Results': Results, 'count': len(Results)}
    return jsonify(response)

if __name__ == "__main__":
    # Run the Flask app with SSL/TLS encryption
    app.run(host='0.0.0.0', port='8080', ssl_context=('cert.pem', 'privkey.pem'))
