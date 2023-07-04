<script setup>
import { onMounted, ref } from 'vue';
   import { useRoute, useRouter } from 'vue-router';
   import Comment from "../components/Comment.vue";
   import store from "../state/store";

   // import required assets
   import defaultProfile from '../assets/images/default-profile.png';
   import defaultCover from '../assets/images/default-cover.jpg';

   const route = useRoute();
   const router = useRouter();

   // get params from url
   const bookId = route.params.id;

   // store data from API
   const book = ref(null);

   // users' book which they have uploaded for 'exchange'
   const userBookUploads = ref([]);
   
   // store input values.
   const commentText = ref('');

   // util state.
   const imageRefs = ref(null);
   const loading = ref(false);
   const message = ref(' ');

   const BASE_API_URL = import.meta.env.VITE_BASE_API_URL;

   // function to fetch data from the API
   async function fetchData(){
      loading.value = true;
      message.value = "Fetching data";

      const url = BASE_API_URL + `books/${bookId}`;
      const res = await fetch(url, {
         method: 'GET',
         headers: {
            Authorization: `Bearer ${store.authTokens.access}`
         }
      });
      const { data, error } = await res.json();

      loading.value = false;
      message.value = '';

      if(res.status === 200){
         book.value = data.book;
      } else {
         message.value = error.message;
      }
   }
   
   // fetch data on component mount.
   onMounted(() => {
      if(!store.user){
         return;
      }

      fetchData().then(async () => {
         // show default image in carousel.
         changeImage();

         // get users' books
         const url = BASE_API_URL + `books/?user=true`;
         const res = await fetch(url, {
            headers: {
               Authorization: `Bearer ${store.authTokens.access}`
            }
         })
         
         if(res.status === 200){
            const { data } = await res.json();
            userBookUploads.value = data.books;
         }
      });
   })

   ///////////////////////// 'book-post' functions //////////////////////////////
   // function to delete post
   async function deletePost(){
      loading.value = true;
      message.value = 'Deleting book.'
      window.scrollTo(0, 0); // scroll to top of the page, to show message

      const url = BASE_API_URL + `books/${bookId}/`;
      const res = await fetch(url, {
         method: 'DELETE',
         headers: {
            Authorization: `Bearer ${store.authTokens.access}`
         }
      });

      loading.value = false;
      message.value = '';

      if(res.status === 200){
         message.value = 'Deleted the book.';
         setTimeout(() => {
               router.push('/feeds')
         }, 2000);
      }
   }

   //////////////////////////// 'comment' functions /////////////////////////////
   // function to post a comment.
   async function postComment(){
      message.value = '';

      if(store.user == null){
         window.scrollTo(0, 0);
         message.value = 'Login to post comment';
         return;
      }

      loading.value = true;
      message.value = 'Posting comment';

      const url = BASE_API_URL + `books/${book.value.id}/comments/`;
      const res = await fetch(url, {
         "method": 'POST',
         "headers": {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${store.authTokens.access}`
         },
         body: JSON.stringify({ comment: commentText.value })
      })

      loading.value = false;
      message.value = '';
      
      const { data, error } = await res.json();

      // show appropriate message after posting comment;
      window.scrollTo(0, 0);
      if(res.status === 200){
         fetchData();
         message.value= "Successfully posted comment";
         commentText.value = '';
      }
      else{
         message.value = error?.message;
      }
   }

   // function to delete a comment.
   async function deleteComment(comment){
      if(store?.user?.user_id !== comment.user.id){
         return;
      }

      const url = BASE_API_URL + `books/${book.value.id}/comments/${comment.id}/`;
      const res = await fetch(url, {
         method: 'DELETE',
         headers: {
            Authorization: `Bearer ${store.authTokens.access}`
         }
      });
      
      // if comment is successfully deleted, update the UI
      if(res.status === 200){
         const data = await res.json();

         const commentIdx = book.value.comments.findIndex((cmt) => cmt.id === comment.id);
         book.value.comments.splice(commentIdx, 1);
      }
      else{
         window.scrollTo(0);
         message.value = "Couldn't delete comment";
      }
   }

   /////////////////////////////// 'offer' functions //////////////////////////////
   async function submitOffer(){
      window.scrollTo(0, 0); // scroll to top and display the message.
      
      // construct payload to send to API
      const payload = {
         posted_book: bookId,
         description: document.querySelector('.offer-message').value
      };

      // if book is for sale, add these options
      if(book.value.for_sale){
         payload['for_purchase'] = true;
         payload['price'] = parseInt(book.value.price);
      }  
      // if book is for exchange, add these options
      else{
         // get selected book for exchange id.
         const selectedOption = document.querySelector('.exchange-book-listbox').value;

         // if no book is selected return.
         if(!selectedOption){
            message.value = 'Select a book to exchange.'
            return;
         }
         payload['exchange_book'] = selectedOption;
      }

      loading.value = true;
      message.value = 'Submitting offer';

      // submit offer data;
      const url = BASE_API_URL + `offers/`;
      const res = await fetch(url, {
         method: 'POST',
         headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${store.authTokens.access}`
         },
         body: JSON.stringify({ ...payload })
      });

      const { data, error } = await res.json();

      loading.value = false;
      message.value = '';

      
      if(res.status === 200){
         message.value = data.message;
      }
      else{
         message.value = error.message;
      }
   }

   //////////////////////// 'wishlist' functions //////////////////////////////////
   // function to update wishlist of the user
   async function updateWishlist(){
      loading.value = true;
      message.value = 'Updating wishlist...';
      window.scrollTo(0, 0);

      const url = BASE_API_URL + `books/${book.value.id}/wishlist`;
      const res = await fetch(url, {
         headers: {
            Authorization: `Bearer ${store.authTokens.access}`
         }
      });
      const { data } = await res.json();
      
      loading.value = false;
      message.value = ''
      
      if(res.status === 200){
         book.value.in_wishlist = !book.value.in_wishlist;
      }
      else{
         message.value = "Couldn't update wishlist!!"
      }
   }
   
   ///////////////////////// util functions ////////////////////////////////////
   // function to get `profile` and `cover` image from the data.
   function getUserImage(type){
      const defaultImages = {
         'cover': defaultCover,
         'profile': defaultProfile
      }

      const image = book.value.user.images?.filter(image => type === image.type);
      return image.length ? image[0].url : defaultImages[type]; 
   }

   // function to change image inside carousel.
   let currIndex = 0;
   function changeImage(movement = 0){
      if(!imageRefs.value) return;

      const allImages = Array.from(imageRefs.value);
      const totalNumOfImages = allImages.length;
      
      // if movement = 1: move right
      if((movement === 1)){
         currIndex = (currIndex+1) % (totalNumOfImages);         
         goToImage(currIndex);
      }
      // if movement = -1: move left
      else if((movement === -1)){
         currIndex = (currIndex > 0) ? currIndex-1 : totalNumOfImages-1;
         goToImage(currIndex);
      }
      else{
         currIndex = Math.floor(totalNumOfImages/2); // middle image by default.
         goToImage(currIndex);
      }

      function goToImage(image){
         allImages.forEach((img, idx) => {
            // show the current image.
            if(idx === image){
               img.style.opacity = 1;
            } 
            else{
               img.style.opacity = 0;
            }

            img.style.transform = `translateX(${100 * (idx - image)}%))`;
         })
      }
   }

   // function to toggle display of other containers (elements)
   function revealContainer(containerClass){
      const containerEle = document.querySelector(`.${containerClass}`);
      
      if(!containerEle){
         return;
      }
      
      if(containerEle.style.display === 'flex'){
         containerEle.style.display = 'none';
      } else {
         containerEle.style.display = 'flex';
      }
   }
