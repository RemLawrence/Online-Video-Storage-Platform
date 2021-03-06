TODO:
1. Password strength check
2. Back to login button (back button)
3. Can't add ' and space in username/pwd/email
4. Give user card some style (outline? bg-Color?)
5. Dude, there's no way to know which users we have.

7. Video - hint image
8. Give your own videolists some colors
9. There should be some styles differences between your own videolists and other users' videolists 

![ER Diagram](https://github.com/RemLawrence/Online-Video-Storage-Platform/blob/main/docs/ERD.png)

All Stored Procedures:
1. loginUser: Check username and password
2. createUser: Create a new user
3. getUserByName: Get a specific user via username
4. updateUser: Update the info of an existing user providing username
5. delUserByName: Delete a specific user providing its username
6. createVideo: Create a video for a specific user
7. getUserVideo: Get all the videos of a user
8. getVideoById: Get a user's video
9. updateVideoLike: Update the likes of a spefiic video
10. delVideoById: Delete a user's video
11. createVideoList: Create a video list for a user
12. getUserVideoList: Get all the videolists of a user
13. getVideoInVideoList: Get the info of a videolist (videos, essentially)
14. updateVideoList: Update existing videolist info
15. delVideoList: Delete a videolist for a user
16. addVideoToVideoList: Add a video to a videolist
17. delVideoFromVideoList: Delete a video from a videolist

Application Directory Structure:
project
    -> /client
        -> stores html/css/js scripts
    -> /server
        -> /sql
            -> /table
                -> stores 4 tables: user, video, videolist, video_videolist
            -> /procedure
                -> /User
                    -> stores procedures relevant to the user endpoint
                -> /Video
                    -> stores procedures relevant to the video endpoint
                -> /VideoList
                    -> stores procedures relevant to the videolist endpoint
        -> app.py
        -> settings.py


Curl Test Plan:
1. Create session cookie, aka Login user:
   Endpoint: POST /signin
    Case 1: Successfully login: 
    curl -i -H "Content-Type: application/json" -X POST -d '{"username": "gwargura", "password": "sh0rkAAAA++"}' -c cookie-jar -k https://cs3103.cs.unb.ca:31308/signin
    Response: 200

    Case 2: Username unmatched:
    curl -i -H "Content-Type: application/json" -X POST -d '{"username": "ina_nis", "password": "sh0rkAAAA++"}' -c cookie-jar -k https://cs3103.cs.unb.ca:31308/signin
    Response: 401

    Case 3: Password unmatched:
    curl -i -H "Content-Type: application/json" -X POST -d '{"username": "ina_nis", "password": "sh0rkAAAA++"}' -c cookie-jar -k https://cs3103.cs.unb.ca:31308/signin
    Response: 401


2. (AUTH REQUIRED) Get session cookie:
   Endpoint: GET /signin
    Case 1: Current user exists in cookie (Do #1 Case 1 first):
    curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://cs3103.cs.unb.ca:61340/signin
    Response: 200 + username

    Case 2: No user exist in cookie (Doesn't do #1 Case 1):
    curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://cs3103.cs.unb.ca:61340/signin
    Response: 401


3. (AUTH REQUIRED) Delete session cookie, aka Logout user: 
   Endpoint: DELETE /signin
    Case 1: Successfully deleted the session cookie (Do #1 Case 1 first):
    curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k https://cs3103.cs.unb.ca:61340/signin
    Response: 200 + username

    Case 2: There's no cookie, yet (Doesn't do #1 Case 1):
    curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k https://cs3103.cs.unb.ca:61340/signin
    Response: 401


4. Signup, or aka create a new user
   Endpoint: POST /signup
    Case 1: Successfully created a new user:
    curl -i -H "Content-Type: application/json" -X POST -d '{"username": "ina_nis", "password": "drawing123", "email": "inanisEN@gmail.com", "country": "USA"}' -c cookie-jar -k https://cs3103.cs.unb.ca:31308/signup
    Response: 201

    Case 2: Username duplicated
    curl -i -H "Content-Type: application/json" -X POST -d '{"username": "gwargura", "password": "ameame22", "email": "ame_holoEN@gmail.com", "country": "UK"}' -c cookie-jar -k https://cs3103.cs.unb.ca:31308/signup
    Response: 400

    Case 3: Does not provide country:
    curl -i -H "Content-Type: application/json" -X POST -d '{"username":"moonaa", "password":"moona_ID", "email": "moonah@gmail.com", "country": ""}' -c cookie-jar -k https://cs3103.cs.unb.ca:31308/signup
    Response: 201


5. Get a user's info
   Endpoint: GET /user/{username}
    Case 1: Get an existing user's info:
    curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/gwargura
    Response: 200 + User object

    Case 2: User does not exist:
    curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/gwargur
    Response: 404


6. (AUTH REQUIRED) Update a user's info
   Endpoint: PUT /user/{username}
    Case 1: Update an existing user's info upon logged in (Do #1 Case 1 first):
    curl -i -H "Content-Type: application/json" -X PUT -d '{"username":"gwargura", "password":"sh0rkAAAA++", "email": "gwargura@gmail.com", "country": "CANADA"}' -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/gwargura
    Response: 200 + User Object

    Case 2: Update with an existing user's Username
    curl -i -H "Content-Type: application/json" -X PUT -d '{"username":"mori++calli", "password":"sh0rkAAAA++", "email": "gwargura@gmail.com", "country": "CANADA"}' -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/gwargura
    Response: 400

    Case 3: Update an existing user's info (Doesn't do #1 Case 1):
    Case 1: Update an existing user's info upon logged in (Do #1 Case 1 first):
    curl -i -H "Content-Type: application/json" -X PUT -d '{"username":"gwargura", "password":"sh0rkAAAA++", "email": "gwargura@gmail.com", "country": "CANADA"}' -c cookie-jar -k https://cs3103.cs.unb.ca:31308/user/gwargura
    Response: 401


7. (AUTH REQUIRED) Delete a user
   Endpoint: DELETE /user/{username}
   Case 1: Delete an existing user upon logged in (Do #1 Case 1 first) (In this case, if you wanna delete user ina_nis, ina_nis's password is drawing123. Do the login first please):
   curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/ina_nis

   Case 2: Delete a non-existing user:
   curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/moon
   Response: 401

   Case 3: Delete an existing user without logged in (Doesn't do #1 Case 1):
   curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/gwarguraa
   Response: 404


8. (AUTH REQUIRED) Create a video for a user
   Endpoint: POST /user/{username}/video
    Case 1: Upload a video for an existing user upon logged in (Do #1 Case 1 first):
    curl -i -H "Content-Type: application/json" -X POST -d '{"title":"debut stream archieve", "size": 2000}' -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/gwargura/video
    Response: 201

    Case 2: Upload a video for an existing user upon logged in (Doesn't do #1 Case 1):
    curl -i -H "Content-Type: application/json" -X POST -d '{"title":"debut stream archieve", "size": 2000}' -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/gwargura/video
    Response: 401


9. Retrieve all videos of a user
   Endpoint: GET /user/{username}/video
    Case 1: Get all videos of an existing user
    curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/uruha_rushia/video
    Response: 200 + Array of Video Object

    Case 2: Get all videos of a non-existing user
    curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/moon/video
    Response: 404


10. Get a video of a user
   Endpoint: GET /user/{username}/video/{videoid}
    Case 1: Get an existing user's video providing a valid videoid
    curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/uruha_rushia/video/e1e858f0-aac2-11ec-b658-525400a3fea8
    Respones: 200 + Video Object

    Case 2: Get an existing user's video providing an invalid videoid
    curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/uruha_rushia/video/1
    Resonse: 404

    Case 3: Get a non-existing user's video providing a valid videoid
    curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/moon/video/e1e858f0-aac2-11ec-b658-525400a3fea8
    Resonse: 404


11. Update (the # of likes) of a user's video
    Endpoint: PUT /user/{username}/video/{videoid}
    Case 1: Update the # of likes for a user's video (valid username, valid videoid):
    curl -i -H "Content-Type: application/json" -X PUT -d '{"likes":1}' -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/gwargura/video/574dc2c0-aaf7-11ec-b658-525400a3fea8
    Response: 200 + Video Object

    Case 2: Update the # of likes for a user's video (valid username, invalid videoid):
    curl -i -H "Content-Type: application/json" -X PUT -d '{"likes":1}' -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/gwargura/video/1
    Response: 404

    Case 3: Update the # of likes for a user's video (invalid username, valid videoid):
    curl -i -H "Content-Type: application/json" -X PUT -d '{"likes":1}' -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/uruha_rushia/video/574dc2c0-aaf7-11ec-b658-525400a3fea8
    Response: 404    

    Case 4: Update the # of likes for a user's video (invalid username, invalid videoid):
    curl -i -H "Content-Type: application/json" -X PUT -d '{"likes":1}' -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/uruha_rushia/video/1
    Response: 404    


12. (AUTH REQUIRED) Delete a user's video
    Endpoint: DELETE /user/{username}/video/{videoid}
    Case 1: Delete a user's video upon logged in (Do #1 Case 1 first):
    curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/gwargura/video/c2e15bb1-adf8-11ec-b658-525400a3fea8
    Response: 200

    Case 2: Delete another user's video (Doesn't do #1 Case 1):
    curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/uruha_rushia/video/2f050dce-aaf0-11ec-b658-525400a3fea8
    Response: 401

    Case 3: Delete a user's video upon logged in, but with invalid videoid:
    curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/gwargura/video/1
    Response: 404


13. (AUTH REQUIRED) Create a videolist for a user:
    Endpoint: POST /user/{username}/videolist
    Case 1: Create a videolist for a user upon logged in (Do #1 Case 1 first):
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"comforting piano", "description":"just a collection of piano music"}' -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/gwargura/videolist
    Response: 201

    Case 2: Create a videolist for a user without logged in (Doesn't #1 Case 1):
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"comforting piano", "description":"just a collection of piano music"}' -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/uruha_rushia/videolist
    Response: 401


14. Get all the videolists of a user
    Endpoint: GET /user/{username}/videolist
    Case 1: Get the videolists of an existing user:
    curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/uruha_rushia/videolist
    Response: 200 + VideoList Object

    Case 2: Get the videolists of an non-existing user:
    curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/moon/videolist
    Response: 404


15. Get the info(videos) in a user's videolist
    Endpoint: GET /user/{username}/videolist/{videolistid}
    Case 1: Get the videos in videolists of an existing user (valid username, valid videolistid):
    curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/uruha_rushia/videolist/b21224ab-ac70-11ec-b658-525400a3fea8
    Response: 200 + Array of VideoId

    Case 2: Get the videos in videolists of a non-existing user (invalid username, valid videolistid):
    curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/uruha_rushi/videolist/b21224ab-ac70-11ec-b658-525400a3fea8
    Response: 404

    Case 3: Get the videos in videolists of an existing user (valid username, invalid videolistid):
    curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/uruha_rushi/videolist/1
    Response: 404

    Case 4: Get the videos in videolists of a non-existing user (invalid username, invalid videolistid):
    curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/uruha_rushi/videolist/1
    Response: 404


16. (AUTH REQUIRED) Update the info of a user's videolist
    Endpoint: PUT /user/{username}/videolist/{videolistid}
    Case 1: Update the videolist info of a user upon logged in (Do #1 Case 1 first):
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name":"comforting piano nyo", "description":"just a collection of piano music"}' -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/gwargura/videolist/3e7b595c-ae01-11ec-b658-525400a3fea8
    Response: 200 + VideoList Object

    Case 2: Update the videolist info of a user upon logged in with invalid videolistid (Do #1 Case 1 first):
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name":"comforting piano nyo", "description":"just a collection of piano music"}' -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/gwargura/videolist/1
    Response: 404

    Case 3: Update the videolist info of a user upon logged in with invalid videolistid (Doesn't do #1 Case):
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name":"comforting piano nyo", "description":"just a collection of piano music"}' -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/uruha_rushia/videolist/b21224ab-ac70-11ec-b658-525400a3fea8
    Respones: 401


17. (AUTH REQUIRED) Delete a videolist of a user
    Endpoint: DELETE /user/{username}/videolist/{videolistid}
    Case 1: Delete a videolist for a user upon logged in (Do #1 Case 1 first):
    curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/gwargura/videolist/7f70f65f-ac5f-11ec-b658-525400a3fea8
    Response: 200

    Case 2: Delete a videolist for a user without logging in (Doesn't do # 1 Case 1 first):
    curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/uruha_rushia/videolist/b21224ab-ac70-11ec-b658-525400a3fea
    Response: 401

    Case 3: Delete a videolist for a user upon logged in, but with invalid videolistid (Do #1 Case 1 first):
    curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/gwargura/videolist/1
    Respones: 404


18. (AUTH REQUIRED) Add a video to a videolist
    Endpoint: POST /user/{username}/videolist/{videolistid}/addVideo
    Case 1: Add a video to a videolist upon logged in (Do #1 Case 1 first):
    curl -i -H "Content-Type: application/json" -X POST -d '{"videoId":"574dc2c0-aaf7-11ec-b658-525400a3fea8"}' -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/gwargura/videolist/7f70f65f-ac5f-11ec-b658-525400a3fea8/addVideo
    Response: 201

    Case 2: Add a video to a videolist without logging in (Doesn't do # 1 Case 1 first):
    curl -i -H "Content-Type: application/json" -X POST -d '{"videoId":"2f050dce-aaf0-11ec-b658-525400a3fea8"}' -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/uruha_rushia/videolist/b21224ab-ac70-11ec-b658-525400a3fea8/addVideo
    Response: 401

    Case 3: Add a video to a videolist upon logged in, but with invalid videolistid (Do #1 Case 1 first):
    curl -i -H "Content-Type: application/json" -X POST -d '{"videoId":"574dc2c0-aaf7-11ec-b658-525400a3fea8"}' -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/gwargura/videolist/1/addVideo
    Response: 404

    Case 3: Add a video to a videolist upon logged in, but with invalid videoid (Do #1 Case 1 first):
    curl -i -H "Content-Type: application/json" -X POST -d '{"videoId":"1"}' -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/gwargura/videolist/7f70f65f-ac5f-11ec-b658-525400a3fea8/addVideo
    Response: 404


19. (AUTH REQUIRED) Delete a video from a videolist
    Endpoint: DELETE /user/{username}/videolist/{videolistid}/deleteVideo
    Case 1: Delete a video from a videolist upon logged in (Do #1 Case 1 first):
    curl -i -H "Content-Type: application/json" -X DELETE -d '{"videoId":"574dc2c0-aaf7-11ec-b658-525400a3fea8"}' -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/gwargura/videolist/7f70f65f-ac5f-11ec-b658-525400a3fea8/deleteVideo
    Response: 200

    Case 2: Delete a video from a videolist without logging in (Doesn't do #1 Case 1):
    curl -i -H "Content-Type: application/json" -X DELETE -d '{"videoId":"2f050dce-aaf0-11ec-b658-525400a3fea8"}' -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/uruha_rushia/videolist/b21224ab-ac70-11ec-b658-525400a3fea8/deleteVideo
    Response: 401

    Case 3: Delete a video from a videolist upon logged in, but with invalid videolistid (Do #1 Case 1 first):
    curl -i -H "Content-Type: application/json" -X DELETE -d '{"videoId":"574dc2c0-aaf7-11ec-b658-525400a3fea8"}' -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/gwargura/videolist/1/deleteVideo
    Response: 404

    Case 3: Delete a video from a videolist upon logged in, but with invalid videoid (Do #1 Case 1 first):
    curl -i -H "Content-Type: application/json" -X DELETE -d '{"videoId":"1"}' -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/gwargura/videolist/7f70f65f-ac5f-11ec-b658-525400a3fea8/deleteVideo
    Response: 404



