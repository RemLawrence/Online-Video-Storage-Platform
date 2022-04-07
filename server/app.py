#!/usr/bin/env python3
import sys
from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import reqparse, Resource, Api
from flask_session import Session
import json
from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import *
import ssl #include ssl libraries
from flask_cors import CORS

import pymysql.cursors 

import settings # Our server and db settings, stored in settings.py

app = Flask(__name__)
CORS(app)
# Set Server-side session config: Save sessions in the local app directory.
app.config['SECRET_KEY'] = settings.SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = 'what'
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
	return make_response(jsonify( { 'status': 'Bad Request' } ), 400)

@app.errorhandler(401) # decorators to add to 401 response
def not_found(error):
	return make_response(jsonify( { 'status': 'Unauthorized' } ), 401)

@app.errorhandler(403) # decorators to add to 403 response
def not_found(error):
	return make_response(jsonify( { 'status': 'Forbidden' } ), 403)

@app.errorhandler(404) # decorators to add to 404 response
def not_found(error):
	return make_response(jsonify( { 'status': 'Resource not found' } ), 404)

@app.errorhandler(500) # decorators to add to 500 response
def not_found(error):
	return make_response(jsonify( { 'status': 'Internal server error' } ), 500)

###################################################################################
#
# Routing: GET and POST using Flask-Session
#
class SignIn(Resource):
	# (✓) 1. POST: Set Session and return Cookie
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X POST -d '{"username": "gwargura", "password": "sh0rkAAAA++"}'
	#  	-c cookie-jar -k https://cs3103.cs.unb.ca:31308/signin
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
			if request_params['username'] in session:
				response = {'status': 'success'}
				responseCode = 200
			else:
				try:
					cursor = mysql.cursor()
					_userName = request_params['username']
					_userPwd = request_params['password']
					param = "CALL loginUser('" +  _userName + "', '" + _userPwd + "')"
					cursor.execute(param)
					mysql.commit()
					user = cursor.fetchall()
					if(len(user) > 0):
						try:	
							ldapServer = Server(host=settings.LDAP_HOST)
							ldapConnection = Connection(ldapServer,
								raise_exceptions=False,
								user='uid='+request_params['username']+', ou=People,ou=fcs,o=unb',
								password = request_params['password'])
							ldapConnection.open()
							ldapConnection.start_tls()
							ldapConnection.bind()
							# At this point we have sucessfully authenticated.
							session['username'] = request_params['username']
							response = {'status': 'success'}
							responseCode = 201
						except LDAPException:
							response = {'status': 'Access denied'}
							responseCode = 401
						finally:
							ldapConnection.unbind()
					else:
						response = {'status': 'Username or password not correct'}
						responseCode = 401
				except:
					abort(400) # bad request
			return make_response(jsonify(response), responseCode)
		except:
			abort(400) # bad request

	# (✕) 2. GET: Check Cookie data with Session data
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X GET -b cookie-jar
	# 	-k https://cs3103.cs.unb.ca:61340/signin
	def get(self):
		success = False
		# Auth check
		if 'username' in session:
			username = session['username']
			response = {'status': 'success', 'user in session': username}
			responseCode = 200
		else:
			abort(401)

		return make_response(jsonify(response), responseCode)

	# (✓) 3. DELETE: Check Cookie data with Session data (logout?)
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar
	#	-k https://cs3103.cs.unb.ca:61340/signin
	def delete(self):

		# Auth check
		if 'username' in session:
			username = session['username']
			# Delete the session
			session.clear()
			response = {'status': 'success', 'deleted username in session': username}
			responseCode = 200
		else:
			abort(401)

		return make_response(jsonify(response), responseCode)


# class GeneralUser
class SignUp(Resource):
	# (✓) 4. POST: Create a new user
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X POST -d '{"username": "ameliawatson", "password": "ameame22", 
	# "email": "ame_holoEN@gmail.com", "country": "UK"}' -c cookie-jar -k https://cs3103.cs.unb.ca:31308/signup
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
				response = {'status': 'created'}
				responseCode = 201
			else:
				abort(400)

			return make_response(jsonify(response), responseCode)

		except:
			abort(400) # bad request