</script>

<template>
   <div class="post-master-container">
      <div class="content-container post-content-container">
         
         <!-- loader and message elements -->
         <div class="message-container">
            <span v-if="loading" class="loader"></span>
            <span v-if="message" class="message">{{ message }}</span>
         </div>

         <div class="post-container" v-if="book">
            <!-- uploader information : kind of a header -->
            <div class="post-header">
               <div class="post-uploader-pfp-name-date" >
                  <img class="post-uploader-pfp" :src="getUserImage('profile')">
                  <div class="post-uploader-name-date">
                     <RouterLink :to="`/users/profile/${book.user.id}`">
                        <h4 class="post-uploader-name">{{book.user.first_name + ' ' + book.user.last_name}}</h4>
                     </RouterLink>
                     <h5 class="post-upload-date">{{book.created_on}}</h5>    
                  </div>
               </div>

               <div class="post-upload-purpose-container">
                  <h4 class="post-upload-purpose-title">Upload Purpose :</h4>
                  <h4 class="post-upload-purpose">
                     {{ book.for_sale ? (book.price > 0) ? 'Sell' : 'Give away' : 'Exchange' }}
                  </h4>
               </div>
            </div>

            <div class="post-information-container">     
               <!-- left column of the information container  -->
               <!-- Image carousel of the book -->
               <div class="post-book-image-carousel">
                     <img
                        v-if="book.images.length > 1" 
                        @click="() => changeImage(-1)"
                        class="arrow left-arrow"
                        src="../assets/images/arrow-symbol.png"
                        alt="previous image"
                     >
                        
                     <div class="post-book-image" v-for="image in book.images" ref="imageRefs">
                        <img :src="image.url" alt="">
                     </div>
                        
                     <img 
                        v-if="book.images.length > 1"
                        @click="() => changeImage(1)"
                        class="arrow right-arrow" 
                        src="../assets/images/arrow-symbol.png" 
                        alt="next image"
                     >
                  </div>


               <div class="post-text-info">
                  <div class="post-top-information">
                     <div class="book-title">
                        <h2 class="post-book-name">{{ book.title }}</h2>
                        <h3 class="post-book-author">{{ book.author }}</h3>
                     </div>

                     <!-- All categories of the book -->
                     <div class="categories">
                        <div class="category" v-for="category in book.categories">
                           {{ category.text }}
                        </div>
                     </div>

                     <!-- Description of the book -->
                     <p class="post-book-description">&emsp; &emsp;{{book.description }}</p>
                  </div>


                  <div class="post-bottom-buttons">

                     <div class="post-operation-comments-button"> 
                        <div class="post-comment-count">{{book.comments.length}}</div>
                        <button class="operation-button" @click="revealContainer('comments-container')">
                           <img class="post-bookmark-icon" src="../assets/images/comments-icon.svg">
                        </button>
                        <div class="post-comments-hover-message">
                           Comments
                        </div>
                     </div>

                        
                     <div v-if="store.user?.user_id != book.user.id" class="post-operation-bookmark-button"> 
                        <button class="operation-button" @click="updateWishlist">
                           <img class="post-bookmark-icon" src="../assets/images/Bookmark-Icon.svg" :style="{ background: book.in_wishlist ? 'black' : '' , borderRadius: '50%' }">
                           <div class="post-bookmark-hover-message">
                              Bookmark
                           </div>
                        </button>
                     </div>

                     <div v-if="store.user?.user_id == book.user.id" class="post-operation-edit-button"> 
                        <button class="operation-button" @click="router.push(`/books/${bookId}/edit`)">
                           <img class="post-bookmark-icon" src="../assets/images/edit-icon.svg">
                           <div class="post-edit-hover-message">
                              Edit post
                           </div>
                        </button>
                     </div>

                     <div v-if="store.user?.user_id != book.user.id" class="post-operation-offer-button"> 
                        <button class="operation-button" @click="revealContainer('make-an-offer')">
                           <img class="post-bookmark-icon" src="../assets/images/offers-icon.svg">
                           <div class="post-offer-hover-message">
                              Make an Offer
                           </div>
                        </button>
                     </div>

                     <div v-if="store.user?.user_id == book.user.id" class="post-operation-delete-button"> 
                        <button class="operation-button" @click="deletePost">
                           <img class="post-bookmark-icon" src="../assets/images/delete-icon.svg">
                           <div class="post-delete-hover-message">
                              Delete post
                           </div>
                        </button>
                     </div>

                  </div>
               </div>
            </div>

            <!-- categories container for tablet and mobile view -->
            <div class="mobile-tablet-categories">
               <div class="category" v-for="category in book.categories">
                  {{ category.text }}
               </div>
            </div>


            <!-- comments section  -->

            <div class="comments-container" id="postCommentDisplay">
               <!-- Form to post comment -->
               <h3 class="post-comments-label">{{book.comments.length}} comment{{ book.comments.length > 1 ? 's' : '' }}</h3>
               <div class="post-add-comments">
                  <img class="post-user-pfp" :src="store.user?.profile || defaultProfile">
                  <form class="comment-form" @submit.prevent="postComment">
                     <div class="post-comment-input-submit">
                        <input  class="post-comment-input" v-model="commentText" type="text" placeholder="Add a comment..." required>
                        <div class="post-comment-submit-container">
                           <button type="submit" class="post-comment-btn">Submit</button>
                        </div>
                     </div>
                  </form>
               </div>

               <!-- Display all comments -->
                  <div class="comments">
                     <span v-if="book?.comments?.length === 0">No comments</span>

                     <Comment class="post-comments-card"
                        v-for="comment in book.comments" 
                        :key="book.comments.id" 
                        :comment="comment"
                        :deleteComment="deleteComment" 
                     />
                  </div>  
            </div>


            <!-- make an offer section  -->

            <div class="make-an-offer">
                  <h3 class="post-offer-details-title">
                     Offer type : {{ book.for_sale ? (book.price > 0) ? 'Sell' : 'Give away' : 'Exchange' }}
                  </h3>
                  

               <div class="make-an-offer-container">
                  <!-- display this if the upload purpose of the book is exchange  -->
                  <div v-if="!book.for_sale" :style="{display: 'flex', flexDirection: 'column', width: '100%'}">
                     <div class="offers-lhs-exchange">
                        <div class="post-uploaded-book-list">
                           <span class="select-book-title">Select a book to offer </span> 
                           <select name="book-list" class="exchange-book-listbox">
                              <option value="" selected disaled>None</option>
                              <option v-for="upload in userBookUploads" :value="upload.id" class="offer-option"> {{ upload.title }} </option>
                           </select>
                        </div>
                     </div>

                     <div class="offers-lhs-giveaway">
                        <h3>
                        <i class="giveaway-message">
                           This book has been uploaded for exchange.
                           <br>The uploader will contact you after submitting request.
                        </i> 
                        </h3>
                     </div>
                  </div>

                  <div v-if="book.for_sale" class="offers-lhs-sales">
                        <h5 class="price-title">
                           Price quoted on this book : 
                        </h5>
                        <h4 class="book-quoted-price">
                           {{ '₹ ' + book.price }}
                        </h4>
                  </div>

                  <div class="exchange-message-rhs-container">
                     <h4 class="offer-message-title">
                        Add a small message for your request 
                     </h4>
                     <textarea class="offer-message" type="text" required rows="2" cols="30" maxlength="300" > </textarea>
                     <div class="request-button-container">
                        <button @click="submitOffer" class="make-request-btn">
                           Submit offer
                        </button>
                     </div>
                  </div>
               </div>
            </div>
         </div>
      </div>
   </div>
