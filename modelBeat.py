import sqlite3 as sql
# Get all beats in database
def get_all_beats():
	with sql.connect("database.db") as db:
		c = db.cursor()
		try:
			c.execute("SELECT beat, beatmaker, genre, ambiance, release, duration, bpm, price, mark FROM beats;")
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res = c.fetchall()
		tab = []
		for current in res:
			if current not in tab:
				tab.append(current)
		return tab

# Get name of all beatmakers in database
def get_all_beatmaker():
	with sql.connect("database.db") as db:
		c = db.cursor()
		try:
			c.execute("SELECT beatmaker FROM beats;")
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res = c.fetchall()
		tab = []
		for current in res:
			if current not in tab:
				tab.append(current)
		return tab

# Genre
def get_beats_by_genre(genre):
	with sql.connect("database.db") as db:
		c = db.cursor()
		try:
			c.execute("SELECT beat, beatmaker, genre, ambiance, release, duration, bpm, price FROM beats WHERE genre LIKE '%"+genre+"%';")
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res = c.fetchall()
		return res

def get_beat_for_genre(genre, beat):
	with sql.connect("database.db") as db:
		c = db.cursor()
		try:
			c.execute("SELECT beatmaker, ambiance, release, duration, bpm, price, link, mark FROM beats WHERE genre LIKE '%"+genre+"%' AND beat LIKE '%"+beat+"%';")
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res = c.fetchall()
		return res

# Beatmaker
def get_beat_by_beatmaker(beatmaker):
	with sql.connect("database.db") as db:
		c = db.cursor()
		try:
			c.execute("SELECT beat, beatmaker, genre, ambiance, release, duration, bpm, price FROM beats WHERE beatmaker LIKE '%"+beatmaker+"%';")
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res = c.fetchall()
		return res

def get_beat_for_beatmaker(beatmaker, beat):
	with sql.connect("database.db") as db:
		c = db.cursor()
		try:
			c.execute("SELECT genre, ambiance, release, duration, bpm, price, link, mark FROM beats WHERE beatmaker LIKE '%"+beatmaker+"%' AND beat LIKE '%"+beat+"%';")
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res = c.fetchall()
		return res
