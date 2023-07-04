<script setup>
   import { computed, onMounted, onUnmounted, ref } from "vue";
   import { RouterLink } from "vue-router";
   import store from "../state/store";

   // import required assets
   import defaultProfile from '../assets/images/default-profile.png';
   import defaultCover from '../assets/images/default-cover.jpg';

   const books = ref([]);
   const loading = ref(false);
   const message = ref('');

   const filteredBooks = computed(() => {
      const text = store.searchText;

      // if 'search text' is empty return all the books.
      if(!text){
         return books.value;
      };

      // filter books if 'search text' match book 'title', 'description', 'author'.
      const a = books.value.filter((book) => {
         return (
            book.title?.toLowerCase().includes(text) || 
            book.description?.toLowerCase().includes(text) ||
            book.author?.toLowerCase().includes(text)
         );
      });

      return a;
   })

   async function fetchData(){
      // notify user about fetching data.
      loading.value = true;
      message.value = 'Fetching data';

      const url = import.meta.env.VITE_BASE_API_URL + 'books/';
      const res = await fetch(url);
      const { data } = await res.json();
      
      loading.value = false;
      message.value = "";
      
      if(res.status === 200){
         books.value = data.books;

         if(!books.value.length){
            message.value = "No books found."
         }
      }
   }

   // reveal elements on scroll
   function revealBooks(){
      const allBooks = document.querySelectorAll('.reveal');
      
      for (let i = 0; i < allBooks.length; i++) {
         const windowHeight = window.innerHeight;
         const elementTop = allBooks[i].getBoundingClientRect().top;
         const elementVisible = 100;

         if (elementTop < (windowHeight - elementVisible)) {
            allBooks[i].classList.add("active");
         } else {
            allBooks[i].classList.remove("active");
         }
      }
   }

   onMounted(() => {
      // fetch data on mount.
      fetchData();
      window.addEventListener('scroll', revealBooks);
   });

   onUnmounted(() => {
      // remove listener on component 'unmount'.
      window.removeEventListener('scroll', revealBooks);    
   })

   // function to get profile image of the user from user object.
   function getUserProfile(user, type){
      const defaultImages = {
         'cover': defaultCover,
         'profile': defaultProfile
      }

      const image = user.images?.filter(image => type === image.type);
      return image.length ? image[0].url : defaultImages[type]; 
   }
</script>

<template>
   <div class="feeds-master-container">
      <div class="content-container feeds-container">

         <div class="heading">
            <div class="feeds-title-with-logo">
               <img src="../assets/images/LOGO-short-inverted.svg" alt="" class="all-books-title-icon">
               <h1 class="feeds-all-books-title">All books</h1>
            </div>
            <button class="feeds-filter-button"><img src="../assets/images/Filter-Icon.svg" alt="" class="feeds-filter-img"></button>
         </div>

         <!-- to show message and spinner while API calls -->
         <div v-if="message || loading" class="feeds-message-container message-container">
            <span v-if="loading" class="loader"></span>
            <span v-if="message" class="message">{{ message }}</span>
         </div>

         <!-- if books are found display all the books -->
         <div class="all-books-container">
            <div v-for="(book, idx) in filteredBooks" :key="book.id" :class="idx > 3 ? 'reveal' : ''">
               <div class="book-container">
                  <div class="feeds-card-uploader-menu-button">
                     <div class="feeds-pfp-name-date">
                        <img class="feeds-user-pfp" :src="getUserProfile(book.user, 'profile')" alt="">
                        <div class="feeds-username-date">
                           <RouterLink :to="`/users/profile/${book.user.id}`">
                              <h4 class="feeds-username">{{ book.user.first_name +' '+book.user.last_name }}</h4> 
                           </RouterLink>
                           <h5 class="feeds-upload-date">{{ book.created_on}} </h5>
                        </div>
                     </div>
                     <button class="feeds-menu-button"><img src="../assets/images/menu-icon.svg" alt="" class="feeds-menu-icon"></button>
                  </div>
                  <img class="feeds-uploaded-book-img" v-if="book.images.length > 0" :src="`${book.images[0].url}`" alt="">
                  <div class="feeds-book-title-author">
                     <h4 class="feeds-book-title">{{book.title}}</h4>
                  <p class="feeds-author-name" v-if="book.author"> {{ book.author }} </p>
                  </div>

                  <div class="feeds-buttons">
                     <RouterLink :to="`/books/${book.id}`">
                        <button class="feeds-check-details-button"> Check details </button>
                     </RouterLink>

                     <!-- Show bookmark icon only if the user is logged-in -->
                     <!-- <button v-if="store.user" class="feeds-bookmark">
                        <img src="../assets/images/Bookmark-Icon.svg" alt="" class="feeds-bookmark-icon">
                     </button> -->
                  </div>
               </div>
            </div>
         </div>
      </div>
   </div>
   
</template>

