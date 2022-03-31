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
        authenticated: false,
        ifSignUp: false,
        //schoolsData: null,
        loggedIn: null,
        //editModal: false,
        loginInput: {
          username: "",
          password: ""
        },
        signupInput: {
          username: "",
          password: "",
          email: "",
          country: ""
        }
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
        login() {
          //axios.defaults.withCredentials = true;
          if (this.loginInput.username != "" && this.loginInput.password != "") {
            axios
            .post(this.serviceURL+"/signin", {
                "username": this.loginInput.username,
                "password": this.loginInput.password
            })
            .then(response => {
                if (response.data.status == "success") {
                  this.authenticated = true;
                  this.loggedIn = response.data.user_id;
                }
            })
            .catch(e => {
                this.loginInput.password = "";
                console.log(e);
            });
          } else {
            alert("A username and password must be present");
          }
        },
    
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