class UserWithName(Resource):
	# (✓) 5. GET: Get a specific user via username
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X GET -b cookie-jar
	#	-k https://cs3103.cs.unb.ca:31308/user/gwargura
	def get(self, _userName):
		try:
			cursor = mysql.cursor()
			param = "CALL getUserByName('" + str(_userName) + "')"
			cursor.execute(param)
			mysql.commit()
			user = cursor.fetchall()
			if(len(user) > 0):
				for row in user:
					returnedUser = {"Name": str(row['userName']), 
					"Country": str(row['userCountry']), 
					"JoinDate": str(row['createDate'])}
				response = {'status': 'success', 'User': returnedUser}
				responseCode = 200
			else:
				response = {'status': 'User not found'}
				responseCode = 404
				
			return make_response(jsonify(response), responseCode)
		except:
			abort(400) # bad request
	
	# 6. PUT: Update the info of an existing user providing username
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X PUT -d 
	# '{"username": "gwar_gura", "password": "sh0rkzzz", "email": "gwargura@hotmail.com", "country":"CANADA"}' 
	# -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/gwarguraa
	def put(self, _userName):
		# Auth check
		if 'username' in session:
			username = session['username']
			if(username != _userName):
				abort(401)
		else:
			abort(401)
		
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
			_newUserName = request_params['username']
			_newUserPwd = request_params['password']
			_newEmail = request_params['email']
			_newCountry = request_params['country']
			param = "CALL updateUser('" + _userName + "', '" +  _newUserName + "', '" + _newUserPwd + "', '" + _newEmail + "', '" + _newCountry + "')"
			cursor.execute(param)
			mysql.commit()
			updatedUser = cursor.fetchall()
			if(len(updatedUser) > 0):
				for row in updatedUser:
					username = {"Id": str(row['userId']),
						"Name": str(row['userName'])}
				# session['username'] = _newUserName
				response = {'status': 'success', 'Updated User': username}
				responseCode = 200
			else:
				response = {'status': 'User not found'}
				responseCode = 404
			return make_response(jsonify(response), responseCode)
		except:
			abort(400) # bad request

	
	# (✕) 7. DELETE: Delete a specific user providing its username
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar
	#	-k https://cs3103.cs.unb.ca:31308/user/gwarguraa
	def delete(self, _userName):
		# Auth check
		if 'username' in session:
			username = session['username']
			if(username != _userName):
				abort(401)
		else:
			abort(401)

		try:
			cursor = mysql.cursor()
			param = "CALL delUserByName('" + str(_userName) + "')"
			cursor.execute(param)
			mysql.commit()
			deletedUser = cursor.fetchall()
			if(len(deletedUser) > 0):
				for row in deletedUser:
					username = {"Id": str(row['userId']),
						"Name": str(row['userName'])}
				response = {'status': 'Deleted', 'Deleted User': username}
				responseCode = 200
			else:
				response = {'status': 'User not found'}
				responseCode = 404
			return make_response(jsonify(response), responseCode)
		except:
			abort(400) # bad request


# class Video
class VideoInit(Resource):
	# (✓) 8. POST: Create a video for a specific user
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X POST -d '{"id":"yqWzCV0kU_c", "size": 200}' 
	# -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/gwargura/video
	def post(self, _userName):
		# Auth check
		if 'username' in session:
			username = session['username']
			if(username != _userName):
				abort(401)
		else:
			abort(401)

		if not request.json: # If the requested object is not in json format
			abort(400) # bad request
		
		parser = reqparse.RequestParser()
		try:
 			# Check for required attributes in json document, create a dictionary
			parser.add_argument('id', type=str, required=True)
			parser.add_argument('size', type=str, required=True)
			request_params = parser.parse_args()
		except:
			abort(400) # bad request

		try:
			cursor = mysql.cursor()
			_videoId = request_params['id']
			_videoSize = request_params['size']
			param = "CALL createVideo('" +  _userName + "', '" + _videoId + "', '" + str(_videoSize) + "')"
			cursor.execute(param)
			mysql.commit()
			lastId = cursor.fetchall()
			if(len(lastId) == 1):
				for row in lastId:
					videoId = str(row['LAST_INSERT_ID()'])
				response = {'status': 'created'}
				responseCode = 201
			else:
				abort(400)
			return make_response(jsonify(response), responseCode)
		except:
			abort(400) # bad request
	
	# (✓) 9. GET: Get all the videos of a user
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X GET -b cookie-jar
	#	-k https://cs3103.cs.unb.ca:31308/user/uruha_rushia/video
	def get(self, _userName):
		try:
			cursor = mysql.cursor()
			param = "CALL getUserVideo('" + str(_userName) + "')"
			cursor.execute(param)
			mysql.commit()
			videos = cursor.fetchall()
			if(len(videos) > 0):
				i = 0
				video = [0] * len(videos)
				for row in videos:
					video[i] = {"id": str(row['videoId']), 
					"size": str(row['videoSize']), 
					"likes": str(row['likes']), 
					"Upload Date": str(row['uploadDate'])}
					i = i+1
				response = {'status': 'success', 'Videos': video}
				responseCode = 200
			else:
				response = {'status': 'User not found'}
				responseCode = 404
			return make_response(jsonify(response), responseCode)
		except:
			abort(400) # bad request