<style>

   :root {
      --primary-bold: #1a1a1a;
      --secondary-dull: #595959;
      --general-white: #f8f0f6;
   }

   * {
      color: var(--primary-bold);   
   }

   body{
      background-color: var(--general-white);
   }

   .feeds-master-container {
      /* border: solid 1px var(--secondary-dull); */
      background-image: url(../assets/images/feeds-background.jpg);
      background-size:cover;
      min-height: 100vh;
   }

   .content-container{
      padding-top: 80px;
   }

   .heading{
      display: flex;
      align-items: center;
      width: 86%;
      height: 50px;
      font-weight: bold;
      justify-content: space-between;
      padding: 0px 20px;
      background-color: var(--general-white);
      border-radius: 10px;
      box-shadow: -1px 3px 8px -1px rgba(0,0,0,0.8);
   }

   .feeds-title-with-logo {
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: center;

   }

   .feeds-all-books-title {
      font-size: 24px;

   }

   .all-books-title-icon {
      display : none;
      height: 24px;
      padding-right: 10px;
   }

   .feeds-filter-button {
      height: 30px;
      width: 30px;
      padding: 0px;
      margin: 0px;
      border-radius: 0px;
      align-items: center;
      justify-content: center;
      transition: all 0.35s;
   }

   .feeds-filter-button:hover {
      background-color: #1a1a1a;
      cursor: pointer;
   }
   
   .feeds-filter-img {
      height: 30px;
      width: 30px;
   }

   .feeds-container{
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
   }

   .feeds-message-container{
      max-width: 300px;
   }

   .feeds-message-container .loader{
      width: 70px;
      height: 70px;
   }  

   .feeds-message-container  .message{
      font-size: 1rem;
      margin-top: 20px;
   }

   /* Books container styling */
   .all-books-container{
      width: 90%;
      max-width: 1600px;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      grid-auto-rows: auto;
      grid-gap: 20px;
      justify-content: center;
      align-content: center;
      padding: 20px 30px;
      
   }

   .all-books-container > div{
      border-radius: 6px;
      padding: 10px 10px;
      box-shadow: -1px 3px 8px -1px rgba(0,0,0,0.5);
      background-color: var(--general-white);
   }
   
   .all-books-container > div:hover{
      box-shadow: -1px 3px 11px 3px rgba(145, 138, 138, 0.35);
   }

   .book-container{
      height: 100%;
      text-decoration: none;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
   }

   .feeds-pfp-name-date {
      display: flex;
      flex-direction: row;
   }
   .feeds-card-uploader-menu-button {
      display: flex;
      width: 100%;
      align-items: center;
      justify-content: space-between;
      padding:0px 4px;
   }

   .feeds-user-pfp {
      display:flex;
      max-width: 30px;
      max-height: 30px;
      border-radius: 15px;
      margin: 0px 10px 0px 0px;
   }

   .feeds-username-date {
      display: flex;
      flex-direction: column;
      justify-content: center;
   }

   .feeds-username {
      font-size: 12px;
      font-weight: 1000;
      height: 16px;
      
   }

   .feeds-upload-date {
      font-size: 9px;
      font-weight: 800;
      color: var(--secondary-dull);
   }

   .feeds-menu-button {
      height: 30px;
      width: 30px;
      padding: none;
      background-color: transparent;
      justify-self: flex-end;
   }

   .book-container h2, .book-container span{
      font-weight: bold;
      text-decoration: underline;
   }

   .feeds-uploaded-book-img {
      display: grid;
      height: 280px;
      margin: 10px 0px;
      border-radius: 4px;
      object-fit: cover;
      object-position: 50% 50%   ;
   }

   .feeds-book-title-author {
      margin: 10px 0px;
      justify-content: center;
   }

   .feeds-book-title {
      font-size: 14px;
      font-weight: 1000;
      margin: 0px 4px;
   }

   .feeds-author-name {
      font-size: 10px;
      font-weight: 800;
      margin: 0px 4px;
      color: var(--secondary-dull);
   }

   .feeds-buttons {
      margin: 0px 4px 0px 4px;
      display: flex;
      justify-content: space-between;
   }

   .feeds-check-details-button { 
      border: 1.8px solid var(--primary-bold);
      background-color: transparent;
      border-radius: 4px;
      font-size: 10px;
      font-weight: 1000;
      padding: 2px 6px;
      align-items: center;
      height: 26px;
      transition: all 0.35s;
   }

   .feeds-check-details-button:hover {
      background-color: var(--primary-bold);
      color:var(--general-white);
      cursor: pointer;
   }

   .feeds-bookmark {
      height: 26px;
      width: 26px;
      padding: 0px; 
      background-color:transparent;
      justify-self: flex-end;
      border-radius: 6px;
      transition: all 0.35s;
      
   }

   .feeds-bookmark:hover {
      cursor: pointer;
   }

   .feeds-bookmark-icon {
      height : 26px;
      width : 26px;
      border-radius: 50%;
   }

   .blue-text{
      color: rgb(71, 137, 223);
      text-decoration: none !important;
   }

   .reveal{
      position: relative;
      transform: translateY(100px);
      opacity: 0;
      transition: 1.4s all ease;
   }
   
   .active{
      transform: translateY(0);
      opacity: 1;
   }

   @media screen and (max-width: 310px) {

      .all-books-container{
         grid-template-columns: repeat(auto-fit, 90vw);
      }

      .book-container img{
         width: 100%;
         margin: 1rem 0;
      }
   }
</style>