</template>

<style>

/* for the options hanging outside the card */
   .button-title {
      font-size: 16px;
      font-weight: 600;
      padding: 0px 10px;
   }

   .post-master-container {
      display: flex ;
      align-items: center;
      justify-content: center;
      background-image: url(../assets/images/feeds-background.jpg) ;
      background-size: cover;
      min-height: 100vh;
   }


   .post-content-container .message-container{
      width: 200px;
      margin: 2rem auto;
   }

   .post-container{
      z-index: 10;
      position: relative;
      padding: 10px 20px;
      width: 90vw;
      display: flex;
      flex-direction: column;
      justify-content: center;
      border: solid 0.2px var(--silver);
      border-radius: 10px;
      margin: 100px 0px;
      background-color: var(--kinda-white);
      box-shadow: -1px 3px 11px 3px rgba(110, 107, 107, 0.35);
      margin: 0 0 100px;
      max-width: 1200px;
   }

   .post-header {
      display: flex; 
      flex-direction: row;
      justify-content: space-between;
      padding: 10px 0px 20px 0px;
   }

   .post-uploader-pfp-name-date {
      display: flex;
      flex-direction: row;
   }

   .post-uploader-pfp {
      width: 50px;
      height: 50px;
      border-radius: 2rem;
      margin: 0px 16px 0px 8px;
   }

   .post-uploader-name-date {
      display: flex;
      flex-direction: column;
      justify-content: center;
   }

   .post-uploader-name {
      font-size: 18px;
      height: 24px;
      font-weight: 900;
   }

   .post-upload-date {
      font-size: 10px;
      color: var(--secondary-dull);
   }

   .post-upload-purpose-container {
      display : flex;
      flex-direction: column;
      justify-content: center;
      align-items: flex-start;
      justify-self: flex-end;
      padding: 0px 0px 0px 10px;
      border-left: solid 0.2px var(--silver);
      margin: 0 8px;
   }

   .post-upload-purpose-title {
      font-size: 11px;
      color: var(--secondary-dull);
      height: 11px;
   }

   .post-upload-purpose {
      font-size: 18px;
      font-weight: 1000;
   }


   .post-information-container {
      display: grid;
      grid-template-columns: 3fr 5fr;
      padding: 26px 10px;
      border-top: solid 0.2px var(--silver);
      
   }
   
   /* image carousel */
   .post-book-image-carousel{      
      position: relative;
      width: 360px;
      height: 500px;
      box-shadow: -1px 3px 8px -1px rgba(0,0,0,0.5);
      margin: 0 auto;
      border-radius: 6px;
      transition: opacity 0.3s linear;
      overflow: hidden;
   }
   
   .post-book-image{
      position: absolute;
      top: 0;
      left: 0;
      width: 360px;
      height: 500px;
      object-fit:contain;
      object-position: 50% 50%;
      border-radius: 6px;     
      transition: transform 0.4s ease-in, opacity 0.7s ease-in;
   }
   
   .post-book-image img{
      width: 360px;
      height: 500px  ;
      border-radius: 6px;
      object-fit: cover;
      object-position: 50% 50%;
   }

   .post-book-image-carousel:hover .arrow{
      opacity: 1;
   }

   .arrow{
      opacity: 0;
      position: absolute;
      top: 50%;
      width: 40px;
      height: 40px;
      z-index: 100;
      transition: opacity 0.5s ease-in;
      border-radius: 50%;
      padding: 5px;
      overflow: hidden;
   }

   .left-arrow{
      left: 0%;
   }

   .right-arrow{
      right: 0%;
      transform: rotateY(180deg);
   }

   .post-text-info {
      display: flex;
      flex-direction: column;
      padding: 8px 0px 0px 20px;
      justify-content: space-between;
   }

   .post-book-name {
      font-size: 32px;
      font-weight: bolder;
   }

   .post-book-author {
      color: var(--secondary-dull);
      padding: 0px 4px; 
      font-size: 25px;
   }

   .post-book-description {
      margin: 40px 0px;
      display: flex;
   }

   .post-bottom-buttons {
      display: flex;
      flex-direction: row;
      justify-content: flex-end;
   }

   .operation-button {
      display: flex;
      align-items: center;
      cursor: pointer;
      height: 30px;
      width: 30px;
      padding: 0px;
      justify-content: center;
   }

   .post-bookmark-icon {
      width: 28px;
      height: 28px;
   }



   
