from flask import Flask
from flask import render_template
from flask import request
import mysql.connector
from flask_cors import CORS
import json
mysql = mysql.connector.connect(user='web', password='webPass',
  host='127.0.0.1',
  database='student')

from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})
app = Flask(__name__)
CORS(app)
# My SQL Instance configurations
# Change the HOST IP and Password to match your instance configurations

@app.route("/test")#URL leading to method
def test(): # Name of the method
 return("Hello World!<BR/>THIS IS ANOTHER TEST!") #indent this line

@app.route("/yest")#URL leading to method
def yest(): # Name of the method
 return("Hello World!<BR/>THIS IS YET ANOTHER TEST!") #indent this line

@app.route("/add", methods=['GET', 'POST']) #Add Student
def add():
  if request.method == 'POST':
    name = request.form['name']
    email = request.form['email']
    print(name,email)
    cur = mysql.cursor() #create a connection to the SQL instance
    s='''INSERT INTO students(studentName, email) VALUES('{}','{}');'''.format(name,email)
    app.logger.info(s)
    cur.execute(s)
    mysql.commit()
  else:
    return render_template('add.html')

  return '{"Result":"Success"}'
@app.route("/") #Default - Show Data
def hello(): # Name of the method
  cur = mysql.cursor() #create a connection to the SQL instance
  cur.execute('''SELECT * FROM students''') # execute an SQL statment
  rv = cur.fetchall() #Retreive all rows returend by the SQL statment
  Results=[]
  for row in rv: #Format the Output Results and add to return string
    Result={}
    Result['Name']=row[0].replace('\n',' ')
    Result['Email']=row[1]
    Result['ID']=row[2]
    Results.append(Result)
  response={'Results':Results, 'count':len(Results)}
  ret=app.response_class(
    response=json.dumps(response),
    status=200,
    mimetype='application/json'
  )
  return ret #Return the data in a string format
if __name__ == "__main__":
  app.run(host='0.0.0.0',port='8080') #Run the flask app at port 8080
  app.run(host='0.0.0.0',port='8080', ssl_context=('cert.pem', 'privkey.pem')) #Run the flask app at port 8080

====================================================

Let's try a JS client in the browser

sudo nano /var/www/html/index.html

<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width">
<title>Test API Client</title>
<script>
let doIt=()=>{
  let tab=document.getElementById("tab1");
  let rows=tab1.getElementsByTagName('tr');
  fetch('https://dspaul.dbsprojects.ie:8080/')
    .then(response => response.json())
    .then(data=>data.Results.forEach(  //.slice(0,3)
      x=>{
        let newRow=rows[0].cloneNode(true);
        let divs=newRow.getElementsByTagName('td');
        divs[0].innerHTML=x['ID'];
        divs[1].innerHTML=x['Name'];
        divs[2].innerHTML=x['Email'];
        tab1.appendChild(newRow);
      }
    )
  );
}
</script>
</head>
<body>
<button onClick="doIt()">Press me</button>
This is where the results turn up: <br/>
<table id='tab1' bgcolor='blue'>
<tr><td>ID</td><td>Name</td><td>Email</td></tr>
</table></body>
</html>
