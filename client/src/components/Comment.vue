<script setup>
   import { ref } from "vue";
   import store from "../state/store";

   // import required assets
   import defaultProfile from '../assets/images/default-profile.png';
   import defaultCover from '../assets/images/default-cover.jpg';

   const props = defineProps({
      comment: Object,
      deleteComment: Function
   });

   const comment = ref(props.comment);

   // function to get `profile` and `cover` image from the data.
   function getUserProfile(type){
      const defaultImages = {
         'cover': defaultCover,
         'profile': defaultProfile
      }
      const image = comment.value.user.images?.filter(image => type === image.type);
      return image.length ? image[0].url : defaultImages[type]; 
   }
</script>

<template>
   <div class="comment">
      <div class="post-comment-nest">
         <img class="post-commentor-pfp" :src="getUserProfile('profile')">
         <div class="commentor-info-submit-button">

            <div class="commentor-info">
               <div>
                  <span class="comment-user">{{ comment.user.first_name + ' ' + comment.user.last_name }}</span>
                  <span class="comment-time">{{ comment.created_on }}</span>
               </div>
               <span class="comment-text">{{ comment.comment }}</span>
            </div>

            <div class="submit-comment-button-container">
               <button 
               v-if="store.user && store.user.user_id === comment.user.id"
               @click="() => deleteComment(comment)"
               class="comment-delete-btn"
               >Delete comment</button>
            </div>
         </div>
      </div>
   </div>
</template>

<style>
   .comment{
      width: 100%;
      margin: 10px 0px 0px;
      padding: 10px 0px;
      display: flex;
      flex-direction: column;
   }

   .post-comment-nest {
      display: flex;
      flex-direction: row;
   }

   .post-commentor-pfp {
      height: 50px;
      width: 50px;
      border-radius: 50%;
      margin: 0px 10px; 

   }

   .commentor-info-submit-button {
      display: flex;
      flex-direction: row;
      width: 100%;
      justify-content: space-between;
   }

   .comment-text {
      display: inline-block;
      margin: 0px 10px;
   }

   .submit-comment-button-container {
      display: flex;
      align-self: flex-end;
   }

   .comment-user {
      font-weight: 700;
      margin: 0px 10px;
      font-size: 18px;
   }

   .comment-time {
      font-weight : 700;
      margin: 0px 6px;
      font-size: 12px;
      color: var(--secondary-dull);
   }

   .commentor-info {
      display: flex;
      flex-direction: column;
   }

   .comment .label   {
      text-decoration: underline;
   }

   .comment-delete-btn{
      width: max-content;
      padding: 2px 10px;
      margin: 8px 0;
      border: solid 2px var(--kinda-black);
      border-radius: 15px;
      background-color: transparent;
      color: var(--kinda-black);
      font-weight: 600;
      transition: all 0.35s;
   }

   .comment-delete-btn:hover {
      background-color: var(--kinda-black);
      color: var(--kinda-white);
   }
</style>