.post-operation-delete-button {
      position: relative;
      padding:none;
      margin-left:5px ;
      height: 40px;
      width:40px; 
      display: flex;
      align-items: center;
      justify-content: center;
      /* overflow: hidden; */
      background-color: var(--kinda-white);
      border-radius: 8px;
      border: solid 2px var(--kinda-black);
   }

   .post-delete-hover-message {
      width:max-content;
      position: absolute;
      bottom: -24px;
      font-size: 10px;
      background-color: var(--silver);
      padding: 2px 4px;
      border-radius:4px ;
      font-weight: 600;
      opacity: 0;
      transition: all 0.35s;
      pointer-events: none;
   }

   .post-operation-delete-button:hover .post-delete-hover-message{
      opacity: 1;
   }



.post-operation-edit-button {
      position: relative;
      padding:none;
      margin: 0px 5px ;
      height: 40px;
      width:40px; 
      display: flex;
      align-items: center;
      justify-content: center;
      background-color: var(--kinda-white);
      border-radius: 8px;
      border: solid 2px var(--kinda-black);
   }

   .post-edit-hover-message {
      width: max-content;
      position: absolute;
      bottom: -24px;
      font-size: 10px;
      background-color: var(--silver);
      padding: 2px 4px;
      border-radius:4px ;
      font-weight: 600;
      opacity: 0;
      transition: all 0.35s;
      pointer-events: none;
   }

   .post-operation-edit-button:hover .post-edit-hover-message{
      opacity: 1;
   }



   .post-operation-comments-button {
      position: relative;
      padding:none;
      margin: 0px 5px ;
      height: 40px;
      width:40px; 
      display: flex;
      align-items: center;
      justify-content: center;
      background-color: var(--kinda-white);
      border-radius: 8px;
      border: solid 2px var(--kinda-black);
   }

   .post-comments-hover-message {
      width:max-content;
      position: absolute;
      bottom: -24px;
      font-size: 10px;
      background-color: var(--silver);
      padding: 2px 4px;
      border-radius:4px ;
      font-weight: 600;
      opacity: 0;
      transition: all 0.35s;
      pointer-events: none;
   }

   .post-operation-comments-button:hover .post-comments-hover-message{
      opacity: 1;
   }

   .post-comment-count {
      position:absolute;
      right:-6px;
      top:-6px;
      font-size: 10px;
      font-weight: 600;
      width: 16px;
      height: 16px;
      padding: 0px;
      display: flex;
      justify-content: center;
      align-items: center;
      color: var(--kinda-white);
      background-color: var(--kinda-black);
      border-radius: 50%;
   }


   .post-operation-bookmark-button {
      position: relative;
      padding:none;
      margin: 0px 5px ;
      height: 40px;
      width:40px; 
      display: flex;
      align-items: center;
      justify-content: center;
      background-color: var(--kinda-white);
      border-radius: 8px;
      border: solid 2px var(--kinda-black);
   }

   .post-bookmark-hover-message {
      width: max-content;
      position: absolute;
      bottom: -24px;
      font-size: 10px;
      background-color: var(--silver);
      padding: 2px 4px;
      border-radius:4px ;
      font-weight: 600;
      opacity: 0;
      transition: all 0.35s;
      pointer-events: none;
   }

   .post-operation-bookmark-button:hover .post-bookmark-hover-message{
      opacity: 1;
   }



   .post-operation-offer-button {
      position: relative;
      padding:none;
      margin-left:5px ;
      height: 40px;
      width:40px; 
      display: flex;
      align-items: center;
      justify-content: center;
      background-color: var(--kinda-white);
      border-radius: 8px;
      border: solid 2px var(--kinda-black);
   }

   .post-offer-hover-message {
      width:max-content;
      position: absolute;
      bottom: -24px;
      font-size: 10px;
      background-color: var(--silver);
      padding: 2px 4px;
      border-radius:4px ;
      font-weight: 600;
      opacity: 0;
      transition: all 0.35s;
      pointer-events: none;
   }

   .post-operation-offer-button:hover .post-offer-hover-message{
      opacity: 1;
   }

   .post-action-button {
      padding:none;
      margin-left:5px ;
      height: 40px;
      width:40px; 
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      background-color: var(--kinda-white);
      border-radius: 8px;
      border: solid 2px var(--kinda-black);
   }

   .post-action-button:hover {
      background-color: var(--kinda-black);
      color:var(--kinda-white);
   }

   .post-rhs-buttons {
      display: flex;
   }


   .post-comment-button {
      background-color: transparent;
      height: 30px;
      width: 30px;
      margin: 0;
      padding: 0;
      transition: all 0.35s ;
      border-radius: 6px;
      margin: 0px 10px;
      overflow: hidden;
   }

   .post-comment-button:hover {
      background-color: var(--kinda-black);
      box-shadow: -1px 3px 8px -1px rgba(0,0,0,0.2);
   }

   .post-comment-icon {
      width: 36px;
      height: 36px;
   }

   .post-bookmark-button {
      background-color: transparent;
      height: 36px;
      width: 36px;
      margin: 0;
      padding: 0;
      transition: all 0.35s ;
      border-radius: 6px;
      overflow: hidden;
   }

   .post-bookmark-button:hover {
      background-color: var(--kinda-black);
      box-shadow: -1px 3px 8px -1px rgba(0,0,0,0.2);
   }



   /* Comments container styling */
   .comments-container{
      width: 100%;   
      padding: 20px 10px;
      display: none;
      flex-direction: column;
      border-top: solid 0.8px var(--silver);
   }

   .post-comments-label{
      font-size: 24px;
      font-weight: bold;
      margin: 10px;
   }

   .post-add-comments {
      display: flex;
      flex-direction: row;
      width: 100%;
   }

   .post-user-pfp {
      height: 50px;
      width: 50px;
      border-radius: 50%;
      margin: 0px 10px;
   }


   .post-comment-input {
      display: flex;
      width: 100%;
      border-bottom: solid 0.6px var(--silver);
      background-color: transparent;
   }

   .post-comment-input:focus {
      outline: none;
      border-bottom : solid 0.8px var(--kinda-black);
}

   .post-comment-submit-container {
      display: flex;
      width: 100%;
      justify-content: flex-end;
      margin-top: 10px;
   }

   .post-comment-btn {
      font-size: 12px;
      padding: 2px 10px;
      margin: 8px 0;
      border: solid 2px var(--kinda-black);
      border-radius: 15px;
      background-color: transparent;
      color: var(--kinda-black);
      font-weight: 600;
      transition: all 0.35s;
   }

   .post-comment-btn:hover {
      background-color: var(--kinda-black);
      color: var(--kinda-white);
   }

   .comment-form{
      display: flex;
      flex-direction: column;
      width: 100%;
   }

   .comments{
      display: flex;
      flex-direction: column;
      width: 100%;
      
   }


   /* maker an offer styling  */
   .make-an-offer {  /*  display:flex to view the offers part  */ 
      display: none;
      flex-direction: column;
      padding-bottom: 10px ;
      width: 100%;
      border-top: solid 0.8px var(--silver);
   }

   .make-an-offer-container {
      display: flex;
      flex-direction: row;
      width: 100%;
   }

   .offers-lhs-exchange {  /*display this if the purpose of upload is exchange */
      display: flex;
      flex-direction: column;
      width: 100%;
      padding-right: 20px;
   }

   .offers-lhs-sales { /*display this if the purpose of upload is sales*/
      display: flex; 
      flex-direction: column;
      width: 100%;
      justify-content: center;
   }

   .offers-lhs-giveaway { /*display this if the purpose of upload is giveaway*/
      display: flex;
      flex-direction: column;
      justify-content: center;
      width: 100%;
      font-size: 14px;
      
   }

   .giveaway-message {
      color:var(--secondary-dull);
   }

   .price-title {
      font-size: 12px;
      color: var(--secondary-dull);
   }

   .book-quoted-price {
      font-size: 44px;
   }


   .post-offer-details-title {
      font-size: 24px;
      padding: 10px 0px 20px 0px;
   }

   .select-book-title {
      display: grid;
      font-weight: 600;
   }

   .exchange-book-listbox {
      width: 100%;
      height: 44px;
      margin: 10px 0px;
      font-size: 18px;
      padding: 10px 
   }

   .offering-book-image {
      height: 10px;
      width: 10px;
   }

   .exchange-book-listbox:focus {
      outline: none;
      border-left: solid 4px var(--secondary-dull);
   }


   .post-upload-details-list {
      display: flex ;
      flex-direction: column;
   } 

   .exchange-message-rhs-container {
      display: flex;
      flex-direction: column;
      width: 100%;
      padding-left: 20px;
      border-left: solid 0.8px var(--silver);
   }

   .offer-message {
      margin: 10px 0px ;
      padding: none;
      resize: none;
   }

   .offer-message:focus {
      outline: none;
      border-left: solid 4px var(--secondary-dull);
   }

   .request-button-container {
      display: flex;
      flex-direction: row;
      width: 100%;
      justify-content: flex-end;
      margin-top: 10px;
   }

   .make-request-btn {
      font-size: 14px;
      font-weight: 600;
      border: solid 2px var(--kinda-black);
      padding: 4px 10px;
      border-radius: 4px;
      transition: all 0.35s;
   }

   .make-request-btn:hover {
      background-color: var(--kinda-black);
      color: var(--kinda-white);
   }



   /* Category styling */
   .categories{
      display: flex;
      flex-direction: row;
      justify-content:start;
      justify-items: start;
      margin: 10px 0;
   }

   .category{

      display: flex;
      width: max-content;
      background-color: var(--silver);
      padding: 2px 14px;
      margin: 0px 6px;
      border-radius: 20px;
      align-items: center;
      font-weight: 600;
      color: var(--secondary-dull);
   }

   .mobile-tablet-categories {
      padding : 10px 0px ;
      display: flex;
      justify-content: center;
      display: none;
   }

   .delete-post-container {
      display: flex;
      justify-content: flex-end;
      width: 100%;
      padding-top: 20px;
      border-top: solid 0.8px var(--silver);
   }

   .delete-post-button {
      font-size: 14px;
      font-weight: 600;
      border: solid 2px var(--kinda-black);
      padding: 4px 10px;
      border-radius: 4px;
      transition: all 0.35s;
   }

   .delete-post-button:hover {
      background-color: var(--kinda-black);
      color: var(--kinda-white);
   }

   /* For tablets */
   @media screen and (max-width: 930px) {
      
      .post-container {
         width: 95vw;
         margin:20px;
      }

      .post-book-image-carousel{
         width: 240px;
         height: 340px;
      }

      .post-book-image {
         width: 240px;
         height: 340px;
      }

      .post-book-image img{
         width: 240px;
         height: 340px;
      }

      .post-text-info{
         margin-left: 0;
      }

      .post-book-name {
         font-size: 26px;
      }

      .post-book-author {
         font-size: 20px;
      }

      /* comment container styling */
      .commentor-info-submit-button{
         flex-direction: column;
      }

      .comments{
         margin: 2rem 0;
      }

      .submit-comment-button-container{
         align-self: flex-start;
      }

      /* make offer container styling*/
      .make-an-offer-container{
         flex-direction: column;
      }

      .offers-lhs-giveaway{
         margin:  10px 0;
      }

      .exchange-message-rhs-container{
         padding: 20px 0 0;
         margin: 10px 0;
         border-left: none;
         border-top: 0.8px solid var(--silver);
      }

      .categories {
         display: none;
      }

      .mobile-tablet-categories {
         display: flex;
      }

      .category {
         width: 95%;
         display: flex;
         justify-content: center;
      }
   }

   /* For mobile devices */
   /* TODO: make page responsive for mobile devices */
   @media screen and (max-width: 500px) {
      .post-book-image-carousel{
         width: none;
         height: none;
      }

      .post-information-container{
         padding-top:20px ;
      }

      .post-information-container{
            grid-template-columns: 1fr;
         }

      .post-top-information {
         padding:10px 0px;
      }

      .post-uploader-pfp {
         padding: 0px;
      }

      .post-upload-purpose-title {
         font-size: 8px;
      }

      .post-upload-purpose {
         font-size: 14px;
      }

      .post-uploader-name {
         font-size: 14px;
         height: 18px;
      }

      .mobile-tablet-categories {
         padding: 0px 4px;
         display: grid;
         grid-template-columns: 1fr 1fr 1fr;
      }
      
      .category {
         margin: 8px 6px;
         font-size: smaller;
      }
   }

</style>