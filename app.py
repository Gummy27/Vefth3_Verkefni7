from flask import Flask, render_template, session, url_for, request, redirect
from os import urandom
import pymysql
import csv

app = Flask(__name__)
app.secret_key = urandom(24)

def getAccounts():
	password = {
		'password':'Swampert27'}
	connection = pymysql.connect(host='localhost', user='Gudmundur', password=password['password'], db='Vefth', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
	sql = connection.cursor()
	sql.execute('select * from users;')
	accounts = sql.fetchall()
	connection.close()

	return accounts

accounts = getAccounts

@app.route("/", methods=['POST', 'GET'])
def home():
	if request.method == 'POST':
		session['user'] = request.form.get('username')
		session['password'] = request.form.get('password')

		for account in accounts:
			print(session['user'], account['name'])
			print(session['password'], account['password'])
			if account['name'] == session['user'] or account['email'] == session['user']:
				if account['password'] == session['password']:
					return redirect(url_for('signedIn'))
		
	return render_template('innskraning.html')


@app.route("/signedIn")
def signedIn():
	return render_template('accounts.html', accounts=accounts)

@app.route("/new", methods=['POST', 'GET'])
def newSqlUser():
	errors = [False, False]
	if request.method == 'POST':
		session['user'] = request.form.get('username')
		session['password'] = request.form.get('password')
		session['email'] = request.form.get('email')

		for account in accounts:
			if account['name'] == session['user']:
				errors[0] = True

			if account['email'] == session['email']:
				errors[1] = True

		if not errors[0] and not errors[1]:
			connection = pymysql.connect(host='localhost', user='Gudmundur', password=password['password'], db='Vefth', charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
			command = f"insert into users(name, password, email)\nValues('{ session['user'] }', '{ session['password'] }', '{ session['email'] }');"
			sql = connection.cursor()
			sql.execute(command)
			connection.commit()
			connection.close()
			accounts = getAccounts

			return redirect(url_for('home'))

	return render_template('nyskranning.tpl', errors=errors)

if __name__ == '__main__':
	app.run(debug=True)