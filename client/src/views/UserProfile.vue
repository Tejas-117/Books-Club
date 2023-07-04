   <script setup>
   import { ref, watchEffect } from 'vue';
   import { useRoute, useRouter } from 'vue-router';
   import store from "../state/store";

   // import required assets
   import defaultProfile from '../assets/images/default-profile.png';
   import defaultCover from '../assets/images/default-cover.jpg';

   const router = useRouter();
   const route = useRoute();
   let userId = route.params.id;

   const user = ref(null);
   // used to switch between user uploaded books and user wishlist books.
   const bookDataToDisplay = ref(null);

   const allGenders = ['male', 'female', 'others', 'prefer not to say'];

   const loading = ref(false);
   const message = ref('');

   // function to fetch data from API.
   async function fetchData(){
      loading.value = true;
      message.value = 'Fetching data';
      
      const url = import.meta.env.VITE_BASE_API_URL + `users/${userId}`;
      const res = await fetch(url, {
         headers: {
            Authorization: `Bearer ${store.authTokens?.access}`
         }
      });
      
      loading.value = false;
      message.value = '';

      const { data } = await res.json();
      
      if(res.status === 404){
         message.value = "User not found";
      }
      else if (res.status >= 400){
         message.value = "Couldn't get user data";
      }
      else{
         user.value = data;

         // by default display books uploaded by the user.
         bookDataToDisplay.value = user.value.books;
      }
   }

   // on url params change
   watchEffect(() => {
      userId = route.params.id;
      fetchData();
   });

   // function to get `profile` and `cover` image from the data.
   function getUserImage(type){
      const defaultImages = {
         'cover': defaultCover,
         'profile': defaultProfile
      }

      const image = user.value.images?.filter(image => type === image.type);
      return image.length ? image[0].url : defaultImages[type]; 
   }

   // function to switch data in UI.
   function switchDataInBookColumn(event, type){
      // display appropriate books according to option selected by user.
      if(type === 'uploaded_books'){
         bookDataToDisplay.value = user.value.books;         
      }
      else{
         bookDataToDisplay.value = user.value.wishlist.map(wishlist => wishlist.book);
      }

      // toggle 'active' class to show which data is selected.
      const allDataToggleButtons = document.querySelectorAll('.toggle-data-button');
      allDataToggleButtons.forEach(btn => btn.classList.remove('active-data'));
      event.target.classList.add('active-data');
   }
</script>

<template>
   <div class="content-container profile-content-container">            
      <!-- loader and message elements -->
      <div v-if="loading || message" class="message-container">
         <span v-if="loading" class="loader"></span>
         <span v-if="message" class="message">{{ message }}</span>
      </div>
      
      <!-- pfp and bg pic starts here -->
      <div class="background-pic" v-if="user">
         <img class="background-pic-img" :src="getUserImage('cover')">

         <div class="profile-pic" v-if="user">
            <img class="profile-pic-img" :src="getUserImage('profile')">
         </div>
      </div>
      <!--pfp and bg pic ends here-->

      <!--body of the webpages begins here-->
      <div class="profile-master-container" v-if="user">
         <!--the div which holds all the other divs-->
         <!-- left side column   -->
         <div class="personal-info">

            <div class="name">{{ user.first_name + ' ' + user.last_name}}</div>
            <div class="bio">{{ user.bio }}</div>

            <div class="dob-gender">
               <div class="dob">
                  <img class="balloon-icon-pic" src="../assets/images/BalloonSymbol.svg">
                  Born {{ user.date_of_birth || 'unknown' }}
               </div>

               <div class="gender">
                  <img class="male-symbol-pic" src="../assets/images/MaleSymbol.png">
                  {{ allGenders[user.gender-1] }}
               </div>
            </div>

            <!-- genres and interests -->
            <div class="personal-genre-interest">
               <div class="interest-title">
                  Interests :
               </div>

               <div class="genre-container">
                  <span v-if="user.interests.length === 0">{{ 'Interests not shared by user' }}</span>
                  <div class="genre-box" v-for="interest in user.interests">{{ interest.text }}</div>
               </div>
            </div>

            <div class="user-action-buttons" v-if="user.id == store.user.user_id">
               <RouterLink :to="`/users/profile/${user.id}/edit`">
                  <button class="user-action-button">
                  Edit profile
                  </button>
               </RouterLink>
            </div>

            <div class="user-action-buttons" v-if="user.id == store.user.user_id">
               <RouterLink :to="`/offers`">
                  <button class="user-action-button">
                  View offers
                  </button>
               </RouterLink>
            </div>
         </div>

         <!-- right side column -->
         <div class="uploaded-books">
            <div class="book-uploads">
               <button class="toggle-data-button active-data" @click="switchDataInBookColumn($event, 'uploaded_books')">
                  Uploaded Books
               </button>

               <button class="toggle-data-button" @click="switchDataInBookColumn($event, 'wishlist')">
                  Wishlist
               </button>
            </div>

            <div class="user-books-status" v-if="bookDataToDisplay === user.books &&  user.books.length === 0">No books uploaded by user yet.</div>
            <div class="user-books-status" v-if="bookDataToDisplay !== user.books && user.wishlist.length === 0">No books in wishlist.</div>

            <div class="upload-preview" v-for="book in bookDataToDisplay" @click="router.push(`/books/${book.id}`)">               
               <img class="upload-preview-img" :src="`${book.images?.[0]?.url}`" >
               
               <div class="book-info">
                  <p class="book-name">{{ book.title }}</p>
                  <p class="Author">{{ book.author }}</p>

                  <div class="book-genre-holder">
                     <div class="book-genre-box" v-for="category in book.categories">{{ category.text }}</div>
                  </div>

                  <div class="upload-purpose">Put up for : 
                     <span v-if="book.for_sale && parseFloat(book.price) === 0">Give Away</span>
                     <span v-else-if="book.for_sale && parseFloat(book.price) > 0">Sale</span>
                     <span v-else>Trade</span>
                  </div>
               </div>   
            </div>  
         </div>   
      </div>
   </div>
