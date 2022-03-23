#!/usr/bin/env python3
import sys
from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import reqparse, Resource, Api
from flask_session import Session
import json
from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import *
import ssl #include ssl libraries

import pymysql.cursors 

import settings # Our server and db settings, stored in settings.py

app = Flask(__name__)
# Set Server-side session config: Save sessions in the local app directory.
app.secret_key = settings.SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = 'peanutButter'
app.config['SESSION_COOKIE_DOMAIN'] = settings.APP_HOST
Session(app)

app.config['MYSQL_HOST'] = settings.MYSQL_HOST
app.config['MYSQL_USER'] = settings.MYSQL_USER
app.config['MYSQL_PASSWORD'] = settings.MYSQL_PASSWD
app.config['MYSQL_DB'] = settings.MYSQL_DB

# Make the connection
mysql = pymysql.connect(host=settings.MYSQL_HOST, 
                                user=settings.MYSQL_USER, 
                                password=settings.MYSQL_PASSWD, 
                                database=settings.MYSQL_DB, 
                                charset='utf8mb4', 
                                cursorclass=pymysql.cursors.DictCursor)

####################################################################################
#
# Error handlers
#
@app.errorhandler(400) # decorators to add to 400 response
def not_found(error):
	return make_response(jsonify( { 'status': 'the fuck is this request' } ), 400)

@app.errorhandler(404) # decorators to add to 404 response
def not_found(error):
	return make_response(jsonify( { 'status': 'Resource not found' } ), 404)

###################################################################################
#
# Routing: GET and POST using Flask-Session
#
 
# @app.route('/login', methods = ['POST', 'GET'])
# def login():#
    
class SignIn(Resource):
	#
	# Set Session and return Cookie
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X POST -d '{"username": "ggura", "password": "123456"}'
	#  	-c cookie-jar -k https://cs3103.cs.unb.ca:31308/signin
	#
	def post(self):    
		if not request.json: # If the requested object is not in json format
			abort(400) # bad request

		# Parse the json, works like lodash
		parser = reqparse.RequestParser()
		try:
 			# Check for required attributes in json document, create a dictionary
			parser.add_argument('username', type=str, required=True)
			parser.add_argument('password', type=str, required=True)
			request_params = parser.parse_args()
		except:
			abort(400) # bad request

		try:
			cursor = mysql.cursor()
			_userName = request_params['username']
			_userPwd = request_params['password']
			param = "CALL loginUser('" +  _userName + "', '" + _userPwd + "')"
			cursor.execute(param)
			mysql.commit()
			user = cursor.fetchall()
			if(len(user) > 0):
				for row in user:
					_userId = str(row['userId'])
				return {'status': 200, 'UserId': _userId}
			else:
				abort(404)
				return {'status': 404, 'message': "Username or Password is incorrect"}
		except:
			abort(400) # bad request

		# if request_params['username'] in session:
		# 	response = {'status': 'success'}
		# 	responseCode = 200
		# else:
		# 	try:
		# 		ldapServer = Server(host=settings.LDAP_HOST)
		# 		ldapConnection = Connection(ldapServer,
		# 			raise_exceptions=True,
		# 			user='uid='+request_params['username']+', ou=People,ou=fcs,o=unb',
		# 			password = request_params['password'])
		# 		ldapConnection.open()
		# 		ldapConnection.start_tls()
		# 		ldapConnection.bind()
		# 		# At this point we have sucessfully authenticated.
		# 		session['username'] = request_params['username']
		# 		response = {'status': 'success' }
		# 		responseCode = 201
		# 	except LDAPException:
		# 		response = {'status': 'Access denied'}
		# 		responseCode = 403
		# 	finally:
		# 		ldapConnection.unbind()

		#return make_response(jsonify(response), responseCode)

	# GET: Check Cookie data with Session data
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X GET -b cookie-jar
	#	-k https://cs3103.cs.unb.ca:61340/signin
	# def get(self):
	# 	success = False
	# 	if 'username' in session:
	# 		username = session['username']
	# 		response = {'status': 'success'}
	# 		responseCode = 200
	# 	else:
	# 		response = {'status': 'fail'}
	# 		responseCode = 403

	# 	return make_response(jsonify(response), responseCode)

	# DELETE: Check Cookie data with Session data (logout?)
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar
	#	-k https://info3103.cs.unb.ca:61340/signin

	#
	#	Here's your chance to shine!
	#