# class Video
class VideoSpec(Resource):
	# (✕) 10. GET: Get a user's video
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X GET -b cookie-jar
	#	-k https://cs3103.cs.unb.ca:31308/user/gwargura/video/574dc2c0-aaf7-11ec-b658-525400a3fea8
	def get(self, _userName, _videoId):
		try:
			cursor = mysql.cursor()
			param = "CALL getVideoById('" + _userName + "','" + _videoId + "')"
			cursor.execute(param)
			mysql.commit()
			video = cursor.fetchall()
			if(len(video) > 0):
				for row in video:
					returnedvideo = {"title": str(row['videoTitle']), 
					"size": str(row['videoSize']), 
					"likes": str(row['likes']), 
					"Upload Date": str(row['uploadDate'])}
				response = {'status': 'success', 'Video': returnedvideo}
				responseCode = 200
			else:
				response = {'status': 'User or video not found'}
				responseCode = 404
			return make_response(jsonify(response), responseCode)
		except:
			abort(400) # bad request

	# (✕) 11. PUT: Update the likes of a spefiic video
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X PUT -d '{"likes":1}' -b cookie-jar -k 
	# https://cs3103.cs.unb.ca:31308/user/gwargura/video/574dc2c0-aaf7-11ec-b658-525400a3fea8
	def put(self, _userName, _videoId):
		if not request.json: # If the requested object is not in json format
			abort(400) # bad request
		
		parser = reqparse.RequestParser()
		try:
 			# Check for required attributes in json document, create a dictionary
			parser.add_argument('likes', type=str, required=True)
			request_params = parser.parse_args()
		except:
			abort(400) # bad request

		try:
			cursor = mysql.cursor()
			_likes = request_params['likes']
			param = "CALL updateVideoLike('" + _userName + "','" + _videoId + "'," + str(_likes) + ")"
			cursor.execute(param)
			mysql.commit()
			video = cursor.fetchall()
			if(len(video) > 0):
				for row in video:
					returnedvideo = {"title": str(row['videoTitle']), 
					"size": str(row['videoSize']), 
					"likes": str(row['likes']), 
					"Upload Date": str(row['uploadDate'])}
				response = {'status': 'success', 'Updated Video': returnedvideo}
				responseCode = 200
			else:
				response = {'status': 'User or video not found'}
				responseCode = 404
			return make_response(jsonify(response), responseCode)
		except:
			abort(400) # bad request
	
	# (✓) 12. DELETE: Delete a user's video
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar
	#	-k https://cs3103.cs.unb.ca:31308/user/uruha_rushia/video/2f050dce-aaf0-11ec-b658-525400a3fea8
	def delete(self, _userName, _videoId):
		# Auth check
		if 'username' in session:
			username = session['username']
			if(username != _userName):
				abort(401)
		else:
			abort(401)
		
		try:
			cursor = mysql.cursor()
			param = "CALL delVideoById('" + _userName + "','" + _videoId + "')"
			cursor.execute(param)
			mysql.commit()
			deletedVideo = cursor.fetchall()
			if(len(deletedVideo) > 0):
				for row in deletedVideo:
					video = {"id": str(row['videoId']),
					"size": str(row['videoSize']), 
					"Upload Date": str(row['uploadDate'])}
				response = {'status': 'Deleted', 'Deleted Video': video}
				responseCode = 200
			else:
				response = {'status': 'User or video not found'}
				responseCode = 404
			return make_response(jsonify(response), responseCode)
		except:
			abort(400) # bad request


