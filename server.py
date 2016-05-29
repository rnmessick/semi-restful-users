from flask import Flask, request, redirect, render_template
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

@app.route("/users/new", methods=["GET"])
def new_user():
  return render_template('new.html')

@app.route("/users/create", methods=["POST"])
def create():
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
  return redirect('/users/<id>')

@app.route('/users/<id>', methods=['POST', 'GET'])
def update(id):
    # Figure out the HTTP verb. If it's a GET, we want to render a page that shows user information.
    if request.method == "GET":
        # Get friend from database
        query = "SELECT id, concat(first_name, ' ', last_name) as name, email, created_at FROM users WHERE id = :id"
        data = { 'id' : id }
        users = mysql.query_db(query, data)
        return render_template('edit.html', users=users)
    # If we're here, it's a POST
    query = "UPDATE users SET first_name = :first_name, last_name = :last_name, email = :email WHERE id = :id"
    data = {
           'first_name': request.form['first_name'],
           'last_name':  request.form['last_name'],
           'email': request.form['email'],
           'id': id
           }
    mysql.query_db(query, data)
    return redirect('/users/'+id)

@app.route('/users/<id>/delete', methods=['POST'])
def destroy(id):
    query = "DELETE FROM users WHERE id = :id"
    data = {'id': id}
    mysql.query_db(query, data)
    return redirect("/users")
  # return render_template('index.html')
app.run(debug=True)