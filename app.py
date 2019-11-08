from flask import Flask, render_template, session, url_for, request, redirect
from os import urandom
import pymysql
import csv

password = {
	'password':'Swampert27'}
connection = pymysql.connect(host='localhost', user='Gudmundur', password=password['password'], db='Vefth', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
sql = connection.cursor()
sql.execute('select * from users;')
results = sql.fetchall()
connection.close()

def newSqlUser(name, password, email):
	connection = pymysql.connect(host='localhost',
							user='Gudmundur',
							password=password['password'],
							db='Vefth',
							charset='utf8mb4',
							cursorclass=pymysql.cursors.DictCursor)
	command = f"""insert into users(name, password, email)
				Values({ name }, { password }, { email })"""

	sql.execute(command)
	connection.commit()
	connection.close()

app = Flask(__name__)
app.secret_key = urandom(24)

@app.route("/")
def home():
	render_template('innskraning.html', results)

if __name__ == '__main__':
	app.run(debug=True)