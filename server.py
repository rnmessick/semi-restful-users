from flask import Flask, request, render_template
# import the Connector function
from mysqlconnection import MySQLConnector
app = Flask(__name__)
# connect and store the connection in "mysql" note that you pass the database name to the function
mysql = MySQLConnector(app, 'user_db')

@app.route("/users", methods=["GET"])
def index():
	query = "SELECT id, concat(first_name, ' ', last_name) as name, email, created_at FROM users" # define your query
	users = mysql.query_db(query) # run the query with the query_db method
	return render_template('index.html', users=users) # pass the data to our template

@app.route("/users/new", methods=["POST"])
def new():
# write our query as a string, notice how we have multiple values we want to
# insert into our query
    query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (:first_name, :last_name, :email, NOW(), NOW())"
    # we'll then create a dictionary of data from the POST data received
    data = {
           'first_name': request.form['first_name'],
           'last_name':  request.form['last_name'],
           'email': request.form['email'],
           'created_at': request.form['created_at']
           }
    # run the query with the dictionary values injected into the query
    mysql.query_db(query, data)
    return redirect('/users')

app.run(debug=True)