class VideoListInit(Resource):
	# (✓) 13. POST: Create a video list for a user
	# Example curl command: 
	# curl -i -H "Content-Type: application/json" -X POST -d 
	# '{"name": "holo_EN", "description": ""}' 
	# -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/gwargura/videolist
	def post(self, _userName):
		# Auth check
		if 'username' in session:
			username = session['username']
			if(username != _userName):
				abort(401)
		else:
			abort(401)
		
		if not request.json: # If the requested object is not in json format
			abort(400) # bad request
		
		parser = reqparse.RequestParser()
		try:
 			# Check for required attributes in json document, create a dictionary
			parser.add_argument('name', type=str, required=True)
			parser.add_argument('description', type=str, required=True)
			request_params = parser.parse_args()
		except:
			abort(400) # bad request
		
		try:
			cursor = mysql.cursor()
			_name = request_params['name']
			_description = request_params['description']
			param = "CALL createVideoList('" + _userName + "','" + _name + "','" + _description + "')"
			cursor.execute(param)
			mysql.commit()
			createdVideoList = cursor.fetchall()
			if(len(createdVideoList) > 0):
				for row in createdVideoList:
					_videoListId = str(row['LAST_INSERT_ID()'])
				response = {'status': 'created'}
				responseCode = 201
			else:
				abort(400)
			return make_response(jsonify(response), responseCode)
		except:
			abort(400) # bad request
	
	# (✓) 14. GET: Get all the videolists of a user
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X GET -b cookie-jar
	#	-k https://cs3103.cs.unb.ca:31308/user/gwargura/videolist
	def get(self, _userName):
		try:
			cursor = mysql.cursor()
			param = "CALL getUserVideoList('" + str(_userName) + "')"
			cursor.execute(param)
			mysql.commit()
			videolists = cursor.fetchall()
			if(len(videolists) > 0):
				i = 0
				videolist = [0] * len(videolists)
				for row in videolists:
					videolist[i] = {"user": _userName,
						"id": str(row['videoListId']), 
						"name": str(row['videoListTitle']), 
					"description": str(row['description'])}
					i = i+1
				response = {'status': 'success', 'VideoLists': videolist}
				responseCode = 200
			else:
				response = {'status': 'User not found'}
				responseCode = 404
			return make_response(jsonify(response), responseCode)
		except:
			abort(400) # bad request
		
class VideoList(Resource):
	# (✓) 15. GET: Get the info of a videolist (videos, essentially)
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k 
	# https://cs3103.cs.unb.ca:31308/user/gwargura/videolist/81daada9-ac5f-11ec-b658-525400a3fea8
	def get(self, _userName, _videoListId):
		try:
			cursor = mysql.cursor()
			param = "CALL getVideoInVideoList('" + _userName + "','" + _videoListId + "')"
			cursor.execute(param)
			mysql.commit()
			videolists = cursor.fetchall()
			if(len(videolists) > 0):
				i = 0
				videolist = [0] * len(videolists)
				for row in videolists:
					videolist[i] = {"videoId": str(row['vv_videoId'])}
					i = i+1
				response = {'status': 'success', 'VideoList': videolist}
				responseCode = 200
			else:
				response = {'status': 'User or videolist not found'}
				responseCode = 404
			return make_response(jsonify(response), responseCode)
		except:
			abort(400) # bad request

	# 16. PUT: Update existing videolist info
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X PUT -d 
	# '{"name": "holo_JP(2019-2022)", "description": "unthinkable memories"}' -b cookie-jar 
	# -k https://cs3103.cs.unb.ca:31308/user/uruha_rushia/videolist/b21224ab-ac70-11ec-b658-525400a3fea8
	def put(self, _userName, _videoListId):
		# Auth check
		if 'username' in session:
			username = session['username']
			if(username != _userName):
				abort(401)
		else:
			abort(401)

		if not request.json: # If the requested object is not in json format
			abort(400) # bad request
		
		parser = reqparse.RequestParser()
		try:
 			# Check for required attributes in json document, create a dictionary
			parser.add_argument('name', type=str, required=True)
			parser.add_argument('description', type=str, required=True)
			request_params = parser.parse_args()
		except:
			abort(400) # bad request
		
		try:
			cursor = mysql.cursor()
			_name = request_params['name']
			_description = request_params['description']
			param = "CALL updateVideoList('" + _userName + "','" + _videoListId + "','" + _name + "','" + _description + "')"
			cursor.execute(param)
			mysql.commit()
			updatedVideoList = cursor.fetchall()
			if(len(updatedVideoList) > 0):
				for row in updatedVideoList:
					returnedvideolist = {"title": str(row['videoListTitle']), 
					"description": str(row['description'])}
				response = {'status': 'success', 'Updated VideoList': returnedvideolist}
				responseCode = 200
			else:
				response = {'status': 'User or videolist not found'}
				responseCode = 404
			return make_response(jsonify(response), responseCode)
		except:
			abort(400) # bad request

	# (✓) 17. DELETE: Delete a videolist for a user
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k 
	# https://cs3103.cs.unb.ca:31308/user/gwargura/videolist/81daada9-ac5f-11ec-b658-525400a3fea8
	def delete(self, _userName, _videoListId):
		# Auth check
		if 'username' in session:
			username = session['username']
			if(username != _userName):
				abort(401)
		else:
			abort(401)

		try:
			cursor = mysql.cursor()
			param = "CALL delVideoList('" + _userName + "','" + _videoListId + "')"
			cursor.execute(param)
			mysql.commit()
			deletedvideolist = cursor.fetchall()
			if(len(deletedvideolist) > 0):
				for row in deletedvideolist:
					videolist = { "id": str(row['videoListId']),
						"title": str(row['videoListTitle']), 
					"description": str(row['description'])}
				response = {'status': 'Deleted', 'Deleted VideoList': videolist}
				responseCode = 200
			else:
				response = {'status': 'User or videolist not found'}
				responseCode = 404
			return make_response(jsonify(response), responseCode)
		except:
			abort(400) # bad request

