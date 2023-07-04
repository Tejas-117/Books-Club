<script setup>
   import { useRouter, useRoute } from 'vue-router';
   import { nextTick, onMounted, ref } from 'vue';
   import store from "../state/store";

   // import required assets
   import defaultProfile from '../assets/images/default-profile.png';
   import defaultCover from '../assets/images/default-cover.jpg';

   const route = useRoute();
   const router = useRouter();
   const userId = route.params.id;

   const loading = ref(false);
   const message = ref('');

   // represents input values
   const firstName = ref('');
   const lastName = ref('');
   const gender = ref(4);
   const date_of_birth = ref('');
   const bio = ref('');
   const interests = ref([]);
   const images = ref([]);

   // function to fetch data from API.
   async function fetchData(){
      message.value = 'Fetching data';
      loading.value = true;

      const url = import.meta.env.VITE_BASE_API_URL + `users/${userId}`;
      const res = await fetch(url, {
         headers: {
            Authorization: `Bearer ${store.authTokens.access}`
         }
      });
      const { data } = await res.json();

      message.value = '';
      loading.value = false;

      if(res.status === 200){
         if(store.user.user_id !== data.id){
            message.value = "Unauthorised";
         } 
         else {
            firstName.value = data.first_name;
            lastName.value = data.last_name;
            bio.value = data.bio;
            interests.value = data.interests;
            images.value = data.images;
            gender.value = data.gender;
            date_of_birth.value = data.date_of_birth;
         }
      }
      else{
         message.value = "Couldn't get user data!!"
      }
   }

   onMounted(async () => {
      await fetchData();
      await nextTick();

      // show user interests as active.
      const allInterestOptions = document.querySelectorAll('.interest-button');
      const allUserInterests = new Set(interests.value.map(interest => interest.text));
      
      Array.from(allInterestOptions).forEach(interest => {
         const interestText = interest.innerText.toLowerCase();
         
         if(allUserInterests.has(interestText)){
            interest.classList.add('interest-active');
         }
      });
   });

   // function to handle submit.
   async function handleSubmit(){
      const payload = {
         first_name: firstName.value,
         last_name: lastName.value,
         gender: gender.value,
         date_of_birth: date_of_birth.value,
         bio: bio.value
      };

      // construct FormData.
      const formData = new FormData();
      for(const key in payload){
         // add only input values which are not empty
         if(payload[key]){
            formData.append(key, payload[key]);
         }
      }

      // append all interest to `formData`
      const interestsSelected = document.querySelectorAll('.interest-active');
      for(let i=0; i<interestsSelected.length; i++){
         formData.append('interests', interestsSelected[i].innerText.toLowerCase());
      }
      
      // append all uploaded images to `formData`;
      const coverImageFile = document.getElementById('edit-bg').files[0];
      const profileImageFile = document.getElementById('edit-pfp').files[0];

      if(coverImageFile){
         formData.append('cover_image', coverImageFile);
      }
      if(profileImageFile){
         formData.append('profile_image', profileImageFile);
      }
      
      // scroll to top and display status of updation. 
      window.scrollTo(0, 0);

      loading.value = true;
      message.value = 'Submitting changes...'
      
      const url = import.meta.env.VITE_BASE_API_URL + `users/${userId}/`;
      const res = await fetch(url, {
         method: 'PUT',
         headers: {
            Authorization: `Bearer ${store.authTokens.access}`
         },
         body: formData
      });
      
      loading.value = false;
      
      if(res.status === 200){
         const { data } = await res.json();
         message.value = data.message;

         // redirect to user profile on successful redirect
         setTimeout(() => {
            router.push(`/users/profile/${userId}`);
         }, 1000);
      }
      else{
         message.value = "Couldn't update profile";         
      }
   }

   // function to change interests
   function changeInterest(element){      
      // return if clicked on wrong element.
      if(element.classList.contains('interest-button') === false){
         return;
      }
      
      // toggle `interest-active` class
      element.classList.toggle('interest-active');
   }

   // function to get 'profile' and 'cover' image from user data;
   function getUserImage(type){
      const defaultImages = {
         'cover': defaultCover,
         'profile': defaultProfile
      }

      const image = images?.value.filter(image => type === image.type);
      return image.length ? image[0].url : defaultImages[type]; 
   }

   // function to preview uploaded image
   function previewUploadedImage(e, previewAtId){
      const previewAt = document.getElementById(previewAtId);
      const uploadedFile = e.target.files[0];

      // FileReader to read file from user.
      const reader = new FileReader();

      // attach event listener, fired when file has been read successfully
      reader.addEventListener('load', () => {
         previewAt.src = reader.result;
      })

      reader.readAsDataURL(uploadedFile);
   }
