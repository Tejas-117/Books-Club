import { reactive } from "vue";
import jwt_decode from "jwt-decode";

const store = reactive({
   // store authentication tokens and current user.
   authTokens:  JSON.parse(localStorage.getItem('authTokens')),
   user: localStorage.getItem('authTokens') ? jwt_decode(localStorage.getItem('authTokens')) : null,

   // function to login user.
   login: async function(email, password){
      if (!email || !password){
         return { data: null, error: { message: 'Incomplete credentials' }};
      }
      
      const url = import.meta.env.VITE_BASE_API_URL + "users/token/";
      const res = await fetch(url, {
         method: "POST",
         headers: {
            "Content-Type": "application/json"
         },
         body: JSON.stringify({ email, password })
      });
      const data = await res.json();
      
      if (res.status === 200){
         // if login was successful, save authTokens and 'setUser' state.
         localStorage.setItem('authTokens', JSON.stringify(data));
         this.authTokens = data;
         this.user = jwt_decode(data.access);
         return { data: this.user, error: null };
      } else {
         return { data: null, error: { message: 'Login failed' }};         
      }
   },

   // function to logout user.
   logout: function(){
      // clear authTokens from state and localStorage.
      this.authTokens = null;
      this.user = null;
      localStorage.removeItem('authTokens');
   }, 

   // update authentication tokens before expiry
   updateAuthToken: async function(){
      const url = import.meta.env.VITE_BASE_API_URL + "users/token/refresh/";

      if(this.authTokens === null){
         return;
      }

      const res = await fetch(url, {
         method: "POST",
         headers: {
            "Content-Type": "application/json"
         },
         body: JSON.stringify({ refresh: this.authTokens.refresh })
      });
      const data = await res.json();

      // update state with new tokens.
      if (res.status === 200){
         // updata state with new data.
         localStorage.setItem('authTokens', JSON.stringify(data));
         this.authTokens = data;
         this.user = jwt_decode(data.access);
      } else {
         this.logout();
      }
   },

   // search text input by user.
   searchText: '',
})

export default store;