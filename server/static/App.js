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
        //schoolsData: null,
        loggedIn: null,
        //editModal: false,
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

        searchedUsername: "",
        searchUserAlert: false,
        showSearchUser: false,
        searchedUser: ""
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
      }
          
    
        
      //   fetchSchools() {
      //     axios
      //     .get(this.serviceURL+"/schools")
      //     .then(response => {
      //         this.schoolsData = response.data.schools;
      //     })
      //     .catch(e => {
      //       alert("Unable to load the school data");
      //       console.log(e);
      //     });
      //   },
    
      //   deleteSchool(schoolId) {
      //     alert("This feature not available until YOUR version of schools.")
      //   },
    
    
      //   selectSchool(schoolId) {
      //       this.showModal();
      //     for (x in this.schoolsData) {
      //       if (this.schoolsData[x].schoolId == schoolId) {
      //         this.selectedSchool = this.schoolsData[x];
      //       }
      //     }
      //   },
    
    
      //   updateSchool(updatedSchool) {
      //     alert("This feature not available until YOUR version of schools.")
      //     // TODO: use axios.update to send the updated record to the service
      //   },
    
      //   showModal() {
      //     this.editModal = true;
      //   },
    
    
      //   hideModal() {
      //     this.editModal = false;
      //   }
    
      }
      //------- END methods --------
    
    });
    
}