</template>

<style>
   .profile-content-container{
      padding: 60px 0 0;
      position: relative;
      min-height: 100vh;
   }

   .profile-content-container .message-container{
      width: 300px;
      margin: 2rem auto;
   }

   .profile-content-container .loader{
      width: 70px;
      height: 70px;
   }  

   .profile-content-container  .message{
      font-size: 1rem;
      margin-top: 20px;
   }

   /* background picture and profile picture */
   .background-pic {
      height: 200px;
      display: flex;
      flex-shrink: 0;
   }

   .background-pic-img {
      min-width: 100%;
      height: 200px;
      object-fit: cover;
      object-position: 50% 50%;
   }

   .profile-pic {
      display: flex;
      background-color: rgb(162, 207, 207);
      height: 160px;
      width: 160px;
      position: absolute;
      left: 10vw;
      top: 160px;
      border-radius: 50%;
      border-style: solid;
      overflow: hidden;
   }

   .profile-pic-img {
      width: 100%;
   }

   /* body of the page below  */
   .profile-master-container {
      display: grid;
      grid-template-columns: 1fr 1.3fr;
      column-gap: 20px;
      padding: 2rem;
   }

   /* left side info */
   .personal-info {
      display: grid;
      padding: 40px;
      border-style: solid;
      border-top-width: 0.2px;
      border-bottom-width: 0.2px;
      border-color: var(--very-close-black);
      width: 90%;
      margin: 5rem auto 2rem;
   }

   .name {
      font-size: 44px;
      height: min-content;
   }

   .bio {
      margin: 20px 0px ;
      color: var(--very-close-black);
   }

   .options-img{
      width: 20px;
      height: 20px;
      position: absolute;
      top: 20px;
      right: 10px;
      z-index: 100;
      cursor: pointer;
   }

   .options-img img{
      width: 100%;
      height: 100%;
   }

   .username {
      font-size: 20px;
      color: var(--kinda-grey);
      padding: 0px;
      border: 0px;
      padding: 15px 0;
      width: max-content;
   }

   .dob-gender {
      display: flex;
      flex-direction: row;
   }

   .dob {
      display: flex;
      color: var(--kinda-grey);
      align-items: center;
   }

   .balloon-icon-pic {
      width: 30px;
      margin-right: 10px;
   }

   .male-symbol-pic {
      width: 30px;
      height: 30px;
      padding: 0px;
      margin-right: 10px;
   }

   .gender {
      display: flex;
      color: var(--kinda-grey);
      align-items: center;
      margin-left: 30px;
   }

   .interest-title {
      font-size: 24px;
      font-weight: 400;
      color:var(--very-close-black);
   }

   .genre-container {
      margin: 10px 0px 40px 0px;
      display: grid;
      grid-template-columns: repeat(auto-fit, clamp(100px, 180px, 200px));
      align-content: center;
      
   }

   .genre-box {
      text-align: center;
      padding: 2px 10px;
      background-color: var(--very-close-black);
      color: var(--kinda-white);
      border-radius: 15px;
      transition: color 0.5s;
      transition: background-color 0.5s;
      margin: 0px 5px 5px;
      opacity: 70%;
   }

   .user-action-buttons {
      display: flex;
      justify-content: center;
      width: 80%;
   }

   .user-action-button {
      height: 30px;
      border-radius: 15px;
      color: var(--kinda-white);
      font-weight: bold;
      width: 100%;
      border-style: solid;
      border-width: 2px;
      border-color: var(--kinda-white);
      background-color: var(--kinda-black);
      align-self: center;
      padding: 1px;
      margin: 4px 0px;
   }



   .user-action-buttons a{
      width: 100%;   
   }

   .user-action-button:hover {
      background-color: var(--kinda-white);
      color: var(--kinda-black);
      padding: 0px;
      border: 1px solid var(--kinda-black);
      cursor: pointer;
   }


   /* right side information  */
   .uploaded-books {
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
      border: 2px solid rgba(220, 220, 220, 0.721);
      border-radius: 10px;
      margin: 30px;
      height: 500px;
      overflow: hidden scroll;   
      position: relative;
   }

   .user-books-status{
      padding: 10px 20px;
   }

   .active-data{
      background-color: var(--kinda-black);
      color: var(--kinda-white);
   }

   .book-uploads {
      width: 100%;
      top: 0;
      left: 0;
      background-color: rgba(220, 220, 220, 0.8);
      text-align: center;
   }

   .toggle-data-button {
      font-size: 24px;
      width: 50%;
      padding: 14px;
      border-bottom: solid 4px var(--kinda-black);
   } 

   .upload-preview {
      display: grid;
      grid-template-columns: 1fr 3fr;
      margin-bottom: 1.5rem;   
      cursor: pointer;
      border: 2px solid rgba(220, 220, 220);
      padding: 20px;
      transition: all 0.3s linear;
   }

   .upload-preview-img {
      width: 130px;
      height: 150px;
      padding: 0px 10px;
      border-radius: 8px;
      align-self: center;
      margin-right: 10px;
   }

   .upload-preview:hover{
      box-shadow: 2px 2px 10px -1px rgb(0 0 0 / 45%);
   }

   .upload-preview:hover .book-name{
      text-decoration: underline;
   }

   .book-info {
      padding: 0px 10px 0px 0px;
      border-radius: 10px;
      position: relative;
      margin-left: 10px;
   }

   .book-name {
      padding: 10px 0px 2px 0px;
      font-size: 20px;
      font-weight: bold;
   }

   .Author {
      font-size: 14px;
      color: #a9a9a9;
      margin-bottom: 8px;
   }

   .book-genre-holder {
      display: grid;
      grid-template-columns: repeat(auto-fit, clamp(100px, 150px, 200px));
      width: 100%;
   }

   .book-genre-box {
      text-align: center;
      font-size: 14px;
      padding: 0px 10px;
      background-color: var(--very-close-black);
      color: var(--kinda-white);
      border-radius: 15px;
      transition: color 0.5s;
      transition: background-color 0.5s;
      margin: 5px;
      margin-left: 0;
   }

   .upload-purpose {
      margin: 5px 0;
      font-weight: bold;
      color:var(--kinda-grey);
   }


   /* Tablet view */
   @media screen and (max-width: 950px){
      .profile-master-container{
         grid-template-columns: 1fr;
         grid-template-rows: 1fr auto;
      }

      .personal-info{
         margin: 3rem auto;
         padding: 2rem 1rem;
      }

      .user-action-buttons{
         width: 100%;
      }

      .uploaded-books{
         margin: 0;
      }

      .genre-container {
         justify-content: center;
      }


   }

   /* Mobile view */
   @media screen and (max-width: 500px) {
      .profile-master-container{
         padding: 20px;
      }

      .profile-pic{
         width: 120px;
         height: 120px;
      }

      .personal-info{
         width: 100%;
         padding: 10px 0;
      }

      .name {
         font-size: 36px;
      }

      .uploaded-books{
         padding: 100px 1rem 1rem;
      }

      .upload-preview{
         text-align: center;
         justify-items: center;
         grid-template-columns: 1fr ;
      }

      .book-genre-holder{
         justify-content: center;
      }
   }
</style>