</script>

<template>
<div class="edit-pf-master-container content-container">

   <!-- loader and message elements -->
   <div class="message-container" v-if="loading || message">
      <span v-if="loading" class="loader"></span>
      <span v-if="message" class="message">{{ message }}</span>
   </div>

   <div class="edit-card">
      <h2 class="edit-profile-title">Edit Profile</h2>

      <div class="update-images-container">
         <div class="update-image">
            <input type="file" accept="image/*" name="image" id="edit-bg" style="display:none" @input="previewUploadedImage($event, 'cover-pic-img')">
            <label for="edit-bg">
               <img class="edit-bg-pic" src="../assets/images/edit-image-icon.png">
            </label>
         </div>
         <div class="edit-cover-pic">
            <img id="cover-pic-img" :src="getUserImage('cover')" alt="">
         </div>

         <div class="update-image">
            <input type="file" accept="image/*" name="image" id="edit-pfp" style="display:none" @input="previewUploadedImage($event, 'profile-pic-img')">
            <label for="edit-pfp">
               <img class="edit-pfp-pic" src="../assets/images/edit-image-icon.png">
            </label>
         </div>

         <div class="edit-profile-pic">
            <img id="profile-pic-img" :src="getUserImage('profile')" alt="">
         </div>
      </div>

      <div class="edit-details-container">
         <div class="register-input-box-holder">First name
            <input class="register-input-box" type="text" placeholder="Enter your first name" v-model="firstName">
         </div>

         <div class="register-input-box-holder">Last name
            <input class="register-input-box" type="text" placeholder="Enter your last name" v-model="lastName">
         </div>

         <div class="register-input-box-holder">Gender
            <label for="gender-category"></label>
            <select name="gender-category" id="sex" class="register-input-box-gender" v-model="gender">
               <option value="1">Male</option>
               <option value="2">Female</option>
               <option value="3">Others</option>
               <option value="4">Rather not say</option>
            </select>
         </div>

         <div class="register-input-box-holder">
            <label for="dob">Date of birth:</label>
            <input class="input-box" type="date" id="dob" min="1960-01-01" max="2015-01-01" v-model="date_of_birth">
         </div>

         <div class="register-input-box-holder">Bio
            <input class="register-input-box" type="text" placeholder="Enter your bio" v-model="bio">
         </div>

         <h4 class="interest-title">Select your genre of interest</h4>
         <div class="interest-container" @click="changeInterest($event.target)">
            <div class="interest-button">Action</div>
            <div class="interest-button">Novel</div>
            <div class="interest-button">Magazine</div>
            <div class="interest-button">Documentation</div>
            <div class="interest-button">Mystery</div>
            <div class="interest-button">Comedy</div>
            <div class="interest-button">Education</div>
            <div class="interest-button">Horror</div>
            <div class="interest-button">Romance</div>
            <div class="interest-button">Sci-fi</div>
            <div class="interest-button">Fantasy</div>
            <div class="interest-button">Biography</div>
            <div class="interest-button">Entertainment</div>
            <div class="interest-button">Literature</div>
            <div class="interest-button">History</div>
         </div>

         <button class="save-changes" @click="handleSubmit">Save changes</button>
      </div>
   </div>
</div>   
</template>

