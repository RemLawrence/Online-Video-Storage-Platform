// register modal component
Vue.component("modal", {
  template: "#modal-template"
});

window.onload = function() {
  var app = new Vue({
      el: "#app",
    
      //------- data --------
      data: {
        serviceURL: "https://cs3103.cs.unb.ca:31308",
        alertDuration: 300,

        authenticated: false,
        ifSignUp: false,
        loggedIn: null,
        loginInput: {
          username: "",
          password: ""
        },
        loginSuccess: false,
        mustpresent: false,
        loginIncorrect: false,

        signupInput: {
          username: "",
          password: "",
          email: "",
          country: ""
        },
        signupSuccess: false,

        /* Control the result/warning shown by search User */
        searchedUsername: "",
        searchUserAlert: false,
        showSearchUser: false,
        searchedUser: "",
        showUserVideoLists: false,
        uservideolists: "",
        noUserVideoList: false,

        /* Control the result/warning shown by add own video */
        isAddVideo: false,
        ytbId: "",
        ytbIdValid: false,
        videoAddedSuccess: false,
        videoAddedFail: false,
        videoAddedDuplicate: false,
        showVideoImage: false,

        /* Control the result/warning shown by add own videolist */
        isAddVideoList: false,
        videoListInput: {
          title: "",
          description: ""
        },
        videoListAddedSuccess: false,
        videoListAddedFail: false,

        /* Control the result/warning shown by show own videos */
        showOwnVideos: false,
        videos: "",
        noVideo: false,

         /* Control the result/warning shown by show own videolists */
        showOwnVideoLists: false,
        videolists: "",
        noVideoList: false,
        videoId_addToList: "",
        videoListVideoAddedSuccess: false,
        videoListVideoAddedFail: false,

        showVideoInOwnVideoList: false,
        showVideoInOwnVideoListFail: false,
        videoInVideoLists: "",
        selectedVideoListId: "",

        showVideoInOtherVideoList: false,
        showVideoInOtherVideoListFail: false,
        videoInOtherVideoLists: "",
        selectedOtherVideoListId: ""
      },
      //------- lifecyle hooks --------
      // mounted: function() {
      //   axios
      //   .get(this.serviceURL+"/signin")
      //   .then(response => {
      //     if (response.data.status == "success") {
      //       this.authenticated = true;
      //       this.loggedIn = response.data.user_id;
      //     }
      //   })
      //   .catch(error => {
      //       this.authenticated = false;
      //       console.log(error);
      //   });
      // },
      //------- methods --------
      methods: {
        /* 1. POST: Set Session and return Cookie
        # Example curl command:
        # curl -i -H "Content-Type: application/json" -X POST -d '{"username": "gwargura", "password": "sh0rkAAAA++"}'
        #  	-c cookie-jar -k https://cs3103.cs.unb.ca:31308/signin */
        login() {
          this.mustpresent = false;
          this.loginIncorrect = false;
          //axios.defaults.withCredentials = true;
          if (this.loginInput.username != "" && this.loginInput.password != "") {
            axios
            .post(this.serviceURL+"/signin", {
                "username": this.loginInput.username,
                "password": this.loginInput.password
            })
            .then(response => {
                if (response.data.status == "success") {
                  this.loginSuccess = true;
                  this.authenticated = true;
                  this.loggedIn = response.data.user_id;
                }
                this.showVideo();
            })
            .catch(e => {
                this.loginInput.password = "";
                this.loginIncorrect = true;
            });
          } else {
            //alert("A username and password must be present");
            this.mustpresent = true;
          }
        },
        
        /* 3. DELETE: Check Cookie data with Session data (logout?)
        # Example curl command:
        # curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar
        #	-k https://cs3103.cs.unb.ca:61340/signin */
        logout() {
          axios
          .delete(this.serviceURL+"/signin")
          .then(response => {
              location.reload();
          })
          .catch(e => {
            console.log(e);
          });
        },

        signupbtn() {
          this.ifSignUp = true;
        },
        
        /* 4. POST: Create a new user
        # Example curl command:
        # curl -i -H "Content-Type: application/json" -X POST -d '{"username": "ameliawatson", "password": "ameame22", 
        # "email": "ame_holoEN@gmail.com", "country": "UK"}' -c cookie-jar -k https://cs3103.cs.unb.ca:31308/signup */
        signup() {
          if (this.signupInput.username != "" && this.signupInput.password != "" && this.signupInput.email != "") {
            if(this.signupInput.country != ""){
              axios
              .post(this.serviceURL+"/signup", {
                  "username": this.signupInput.username,
                  "password": this.signupInput.password,
                  "email": this.signupInput.email,
                  "country": this.signupInput.country
              })
              .then(response => {
                  if (response.data.status == "created") {
                    this.signupSuccess = true;
                    setTimeout(function() {
                      location.reload();
                    }, 3000);
                  }
              })
              .catch(e => {
                  this.signupInput.password = "";
                  console.log(e);
              });
            }
            else {
              axios
              .post(this.serviceURL+"/signup", {
                  "username": this.signupInput.username,
                  "password": this.signupInput.password,
                  "email": this.signupInput.email,
                  "country": ""
              })
              .then(response => {
                  if (response.data.status == "created") {
                    this.signupSuccess = true;
                    setTimeout(function() {
                      location.reload();
                    }, 3000);
                    this.signupSuccess = false;
                  }
              })
              .catch(e => {
                  this.signupInput.password = "";
                  console.log(e);
              });
            }
          } else {
            alert("A username, password and email must be presented");
          }
        },
        
        /* # 5. GET: Get a specific user via username
        # Example curl command:
        # curl -i -H "Content-Type: application/json" -X GET -b cookie-jar
        #	-k https://cs3103.cs.unb.ca:31308/ */
        searchUserWithName() {
          this.turnOffAddVideo();
          this.turnOffAddVideoList();
          this.turnOffGetVideo();
          this.turnOffGetVideoList();
          /* Once a new search, the user card needs to be cleared about the videolists */
          this.showUserVideoLists = false;
          this.noUserVideoList = false;

          $("#searchUser_form").submit(function(e) {
            e.preventDefault();
          });
          this.showSearchUser = false;
          this.searchUserAlert = false;
          if(this.searchedUsername != "") {
            axios
            .get(this.serviceURL+"/user/"+this.searchedUsername)
            .then(response => {
              if (response.data.status == "success") {
                this.showSearchUser = true;
                this.searchedUser = response.data.User;
              }
            })
            .catch(e => {
              this.searchUserAlert = true;
              console.log(e);
            });
        }
        else {
          this.searchUserAlert = true;
        }
      },

      gonnaaddvideo() {
        this.isAddVideo = true;
        this.showVideoImage = true;
        this.isAddVideoList = false;
        this.turnOffSearchUser();
        this.turnOffGetVideo();
        this.turnOffGetVideoList();
        this.turnOffAddVideoList();
      },

      /* 8. POST: Create a video for a specific user
        # Example curl command:
        # curl -i -H "Content-Type: application/json" -X POST -d '{"title":"minecraft chu", "size": 200}' 
        # -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/gwargura/video */
      addVideo() {
        this.videoAddedSuccess = false;
        this.videoAddedFail = false;
        this.videoAddedDuplicate = false;
        if (this.ytbId != "") {
          this.validVideoId(this.ytbId);
          if(this.ytbIdValid){
            axios
            .post(this.serviceURL + "/user/" + this.loginInput.username + "/video", {
                "id": this.ytbId,
                "size": 0
            })
            .then(response => {
                if (response.data.status == "created") {
                  this.videoAddedSuccess = true;
                }
            })
            .catch(e => {
                this.videoAddedDuplicate = true; 
            });
          } else {
          this.videoAddedFail = true; 
          }
        }
      },

      gonnaaddvideolist() {
        this.isAddVideoList = true;
        this.isAddVideo = false;
        this.turnOffAddVideo();
        this.turnOffSearchUser();
        this.turnOffGetVideo();
        this.turnOffGetVideoList();
      },

      /* 13. POST: Create a video list for a user
        # Example curl command: 
        # curl -i -H "Content-Type: application/json" -X POST -d 
        # '{"name": "holo_EN", "description": ""}' 
        # -b cookie-jar -k https://cs3103.cs.unb.ca:31308/user/gwargura/videolist */
      addVideoList() {
        this.videoListAddedSuccess = false;
        this.videoListAddedFail = false;
        if (this.videoListInput.title != "") {
          if(this.videoListInput.description != "") {
            axios
            .post(this.serviceURL + "/user/" + this.loginInput.username + "/videolist", {
                "name": this.videoListInput.title,
                "description": this.videoListInput.description
            })
            .then(response => {
                if (response.data.status == "created") {
                  this.videoListAddedSuccess = true;
                }
            })
            .catch(e => {
              this.videoListAddedFail = true;
            });
          } else {
            axios
            .post(this.serviceURL + "/user/" + this.loginInput.username + "/videolist", {
                "name": this.videoListInput.title,
                "description": ""
            })
            .then(response => {
                if (response.data.status == "created") {
                  this.videoListAddedSuccess = true;
                }
            })
            .catch(e => {
              this.videoListAddedFail = true;
            });
          }
        }
        else {
          this.videoListAddedFail = true;
        }
      },

      /* 9. GET: Get all the videos of a user
        # Example curl command:
        # curl -i -H "Content-Type: application/json" -X GET -b cookie-jar
        #	-k https://cs3103.cs.unb.ca:31308/user/uruha_rushia/video */
      showVideo() {
        this.turnOffAddVideo();
        this.turnOffAddVideoList();
        this.turnOffSearchUser();
        this.turnOffGetVideoList();
        this.showOwnVideoLists = false;
        this.noVideo = false;

        axios
        .get(this.serviceURL + "/user/" + this.loginInput.username + "/video")
        .then(response => {
          if (response.data.status == "success") {
            this.showOwnVideos = true;
            this.videos = response.data.Videos;
          }
        })
        .catch(e => {
            this.noVideo = true;
          });
      },

      /* 14. GET: Get all the videolists of a user
        # Example curl command:
        # curl -i -H "Content-Type: application/json" -X GET -b cookie-jar
        #	-k https://cs3103.cs.unb.ca:31308/user/gwargura/videolist */
      showVideoList() {
        this.turnOffAddVideo();
        this.turnOffAddVideoList();
        this.turnOffSearchUser();
        this.turnOffGetVideo();
        this.showOwnVideos = false;
        this.noVideoList = false;

        axios
        .get(this.serviceURL + "/user/" + this.loginInput.username + "/videolist")
        .then(response => {
          if (response.data.status == "success") {
            this.showOwnVideoLists = true;
            this.videolists = response.data.VideoLists;
          }
        })
        .catch(e => {
            this.noVideoList = true;
          });
      },

      /* 14. GET: Get all the videolists of a user
        # Example curl command:
        # curl -i -H "Content-Type: application/json" -X GET -b cookie-jar
        #	-k https://cs3103.cs.unb.ca:31308/user/gwargura/videolist */
      showUserVideoList() {
        this.turnOffAddVideo();
        this.turnOffAddVideoList();
        this.turnOffGetVideo();
        this.turnOffGetVideoList();
  
        axios
        .get(this.serviceURL + "/user/" + this.searchedUsername + "/videolist")
        .then(response => {
          if (response.data.status == "success") {
            this.showUserVideoLists = true;
            this.uservideolists = response.data.VideoLists;
          }
        })
        .catch(e => {
            this.noUserVideoList = true;
          });
      },

      /* 18. POST: Add a video to a videolist
        # Example curl command:
        # curl -i -H "Content-Type: application/json" -X POST -d 
        # '{"videoId": "574dc2c0-aaf7-11ec-b658-525400a3fea8"}' 
        # -b cookie-jar -k 
        # https://cs3103.cs.unb.ca:31308/user/gwargura/videolist/9313ec35-ac5c-11ec-b658-525400a3fea8/addVideo */
      addVideoToVideoList: function(id){
        this.videoListVideoAddedSuccess = false;
        this.videoListVideoAddedFail = false;
        /* Store this clicked videolist id */
        this.selectedVideoListId = id;

        if(this.videoId_addToList != "") {
          axios
          .post(this.serviceURL + "/user/" + this.loginInput.username + "/videolist/" + id + "/addVideo", {
              "videoId": this.videoId_addToList
          })
          .then(response => {
              if (response.data.status == "created") {
                  this.videoListVideoAddedSuccess = true;
              }
          })
          .catch(e => {
            this.videoListVideoAddedFail = true;
          });
        }
        else {
          this.videoListVideoAddedFail = true;
        }
      },

      /* 15. GET: Get the info of a videolist (videos, essentially)
        # Example curl command:
        # curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k 
        # https://cs3103.cs.unb.ca:31308/user/gwargura/videolist/81daada9-ac5f-11ec-b658-525400a3fea8 */
      showVideoInVideoList: function(id){
        this.videoListVideoAddedSuccess = false;
        this.videoListVideoAddedFail = false;
        
        this.showVideoInOwnVideoList = false;
        this.showVideoInOwnVideoListFail = false;
        this.videoInVideoLists = "";
        /* Store this clicked videolist id */
        this.selectedVideoListId = id;
        axios
        .get(this.serviceURL + "/user/" + this.loginInput.username + "/videolist/" + id)
        .then(response => {
          if (response.data.status == "success") {
            this.videoInVideoLists = response.data.VideoList;
            this.showVideoInOwnVideoList = true;
          }
        })
        .catch(e => {
          this.showVideoInOwnVideoListFail = true;
        });
      },

      /* 15. GET: Get the info of a videolist (videos, essentially)
        # Example curl command:
        # curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k 
        # https://cs3103.cs.unb.ca:31308/user/gwargura/videolist/81daada9-ac5f-11ec-b658-525400a3fea8 */
        showVideoInVideoList_Other: function(id){
          this.showVideoInOtherVideoList = false;
          this.showVideoInOtherVideoListFail = false;
          this.videoInOtherVideoLists = "";
          /* Store this clicked videolist id */
          this.selectedOtherVideoListId = id;
          axios
          .get(this.serviceURL + "/user/" + this.searchedUsername + "/videolist/" + id)
          .then(response => {
            if (response.data.status == "success") {
              this.videoInOtherVideoLists = response.data.VideoList;
              this.showVideoInOtherVideoList = true;
            }
          })
          .catch(e => {
            this.showVideoInOtherVideoListFail = true;
          });
        },

      /* Helper functions. Checks if the entered Youtube id is valid 
        Credits: https://gist.github.com/tonY1883/a3b85925081688de569b779b4657439b */
      validVideoId(id) {
        var img = document.getElementById('ytbImage'); 

        if (img.clientWidth === 120) {
          this.ytbIdValid = false;
        }
        else if(img.clientWidth === 320) {
          this.ytbIdValid = true;
        }
      },

      turnOffAddVideo() {
        this.isAddVideo = false;
        this.ytbId = "";
        this.videoAddedFail = false;
        this.videoAddedDuplicate = false;
      },
      turnOffAddVideoList() {
        this.isAddVideoList = false;
        this.videoListInput.description = "";
        this.videoListInput.title = "";
        this.videoListAddedFail = false;
        this.videoListAddedSuccess = false;
      },
      turnOffSearchUser() {
        this.showSearchUser = false;
        this.searchedUsername = "";
        this.searchUserAlert = false;

        this.showVideoInOtherVideoList = false;
        this.showVideoInOtherVideoListFail = false;
        this.videoInOtherVideoLists = "";
        this.selectedOtherVideoListId = "";
      },
      turnOffGetVideo() {
        this.showOwnVideos = false;
        this.noVideo = false;
      },
      turnOffGetVideoList() {
        this.noVideoList = false;
        this.showOwnVideoLists = false;

        this.videoId_addToList = "";
        this.videoListVideoAddedSuccess = false;
        this.videoListVideoAddedFail = false;

        this.showVideoInOwnVideoList = false;
        this.showVideoInOwnVideoListFail = false;
        this.videoInVideoLists = "";
        this.selectedVideoListId = "";
      }
    }
      //------- END methods --------
    
    });
    
}