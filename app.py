from flask import Flask, render_template, session, url_for, request, redirect, flash
from os import urandom
import pymysql

app = Flask(__name__)
app.secret_key = urandom(24)

def getAccounts():
	password = [
		'Swampert27'
	]
	connection = pymysql.connect(host='localhost', user='Gudmundur', password=password[0], db='Vefth', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
	sql = connection.cursor()
	sql.execute('select * from users;')
	accounts = sql.fetchall()
	connection.close()

	return accounts

@app.route("/", methods=['POST', 'GET'])
def home():
	error = False
	if request.method == 'POST':
		session['user'] = request.form.get('username')
		session['password'] = request.form.get('password')

		for account in getAccounts():
			if account['name'] == session['user'] or account['email'] == session['user']:
				if account['password'] == session['password']:
					flash("Innskráning tókst!")
					return redirect(url_for('signedIn'))
		
		error = True
		
	return render_template('innskraning.html', error=error)


@app.route("/signedIn")
def signedIn():
	return render_template('accounts.html', accounts=getAccounts())

@app.route("/new", methods=['POST', 'GET'])
def newSqlUser():
	errors = [False, False]
	if request.method == 'POST':
		session['user'] = request.form.get('username')
		session['password'] = request.form.get('password')
		session['email'] = request.form.get('email')

		for account in getAccounts():
			if account['name'] == session['user']:
				errors[0] = True

			if account['email'] == session['email']:
				errors[1] = True

		if not errors[0] and not errors[1]:
			password=[
				'Swampert27'
			]
			connection = pymysql.connect(host='localhost', user='Gudmundur', password=password[0], db='Vefth', charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
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