# class GeneralUser
class GeneralUser(Resource):
	# POST: Create a new user
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X POST -d '{"username": "uruharushia", "password": "marine", 
	# "email": "mikeneko@gmail.com", "country": "JAPAN"}' -c cookie-jar -k https://cs3103.cs.unb.ca:31308/user
	def post(self):
		if not request.json: # If the requested object is not in json format
			abort(400) # bad request
		
		parser = reqparse.RequestParser()
		try:
 			# Check for required attributes in json document, create a dictionary
			parser.add_argument('username', type=str, required=True)
			parser.add_argument('password', type=str, required=True)
			parser.add_argument('email', type=str, required=True)
			parser.add_argument('country', type=str, required=True)
			request_params = parser.parse_args()
		except:
			abort(400) # bad request

		try:
			cursor = mysql.cursor()
			_userName = request_params['username']
			_userPwd = request_params['password']
			_email = request_params['email']
			_country = request_params['country']
			param = "CALL createUser('" +  _userName + "', '" + _userPwd + "', '" + _email + "', '" + _country + "')"
			cursor.execute(param)
			mysql.commit()
			lastId = cursor.fetchall()
			if(len(lastId) == 1):
				for row in lastId:
					_userId = str(row['LAST_INSERT_ID()'])
				return {'status': 200, 'LAST_INSERT_ID': _userId}
			else:
				abort(400)
				return {'status': 400, 'message': "BAD REQUEST"}
		except:
			abort(400) # bad request
	
	# GET: Retrieve all the users in the database
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X GET -b cookie-jar
	#	-k https://cs3103.cs.unb.ca:31308/user
	def get(self):
		try:
			cursor = mysql.cursor()
			param = "CALL getAllUsers()"
			cursor.execute(param)
			mysql.commit()
			users = cursor.fetchall()
			if(len(users) > 0):
				i = 0
				user = [0] * len(users)
				for row in users:
					user[i] = {"Name": str(row['userName']), 
					"Country": str(row['userCountry']), 
					"Join Date": str(row['createDate'])}
					i = i+1
				return {'status': 200, 'User': user}
			else:
				abort(404)
				return {'status': 404, 'message': "No Content"}
		except:
			abort(400) # bad request

class UserWithId(Resource):
	# GET: Get a specific user via userid
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X GET -b cookie-jar
	#	-k https://cs3103.cs.unb.ca:31308/user/1
	def get(self, _userId):
		try:
			cursor = mysql.cursor()
			param = "CALL getUserById('" + str(_userId) + "')"
			cursor.execute(param)
			mysql.commit()
			user = cursor.fetchall()
			if(len(user) > 0):
				for row in user:
					returnedUser = {"Name": str(row['userName']), 
					"Country": str(row['userCountry']), 
					"Join Date": str(row['createDate'])}
				return {'status': 200, 'User': returnedUser}
			else:
				abort(404)
				return {'status': 404, 'message': "BAD REQUEST"}
		except:
			abort(400) # bad request
	
	# PUT: Update the info of an existing user providing userid
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X PUT -d 
	# '{"username": "gwar_gura", "password": "sh0rkzzz", "email": "gwargura@hotmail.com", "country":"CANADA"}' 
	# -c cookie-jar -k https://cs3103.cs.unb.ca:31308/user/1
	def put(self, _userId):
		if not request.json: # If the requested object is not in json format
			abort(400) # bad request
		
		parser = reqparse.RequestParser()
		try:
 			# Check for required attributes in json document, create a dictionary
			parser.add_argument('username', type=str, required=True)
			parser.add_argument('password', type=str, required=True)
			parser.add_argument('email', type=str, required=True)
			parser.add_argument('country', type=str, required=True)
			request_params = parser.parse_args()
		except:
			abort(400) # bad request
		
		try:
			cursor = mysql.cursor()
			_userName = request_params['username']
			_userPwd = request_params['password']
			_email = request_params['email']
			_country = request_params['country']
			param = "CALL updateUser('" + _userId + "', '" +  _userName + "', '" + _userPwd + "', '" + _email + "', '" + _country + "')"
			cursor.execute(param)
			mysql.commit()
			updatedUser = cursor.fetchall()
			if(len(updatedUser) > 0):
				for row in updatedUser:
					username = {"Id": str(row['userId']),
						"Name": str(row['userName'])}
				return {'status': 200, 'Updated User': username}
			else:
				abort(404)
				return {'status': 404, 'message': "USER NOT FOUND"}
		except:
			abort(400) # bad request

	
	# DELETE: Delete a specific user providing its userid
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar
	#	-k https://info3103.cs.unb.ca:31308/5
	def delete(self, _userId):
		try:
			cursor = mysql.cursor()
			param = "CALL delUserById('" + str(_userId) + "')"
			cursor.execute(param)
			mysql.commit()
			deletedUser = cursor.fetchall()
			if(len(deletedUser) > 0):
				for row in deletedUser:
					username = {"Id": str(row['userId']),
						"Name": str(row['userName'])}
				return {'status': 200, 'Deleted User': username}
			else:
				abort(404)
				return {'status': 404, 'message': "USER NOT FOUND"}
		except:
			abort(400) # bad request


