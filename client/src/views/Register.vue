<script setup>
import { ref } from "vue";
import { useRouter, RouterLink } from "vue-router";

// Fields required to register user :
// required --> first_name, last_name, email,  password
// optional -->  gender, dob, interests, profile_image and cover_image

// required 'form data' state;
const first_name = ref('');
const last_name = ref('');
const email = ref('');
const password = ref('');
const confirm_password = ref('');
const gender = ref('4');
const date_of_birth = ref('');
const bio = ref('');

// other util state;
const loading = ref(false);
const message = ref('');
const registerProcess = ref(1);
const router = useRouter();

async function handleSubmit(e) {
   message.value = ''
   if (password.value !== confirm_password.value) {
      message.value = "Re-enter password.";
      return;
   }

   // if registeration process is incomplete, reveal second step.
   if (registerProcess.value === 1) {
      registerProcess.value = 2;
      return;
   }

   // update loading and message values.
   loading.value = true;
   message.value = 'Submitting data..';

   const url = import.meta.env.VITE_BASE_API_URL + 'users/register/'
   // append required data;
   const payload = {
      first_name: first_name.value,
      last_name: last_name.value,
      email: email.value,
      password: password.value,
   }

   const formData = new FormData();
   for (const key in payload) {
      if (!payload[key]) {
         registerProcess.value = 1;
         loading.value = false;
         message.value = 'Incomplete information'
         return;
      }
      formData.append(key, payload[key]);
   }

   // append additional data;
   formData.append('gender', gender.value);
   formData.append('date_of_birth', date_of_birth.value);
   formData.append('bio', bio.value);

   // if user uploads profile-image and cover-image append it to formData
   const profileImageFile = document.querySelector('#profile-image').files;
   const coverImageFile = document.querySelector('#cover-image').files;
   if (profileImageFile.length) {
      formData.append('profile_image', profileImageFile[0]);
   }
   if (coverImageFile.length) {
      formData.append('cover_image', coverImageFile[0]);
   }

   // append interests selected by users
   const userInterests = document.querySelectorAll('.interest-active');
   userInterests.forEach(interest => {
      formData.append("interests", interest.innerText.toLowerCase());
   });

   // POST data to the API.
   const res = await fetch(url, {
      'method': 'POST',
      'body': formData
   });
   const data = await res.json();

   // set loading to false
   loading.value = false;
   message.value = '';

   // Successfully registered user
   if(res.status === 200){
      message.value = "User registered successfully"

      // if user registeration is successful, redirect to login page after 3s.
      setTimeout(() => {
         router.replace("login/")            
      }, 2000);
   } else { 
      message.value = data.error.message;
   }
}

// function to change interests
function changeInterest(element) {
   // return if clicked on wrong element.
   if (element.classList.contains('interest-button') === false) {
      return;
   }

   // toggle `interest-active` class
   element.classList.toggle('interest-active');
}

// function to preview uploaded image
function previewUploadedImage(e, previewAtId) {
   // get element to preview at.
   const previewAt = document.getElementById(previewAtId);

   // get file uploaded by the user.
   const uploadedFile = e.target.files[0];

   // FileReader to read file from user.
   const reader = new FileReader();

   // attach event listener, fired when file has been read successfully
   reader.addEventListener('load', () => {
      // add src to preview element.
      previewAt.src = reader.result;
      previewAt.removeAttribute('hidden');
   })

   reader.readAsDataURL(uploadedFile);
}

</script>

