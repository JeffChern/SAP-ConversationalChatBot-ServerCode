from flask import Flask, request, jsonify 
import json 
import pyhdb

# Using pyhdb to connect with SAP HANA


app = Flask(__name__) 
port = 5000

def query_name(firstName,lastName):
  connection = pyhdb.connect('localhost', 30015, 'YOUR_DB', 'YOUR_PASSWORD')
  cursor = connection.cursor()
  query_name = "SELECT PEOPLE.employee_id, salary, salary_date FROM PEOPLE, SALARY WHERE PEOPLE.employee_id = SALARY.employee_id AND PEOPLE.employee_first_name = '{0}' AND PEOPLE.employee_last_name = '{1}'".format(firstName.capitalize(), lastName.capitalize())
  cursor.execute(query_name)
  obj = cursor.fetchall()
  connection.close()
  return obj

def query_name_date(firstName,lastName,date_month,date_year):
  connection = pyhdb.connect('localhost', 30015, 'YOUR_DB', 'YOUR_PASSWORD')
  cursor = connection.cursor()
  query_name = "SELECT PEOPLE.employee_id, salary, salary_date FROM PEOPLE, SALARY WHERE PEOPLE.employee_id = SALARY.employee_id AND PEOPLE.employee_first_name = '{0}' AND PEOPLE.employee_last_name = '{1}' AND MONTH(salary_date) = '{2}' AND YEAR(salary_date) = '{3}'".format(firstName.capitalize(), lastName.capitalize(),date_month,date_year)
  cursor.execute(query_name)
  obj = cursor.fetchall()
  connection.close()
  return obj  

def query_id_date(id,date_month,date_year):
  connection = pyhdb.connect('localhost', 30015, 'YOUR_DB', 'YOUR_PASSWORD')
  cursor = connection.cursor()
  query_name = "SELECT PEOPLE.employee_first_name, PEOPLE.employee_last_name, salary, salary_date FROM PEOPLE, SALARY WHERE PEOPLE.employee_id = SALARY.employee_id AND PEOPLE.employee_id = '{0}' AND MONTH(salary_date) = '{1}' AND YEAR(salary_date) = '{2}'".format(id,date_month,date_year)
  cursor.execute(query_name)
  obj = cursor.fetchall()
  connection.close()
  return obj  

def query_id(id):
  connection = pyhdb.connect('localhost', 30015, 'YOUR_DB', 'YOUR_PASSWORD')
  cursor = connection.cursor()
  #query_name = "SELECT PEOPLE.employee_id, salary, salary_date FROM PEOPLE, SALARY WHERE PEOPLE.employee_first_name = '{0}' AND PEOPLE.employee_last_name = '{1}'".format(firstName.capitalize(), lastName.capitalize())
  query_id = "SELECT PEOPLE.employee_first_name, PEOPLE.employee_last_name, salary, salary_date FROM PEOPLE, SALARY WHERE PEOPLE.employee_id = SALARY.employee_id AND PEOPLE.employee_id = '{0}'".format(id)  
  #query_id = "SELECT PEOPLE.employee_id, salary, salary_date FROM PEOPLE, SALARY WHERE PEOPLE.employee_id = SALARY.employee_id AND PEOPLE.employee_id = '{0}'".format(id)  
  cursor.execute(query_id)
  obj = cursor.fetchall()
  connection.close()
  return obj


@app.route('/get-name', methods=['POST']) 
def get_name(): 
  data = json.loads(request.get_data())
  fullname = data['nlp']['entities']['person'][0]['fullname']
  tmp = fullname.split()
  fName = tmp[0]
  lName = tmp[1]
  res = query_name(fName, lName)
  ans = "ID is {0} \n".format(res[0][0])
  for k in range(0, len(res)):
    s = res[k][1]
    d = res[k][2]
    ans += "month salary of payment date {0} is {1} \n".format(d, s) 

  return jsonify( 
    status=200, 
    replies=[{ 
      "type": "text",
          'content': ans
    }]
  ) 

@app.route('/get-name-date', methods=['POST']) 
def get_name_date(): 
  data = json.loads(request.get_data())
  fullname = data['nlp']['entities']['person'][0]['fullname']
  date = data['nlp']['entities']['datetime'][0]['iso']
  temp = date.split("-")
  date_month = temp[1]
  date_year = temp[0]
  tmp = fullname.split()
  fName = tmp[0]
  lName = tmp[1]
  res = query_name_date(fName, lName,date_month,date_year)
  ans = "ID is {0} \n".format(res[0][0])
  for k in range(0, len(res)):
    s = res[k][1]
    d = res[k][2]
    ans += "month salary of payment date {0} is {1} \n".format(d, s) 

  return jsonify( 
    status=200, 
    replies=[{ 
      "type": "text",
          'content': ans
    }]
  ) 

@app.route('/get-id', methods=['POST']) 
def get_id(): 
  data = json.loads(request.get_data())
  id = data['nlp']['entities']['id'][0]['value']
  res = query_id(id) 
  ans = "Name is {0} {1} \n".format(res[0][0], res[0][1])
  for k in range(0, len(res)):
    s = res[k][2]
    d = res[k][3]
    ans += "month salary of payment date {0} is {1} \n".format(d, s) 

  return jsonify( 
    status=200, 
    replies=[{ 
      "type": "text",
          'content': ans
    }]
  ) 

@app.route('/get-id-date', methods=['POST']) 
def get_id_date(): 
  data = json.loads(request.get_data())
  id = data['nlp']['entities']['id'][0]['value']
  date = data['nlp']['entities']['datetime'][0]['iso']
  temp = date.split("-")
  date_month = temp[1]
  date_year = temp[0]
  res = query_id_date(id,date_month,date_year) 
  ans = "Name is {0} {1} \n".format(res[0][0], res[0][1])
  for k in range(0, len(res)):
    s = res[k][2]
    d = res[k][3]
    ans += "month salary of payment date {0} is {1} \n".format(d, s) 

  return jsonify( 
    status=200, 
    replies=[{ 
      "type": "text",
          'content': ans
    }]
  ) 


@app.route('/errors', methods=['POST']) 
def errors(): 
  print(json.loads(request.get_data())) 
  
  return jsonify( 
    status=200, 
    replies=[{ 
      "type": "text",
          'content': "I can't get any data!"
    }]
  ) 
if __name__ == "__main__": 
  app.run(port=port)