class AddVideoToVideoList(Resource):
	# (✓) 18. POST: Add a video to a videolist
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X POST -d 
	# '{"videoId": "574dc2c0-aaf7-11ec-b658-525400a3fea8"}' 
	# -b cookie-jar -k 
	# https://cs3103.cs.unb.ca:31308/user/gwargura/videolist/9313ec35-ac5c-11ec-b658-525400a3fea8/addVideo
	def post(self, _userName, _videoListId):
		# Auth check
		if 'username' in session:
			username = session['username']
			if(username != _userName):
				abort(401)
		else:
			abort(401)

		if not request.json: # If the requested object is not in json format
			abort(400) # bad request
		
		parser = reqparse.RequestParser()
		try:
 			# Check for required attributes in json document, create a dictionary
			parser.add_argument('videoId', type=str, required=True)
			request_params = parser.parse_args()
		except:
			abort(400) # bad request
		
		try:
			cursor = mysql.cursor()
			_videoId = request_params['videoId']
			param = "CALL addVideoToVideoList('" + _userName + "','" + _videoId + "','" + _videoListId + "')"
			cursor.execute(param)
			mysql.commit()
			addedVideoId = cursor.fetchall()
			if(len(addedVideoId) > 0):
				for row in addedVideoId:
					_videoListId = str(row['LAST_INSERT_ID()'])
				response = {'status': 'created'}
				responseCode = 201
			else:
				response = {'status': 'User or videolist not found'}
				responseCode = 404
			return make_response(jsonify(response), responseCode)
		except:
			abort(400) # bad request

class DelVideoFromVideoList(Resource):
	# 19. DELETE: Delete a video from a videolist
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X DELETE -d 
	# '{"videoId": "574dc2c0-aaf7-11ec-b658-525400a3fea8"}' -b cookie-jar -k 
	# https://cs3103.cs.unb.ca:31308/user/gwargura/videolist/9313ec35-ac5c-11ec-b658-525400a3fea8/deleteVideo
	def delete(self, _userName, _videoListId):
		# Auth check
		if 'username' in session:
			username = session['username']
			if(username != _userName):
				abort(401)
		else:
			abort(401)

		if not request.json: # If the requested object is not in json format
			abort(400) # bad request
		
		parser = reqparse.RequestParser()
		try:
 			# Check for required attributes in json document, create a dictionary
			parser.add_argument('videoId', type=str, required=True)
			request_params = parser.parse_args()
		except:
			abort(400) # bad request

		try:
			cursor = mysql.cursor()
			_videoId = request_params['videoId']
			param = "CALL delVideoFromVideoList('" + _userName + "','" + _videoId + "','" + _videoListId + "')"
			cursor.execute(param)
			mysql.commit()
			deletedVideoId = cursor.fetchall()
			if(len(deletedVideoId) > 0):
				for row in deletedVideoId:
					_video = {"deleted video": str(row['vv_videoId']),
						"video list": str(row['vv_videoListId'])}
				response = {'status': 'Deleted', 'Deleted Video': _video}
				responseCode = 200
			else:
				response = {'status': 'User or video or videolist not found'}
				responseCode = 404
			return make_response(jsonify(response), responseCode)
		except:
			abort(400) # bad request

####################################################################################
#
# Identify/create endpoints and endpoint objects
#
api = Api(app)
api.add_resource(SignIn, '/signin')
api.add_resource(SignUp, '/signup')
api.add_resource(UserWithName, '/user/<_userName>')

api.add_resource(VideoInit, '/user/<_userName>/video')
api.add_resource(VideoSpec, '/user/<_userName>/video/<_videoId>')

api.add_resource(VideoListInit, '/user/<_userName>/videolist')
api.add_resource(VideoList, '/user/<_userName>/videolist/<_videoListId>')
api.add_resource(AddVideoToVideoList, '/user/<_userName>/videolist/<_videoListId>/addVideo')
api.add_resource(DelVideoFromVideoList, '/user/<_userName>/videolist/<_videoListId>/deleteVideo')


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