<template>
   <div class="register-master-container content-container">
      <div class="box-form">
         <div class="create-account">Create an account</div>
         <div class="already-have-account"> Already have an account ? <RouterLink to="/login">Sign in</RouterLink>
         </div>

         <!-- First part of registration process -->
         <div v-if="registerProcess === 1" style="width: 100%;">
            <div class="input-box-holder">
               First name
               <input class="input-box" type="text" placeholder="Enter your first name" v-model="first_name" required>
            </div>


            <div class="input-box-holder">
               Last name
               <input class="input-box" type="text" placeholder="Enter your last name" v-model="last_name" required>
            </div>


            <div class="input-box-holder">
               Email
               <input class="input-box" type="email" placeholder="Enter your email address" v-model="email" required>
            </div>

            <div class="input-box-holder">
               Gender
               <label for="gender-category"></label>
               <select name="gender-category" id="sex" class="input-box-gender" v-model="gender">
                  <option value="1">Male</option>
                  <option value="2">Female</option>
                  <option value="3">Others</option>
                  <option value="4">Rather not say</option>
               </select>
            </div>

            <div class="input-box-holder">
               <label for="dob">Date of birth:</label>
               <input class="input-box" type="date" id="dob" min="1960-01-01" max="2015-01-01" v-model="date_of_birth">
            </div>

            <div class="input-box-holder">
               Bio
               <input class="input-box" type="text" placeholder="Enter your bio (optional)" v-model="bio">
            </div>

            <div class="input-box-holder">Password
               <input class="input-box" type="password" placeholder="Enter a password" v-model="password" required>
            </div>

            <div class="input-box-holder">Re-enter Password
               <input class="input-box" type="password" placeholder="Re-enter passsword" v-model="confirm_password" required>
            </div>
         </div>

         <!-- Second part of the registration process -->
         <div v-if="registerProcess === 2" style="width: 100%; margin: 2rem auto;">
            <!-- Input profile image from the user. -->
            <input type="file" accept="image/*" name="image" id="profile-image" style="display:none"
               @input="previewUploadedImage($event, 'profile-upload-preview')">
            <label for="profile-image">
               <div class="pic-upload">
                  <img class="upload-icon" src="../assets/images/upload-icon.png">
                  Upload a profile image (optional)
               </div>
            </label>

            <!-- Preview profile image -->
            <div class="profile-upload-preview">
               Preview of profile image :
               <img id="profile-upload-preview" src="" hidden>
            </div>

            <input type="file" accept="image/*" name="image" id="cover-image" style="display:none"
               @input="previewUploadedImage($event, 'cover-upload-preview')">
            <label for="cover-image">
               <div class="pic-upload">
                  <img class="upload-icon" src="../assets/images/upload-icon.png">
                  Upload a cover image (optional)
               </div>
            </label>
            <div class="cover-upload-preview">
               Preview of cover image :
               <img id="cover-upload-preview" src="" hidden>
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
         </div>

         <!-- Contains `loader` and `message` -->
         <div class="message-container">
            <span v-if="loading" class="loader"></span>
            <span v-if="message" class="message">{{ message }}</span>
         </div>

         <div class="proceed-button-container">
            <button @click="handleSubmit" class="proceed-button">{{ (registerProcess === 1) ? 'Proceed' : 'Sign Up'
            }}</button>
         </div>
      </div>
   </div>
</template>

<style>
   body {
      justify-items: center;
      align-items: center;
      min-width: 200px;
   }

   .message-container {
      width: 100%;
      margin: 8px 0px;
      padding: 8px 0;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      font-size: 0.8rem;
   }

   /* change color to match color scheme */
   .loader {
      border: 9px solid #b5adad;
      border-top: 9px solid #020d14;
      border-radius: 50%;
      width: 35px;
      height: 35px;
      animation: spin 1s linear infinite;
      margin: 5px 0;
   }

   @keyframes spin {
      0% {
         transform: rotate(0deg);
      }

      100% {
         transform: rotate(360deg);
      }
   }

   .message {
      width: 90%;
      padding: 6px;
      margin: 8px 0 0;
      color: var(--kinda-black);
      text-align: center;
      background-color: rgb(186, 186, 180);
      border-radius: 5px;
   }

   .register-master-container .message-container {
      width: 100%;
   }

   .register-master-container .message {
      padding: 7px 0;
   }

   .register-master-container {
      width: 100%;
      background-image: url(../assets/images/Books-image.jpg);
      background-size: cover;
      min-height: 100vh;
   }

   .box-form {
      display: grid;
      justify-items: center;
      justify-content: center;
      background-color: var(--kinda-white);
      grid-auto-columns: 90%;
      padding: 30px;
      border-radius: 10px;
      width: clamp(200px, 600px, 90vw);
      margin: 10vh auto;
   }

   .create-account {
      font-size: 34px;
      font-weight: bold;
   }

   .already-have-account {
      margin-bottom: 40px;
   }

   .register-master-container .interest-title {
      text-align: center;
   }

   .register-master-container .interest-container {
      display: grid;
      width: 80%;
      margin: 20px auto;
      grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
      justify-content: center;
   }

   .input-box-holder {
      font-weight: 550;
      width: 90%;
      margin: 0 auto;
   }

   .input-box {
      width: 100%;
      display: flex;
      border-style: solid;
      border-color: var(--kinda-grey);
      border-width: 1.6px;
      border-radius: 4px;
      padding: 6px 8px;
      margin: 4px 0px;
      background-color: var(--kinda-white);
   }

   .input-box-gender {
      width: 100%;
      display: flex;
      margin: 10px 0px;
      border-style: solid;
      border-color: var(--kinda-grey);
      background-color: var(--kinda-white);
      border-width: 1.6px;
      border-radius: 4px;
      padding: 6px 8px;
   }

   .proceed-button-container {
      width: 90%;
   }

   .proceed-button {
      width: 100%;
      background-color: var(--kinda-black);
      color: var(--kinda-white);
      padding: 5px;
      border-style: solid;
      border-width: 2px;
      border-color: var(--kinda-black);
      border-radius: 6px;
      font-size: 14px;
      font-weight: 550;
   }

   .proceed-button:hover {
      background-color: var(--kinda-white);
      color: var(--kinda-black);
      border-color: var(--kinda-black);
      font-weight: 600;
      cursor: pointer;
   }

   .profile-upload-preview,
   .cover-upload-preview {
      width: 80%;
      margin: 1rem auto;
      object-fit: cover;
      display: flex;
      flex-direction: row;
      justify-content: flex-start;
   }

   .profile-upload-preview img,
   .cover-upload-preview img {
      width: 100px;
      height: 100px;
   }
</style>