<style>
   /* body of the page starts here */
   .edit-pf-master-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background-image: url(../assets/images/Books-image.jpg);
      background-size: cover;
      min-height: 100vh;
      position: relative;
   }

   /* custom message container specific to this page */
   .edit-pf-master-container .message-container{
      width: 300px;
      font-size: 1.1rem;
   }

   .edit-pf-master-container .message-container .loader{
      width: 70px;
      height: 70px;
   }


   .edit-card {
      display: grid;
      align-items: center;
      background-color: var(--kinda-white); 
      width: clamp(200px, 600px, 90vw);
      border-radius: 10px;
      margin-bottom: 40px;
   }

   .edit-profile-title {
      justify-self: start;
      padding: 10px 10px;
      margin: 0px auto;
      font-weight: 800;
   }

   /*background picture & profile picture*/
   .update-images-container {
      height:200px;
      background-color: var(--kinda-grey);
      position: relative;
      background-size: cover;
   }

   .edit-profile-pic {
      background-color: var(--kinda-grey);
      height:160px;
      width:160px;
      position: relative;
      left: 10%;
      bottom: 50%;
      border-radius:50%;
      border-style:solid;
      border-width:4px;
      border-color: var(--kinda-white);
      overflow: hidden;
   }

   .edit-cover-pic{
      position: relative;
      width: 100%;
      height: 100%;
   }

   .edit-cover-pic img, .edit-profile-pic img{
      width: 100%;
      height: 100%;
      object-fit: cover;
   }

   .edit-bg-pic {
      padding: 10px;
      background-color: rgb(235, 230, 230);
      position: absolute;
      z-index: 10;
      width:35px;
      height:35px;
      right:40px;
      bottom:-25px;
      border-radius: 50%;
   }

   .edit-pfp-pic {
      z-index: 10;
      padding: 10px;
      background-color: rgb(235, 230, 230);
      position: absolute;
      width:30px;
      height:30px;
      left: 180px;
      bottom:-50px;
      border-radius: 50%;
   }

   .edit-details-container {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      width: 100%;
      color:var(--kinda-black);
      margin : 70px 0px;
      padding: 1rem;
   }

   .register-input-box-holder {
      font-weight: 550;
      width: 80%;
      margin:10px 0px;
   }

   .register-input-box {
      display: flex;
      width: 100%;
      background-color: var(--kinda-white);
      border-style: solid;
      border-width: 1px;
      border-radius: 4px;
      padding: 6px 8px;
      margin:8px 0 0;
   }

   .register-input-box-gender {
      background-color: var(--kinda-white);
      display: flex;
      width: 100%;
      margin: 10px 0px;
      border-style: solid;
      border-width: 1px;
      border-radius: 4px;
      padding: 6px 8px;
   }


   .interest-title {
      font-weight: 400;
      font-size: larger;
      margin: 20px 0px 20px 0px;
   }

   .interest-container {
      display: grid;
      width: 80%;
      margin: 20px 0px;
      grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)) ;
      justify-content: center;
   }

   .interest-button {
      text-align: center;
      padding: 2px 14px;
      background-color: var(--very-close-black);
      color: var(--kinda-white);
      border-radius: 4px;
      margin: 5px;
   }

   .interest-button:hover{
      background-color: var(--kinda-white);
      color: var(--kinda-black);
      padding: 0px 12px;
      border: 1px solid var(--kinda-black);
      cursor: pointer;
   }

   .interest-active{
      background-color: var(--kinda-white);
      color: var(--kinda-black);
      padding: 0px 12px;
      border: 1px solid var(--kinda-black);
      cursor: pointer;
   }

   .save-changes {
      margin: 40px 0px ;
      padding: 4px 20px;
      border: 0.8px solid var(--kinda-black);
      background-color: var(--kinda-white);
      border-radius: 4px;
      justify-self: center;
      width: 50%;
      transition: all 0.35s ease-out;
   }

   .save-changes:hover {
      background-color: var(--kinda-black);
      color: var(--kinda-white);
      border-radius: 8px;
   }
</style>