# class Video
class VideoInit(Resource):
	# POST: Create a video for a specific user
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X POST -d '{"title":"minecraft chu", "size": 200}' 
	# -c cookie-jar -k https://cs3103.cs.unb.ca:31308/user/1/video
	def post(self, _userId):
		if not request.json: # If the requested object is not in json format
			abort(400) # bad request
		
		parser = reqparse.RequestParser()
		try:
 			# Check for required attributes in json document, create a dictionary
			parser.add_argument('title', type=str, required=True)
			parser.add_argument('size', type=str, required=True)
			request_params = parser.parse_args()
		except:
			abort(400) # bad request

		try:
			cursor = mysql.cursor()
			_videoTitle = request_params['title']
			_videoSize = request_params['size']
			param = "CALL createVideo('" +  _userId + "', '" + _videoTitle + "', '" + str(_videoSize) + "')"
			cursor.execute(param)
			mysql.commit()
			lastId = cursor.fetchall()
			if(len(lastId) == 1):
				for row in lastId:
					_videoId = str(row['LAST_INSERT_ID()'])
				return {'status': 200, 'LAST_INSERT_ID': _videoId}
			else:
				abort(400)
				return {'status': 400, 'message': "BAD REQUEST"}
		except:
			abort(400) # bad request
	
	# GET: Get all the videos of a user
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X GET -b cookie-jar
	#	-k https://cs3103.cs.unb.ca:31308/user/1/video
	def get(self, _userId):
		try:
			cursor = mysql.cursor()
			param = "CALL getUserVideo('" + str(_userId) + "')"
			cursor.execute(param)
			mysql.commit()
			videos = cursor.fetchall()
			if(len(videos) > 0):
				i = 0
				video = [0] * len(videos)
				for row in videos:
					video[i] = {"title": str(row['videoTitle']), 
					"size": str(row['videoSize']), 
					"likes": str(row['likes']), 
					"Upload Date": str(row['uploadDate'])}
					i = i+1
				return {'status': 200, 'Video': video}
			else:
				abort(404)
				return {'status': 404, 'message': "No Content"}
		except:
			abort(400) # bad request

# class Video
class VideoSpec(Resource):
	# GET: Get a user's video
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X GET -b cookie-jar
	#	-k https://cs3103.cs.unb.ca:31308/user/1/video/1
	def get(self, _userId, _videoId):
		try:
			cursor = mysql.cursor()
			param = "CALL getVideoById(" + str(_userId) + "," + str(_videoId) + ")"
			cursor.execute(param)
			mysql.commit()
			video = cursor.fetchall()
			if(len(video) > 0):
				for row in video:
					returnedvideo = {"title": str(row['videoTitle']), 
					"size": str(row['videoSize']), 
					"likes": str(row['likes']), 
					"Upload Date": str(row['uploadDate'])}
				return {'status': 200, 'Video': returnedvideo}
			else:
				abort(404)
				return {'status': 404, 'message': "BAD REQUEST"}
		except:
			abort(400) # bad request
	
	# DELETE: Delete a user's video
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar
	#	-k https://info3103.cs.unb.ca:31308/1/video/2
	def delete(self, _userId, _videoId):
		try:
			cursor = mysql.cursor()
			param = "CALL delVideoById(" + str(_userId) + "," + str(_videoId) + ")"
			cursor.execute(param)
			mysql.commit()
			deletedVideo = cursor.fetchall()
			if(len(deletedVideo) > 0):
				for row in deletedVideo:
					video = {"id": str(row['videoId']),
						"title": str(row['videoTitle']), 
					"size": str(row['videoSize']), 
					"Upload Date": str(row['uploadDate'])}
				return {'status': 200, 'Deleted Video': video}
			else:
				abort(404)
				return {'status': 404, 'message': "USER NOT FOUND"}
		except:
			abort(400) # bad request

####################################################################################
#
# Identify/create endpoints and endpoint objects
#
api = Api(app)
api.add_resource(SignIn, '/signin')
api.add_resource(GeneralUser, '/user')
api.add_resource(UserWithId, '/user/<_userId>')

api.add_resource(VideoInit, '/user/<_userId>/video')
api.add_resource(VideoSpec, '/user/<_userId>/video/<_videoId>')


#############################################################################
# xxxxx= last 5 digits of your studentid. If xxxxx > 65535, subtract 30000
if __name__ == "__main__":
# 	#
# 	# You need to generate your own certificates. To do this:
# 	#	1. cd to the directory of this app
# 	#	2. run the makeCert.sh script and answer the questions.
# 	#	   It will by default generate the files with the same names specified below.
# 	#
	context = ('cert.pem', 'key.pem') # Identify the certificates you've generated.
	app.run(
		host=settings.APP_HOST,
		port=settings.APP_PORT,
		ssl_context=context,
		debug=settings.APP_DEBUG)