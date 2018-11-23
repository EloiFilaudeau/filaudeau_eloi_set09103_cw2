# import cgi
import re
import sqlite3 as sql
from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Get all beats in database
def get_all_users():
	with sql.connect("users.db") as db:
		c = db.cursor()
		try:
			c.execute("SELECT username, email, password FROM users;")
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res = c.fetchall()
		tab = []
		for current in res:
			if current not in tab:
				tab.append(current)
		return tab

def verify_method(username, email, password, password_verif):
	if username!="" and email!="" and password!="" and password_verif!="":#si tous les attributs sont remplis et valide synthaxiquement parlant
		# flask use own xss protection
		# username = cgi.escape(username, True)
		# email = cgi.escape(email, True)
		# password = cgi.escape(password, True)
		# password_verif = cgi.escape(password_verif, True)
		if re.match(r"[^@\/,{}]+@.+[.].+", email) != None: #regex email
			if password == password_verif:# alors on vérifie que les deux passwords sont egaux
				msg = encrypt_method(username, email, password)
			else:
				msg = "Passwords not equals!"
		else:
			msg = "Email not valid!"
	else:
		msg = "One field is empty!"
	return msg

def encrypt_method(username, email, password):
	# on encrypt le password : salt, hash...
	pw_hash = bcrypt.generate_password_hash(password, 10)
	msg = add_user_method(username, email, pw_hash)
	return msg

def add_user_method(username, email, password):
	with sql.connect("users.db") as db:
		c = db.cursor()
		if get_user_method(username):
			msg = "User already exist!"
		else:
			try:
				c.execute("INSERT INTO users (username, email, password) VALUES ('"+username+"', '"+email+"', '"+password+"');")
				db.commit()
				msg = "User created"
			except sql.DatabaseError as err:
				db.rollback()
				msg = "Error when accessing the database: '{}'".format(err)
		return msg

def decrypt_method(username, password):
	if username!="" and password!="":
		db_pwd = get_user_password_method(username)
		try:
			if bcrypt.check_password_hash(db_pwd, password):
				msg = "success"
			else:
				msg = "Wrong password!"
		except:
			msg = "Inexistent user!"

	else:
		msg = "One field is empty!"
	return msg

def get_user_password_method(username):
	with sql.connect("users.db") as db:
		c = db.cursor()
		if get_user_method(username)==False:
			msg = ""
		else:
			try:
				c.execute("SELECT password FROM users WHERE username LIKE '%"+username+"%';")
			except sql.DatabaseError as err:
				print("Error when accessing the database: '{}'".format(err))
			pwd = c.fetchall()
			msg = pwd[0][0]
		return msg

def get_user_method(username):
	with sql.connect("users.db") as db:
		c = db.cursor()
		try:
			c.execute("SELECT username FROM users WHERE username LIKE '%"+username+"%';")
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		user = c.fetchall()
		if not user:
			msg=False
		else:
			if user[0][0]==username:
				msg=True
			else:
				msg=False
		return msg

def delete_user_method(username):
	with sql.connect("users.db") as db:
		c = db.cursor()
		if get_user_method(username)==False:
			msg = "Inexistent user!"
		else:
			try:
				c.execute("DELETE FROM users WHERE username LIKE '"+username+"';")
				db.commit()
				msg = "User deleted"
			except sql.DatabaseError as err:
				db.rollback()
				msg = "Error when accessing the database: '{}'".format(err)
		return msg

def update_user_method(username, password):
	pw_hash = bcrypt.generate_password_hash(password, 10)
	with sql.connect("users.db") as db:
		c = db.cursor()
		if get_user_method(username)==False:
			msg = "Inexistent user!"
		else:
			try:
				c.execute("UPDATE users SET password = '"+pw_hash+"' WHERE username LIKE '"+username+"';")
				db.commit()
				msg = "Password modify"
			except sql.DatabaseError as err:
				db.rollback()
				msg = "Error when accessing the database: '{}'".format(err)
		return msg

def add_mark_method(beat):
	with sql.connect("database.db") as db:
		c = db.cursor()
		try:
			c.execute("UPDATE beats SET mark = '1' WHERE beat LIKE '"+beat+"';")
			db.commit()
			msg = "Beat added to favorites"
		except sql.DatabaseError as err:
			db.rollback()
			msg = "Error when accessing the database: '{}'".format(err)
		return msg

def del_mark_method(beat):
	with sql.connect("database.db") as db:
		c = db.cursor()
		try:
			c.execute("UPDATE beats SET mark = '0' WHERE beat LIKE '"+beat+"';")
			db.commit()
			msg = "Beat removed from favorites"
		except sql.DatabaseError as err:
			db.rollback()
			msg = "Error when accessing the database: '{}'".format(err)
		return msg

def get_mail_method(username):
	with sql.connect("users.db") as db:
		c = db.cursor()
		try:
			c.execute("SELECT email FROM users WHERE username LIKE '"+username+"';")
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res = c.fetchall()
		res = res[0][0]
		return res

def logout():
	session.pop()
	return home()
