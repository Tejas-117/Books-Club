<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

import store from "../state/store";

//  required fields: 'title', 'description', 'address', 'city', 'state', 'country', 'images'
//  optional fields: 'for_sale', 'price', 'author', 'publisher', isbn, 'categories'

const router = useRouter();

// state to represent input values
const title = ref('');
const description = ref('');
const address = ref('');
const city = ref('');
const state = ref('');
const country = ref('');
const for_sale = ref(0);
const price = ref();
const author = ref('');
const publisher = ref('');
const isbn = ref('');

// other util state
const loading = ref(false);
const message = ref('');

// function to post book to API
async function handleSubmit(e) {
   if (store.user === null) {
      message.value = 'Login to upload book';
      return;
   }

   // if book is not for sale or price is not specified, price defaults to 0
   if(for_sale.value == 0 || !price.value){
      price.value = 0;
   }

   const payload = {
      title: title.value,
      description: description.value,
      address: address.value,
      city: city.value,
      state: state.value,
      country: country.value,
      for_sale: for_sale.value,
      price: price.value,
      author: author.value,
      publisher: publisher.value,
      isbn: isbn.value,
   }

   // API accepts FormData at this endpoint.
   const formData = new FormData();
   for (const key in payload) {
      // add only input values which are not empty
      formData.append(key, payload[key]);
   }

   // append all uploaded images to `formData`;
   const allUploadedImages = document.getElementById('file').files;
   Array.from(allUploadedImages).forEach((image, idx) => {
      if(idx < 4){
         formData.append('images', image);
      }
   });

   // append all selected categories of the book.
   const bookCategories = document.querySelectorAll('.interest-active');
   bookCategories.forEach(interest => {
      formData.append("categories", interest.innerText.toLowerCase());
   });

   loading.value = true;
   message.value = 'Uploading book'

   // POST data to the API.
   const url = import.meta.env.VITE_BASE_API_URL + `books/`;
   const res = await fetch(url, {
      method: 'POST',
      headers: {
         Authorization: `Bearer ${store.authTokens.access}`
      },
      body: formData
   });

   loading.value = false;
   message.value = '';

   const { data, error } = await res.json();
   if (res.status === 200) {
      // if book was successfully uploaded, display message and redirect.
      message.value = 'Successfully uploaded book';

      setTimeout(() => {
         router.push(`/books/${data.book_id}`);         
      }, 2000)
   } else {
      message.value = error.message;
   }
}

// function to preview uploaded images.
function previewUploadedImages(e, previewAtId) {
   // get element to preview at.
   const previewAt = document.getElementById(previewAtId);
   previewAt.innerHTML = 'Files uploaded: ';

   // get all files uploaded by the user.
   const uploadedFileList = e.target.files;

   function readFile(index) {
      if (index >= Math.min(uploadedFileList.length, 4)) {
         return;
      }

      // FileReader to read file from user.
      const reader = new FileReader();

      // attach event listener, fired when file has been read successfully.
      reader.addEventListener('load', () => {
         // add src to preview element.
         const imgElement = document.createElement('img');
         imgElement.src = reader.result;
         previewAt.insertAdjacentElement('beforeend', imgElement);

         readFile(index + 1); // recurse and read next file.
      })

      reader.readAsDataURL(uploadedFileList[index]);
   }
   readFile(0); // read first file.
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

</script>

<template>
   <div class="content-container book-upload-container">
      <div class="card">
         <!-- LHS part  -->
         <form class="LHS" @submit.prevent="handleSubmit">
            <div class="title-book-details">
               Upload a book
            </div>

            <div class="input-boxes">
               Book Title : <br />
               <input v-model="title" class="take-in" type="text" placeholder="Enter book title" required>
            </div>

            <div class="input-boxes">
               Book isbn number : <br />
               <input v-model="isbn" class="take-in" type="text" placeholder="Enter isbn number (optional)">
            </div>

            <div class="input-boxes">
               Author name : <br />
               <input v-model="author" class="take-in" type="text" placeholder="Enter author name (optional)">
            </div>

            <div class="input-boxes">
               Publisher : <br />
               <input v-model="publisher" class="take-in" type="text" placeholder="Enter publisher name (optional)">
            </div>

            <div class="title-upload-img">
               Upload an image of your book :
            </div>
            <input type="file" accept="image/*" name="image" id="file" style="display:none" multiple
               @input="previewUploadedImages($event, 'preview-images')">
            <label for="file">
               <div class="pic-upload">
                  <img class="upload-icon" src="../assets/images/upload-icon.png">
                  Upload book images (Max 4)
               </div>
            </label>

            <!-- preview all uploaded images -->
            <div id="preview-images"></div>

            <div>
               <p class="what-book">
                  What would you like to do with your book ?
               </p>
               <div class="drop-list-container">
                  <select class="drop-list" v-model="for_sale">
                     <option :value=1>Give away</option>
                     <option :value=0>Trade</option>
                     <option :value=1>Sell</option>
                  </select>
               </div>

               <div class="input-boxes">
                  <input v-model="price" class="take-in" type="number"
                     placeholder="Quote a Price if you are selling the book">
               </div>
            </div>

            <p class="add-description">Add a description</p>
            <p class="Subs">Let other readers know about your experience of this book </p>
            <textarea v-model="description" class="description" type="text" required rows="5" cols="30"
               maxlength="300"></textarea>

            <p class="add-description">Add location details of the book</p>
            <div class="input-boxes">
               Address : <br />
               <input v-model="address" class="take-in" type="text" placeholder="Enter address" required>
            </div>
            <div class="input-boxes">
               City : <br />
               <input v-model="city" class="take-in" type="text" placeholder="Enter city" required>
            </div>
            <div class="input-boxes">
               State : <br />
               <input v-model="state" class="take-in" type="text" placeholder="Enter state" required>
            </div>
            <div class="input-boxes">
               Country : <br />
               <input v-model="country" class="take-in" type="text" placeholder="Enter country" required>
            </div>

            <!-- All available interests -->
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

            <!-- Contains `loader` and `message` -->
            <div class="message-container">
               <span v-if="loading" class="loader"></span>
               <span v-if="message" class="message">{{ message }}</span>
            </div>

            <div class="submit">
               <button class="submit-button" type="submit">Submit</button>
            </div>
         </form>
      </div>
   </div>
</template>

<style>
   .book-upload-container {
      display: flex;
      justify-content: center;
      background: url(../assets/images/Books-image.jpg);
      min-height: 100vh;
   }

   /* body of the webpage after header  */
   .card {
      display: flex;
      flex-direction: column;
      justify-content: center;
      background-color: var(--kinda-white);
      border: 2px solid var(--borders);
      padding: 40px;
      border-radius: 10px;
      margin: 40px auto;
      width: clamp(200px, 700px, 90vw);
      height: fit-content;
   }

   .card textarea {
      resize: none;
      max-width: 100%;
   }

   .title-book-details {
      font-size: 30px;
      font-weight: bold;
      margin-bottom: 20px;
      text-align: center;
   }

   .input-box {
      display: flex;
      justify-content: center;
      margin-bottom: 10px;
   }

   .take-in {
      width: 100%;
      height: 50px;
      border-radius: 4px;
      border-style: solid;
      border-width: 0.2px;
      border-color: var(--borders);
      background-color: var(--kinda-white);
      margin-bottom: 20px;
      padding: 0px 10px;
      margin-top: 10px;
      transition: border-color 0.2s;
   }

   .take-in:hover {
      cursor: pointer;
   }

   .title-upload-img {
      margin: 20px 0px;
      font-size: 16px;
      font-weight: 550;
   }

   .upload-icon {
      width: 20px;
      display: block
   }

   .pic-upload {
      height: 100px;
      display: flex;
      justify-content: center;
      align-items: center;
      border-style: solid;
      border-width: 0.2px;
      border-color: var(--borders);
      border-radius: 8px;
      flex-direction: column;
      width: 100%;
      margin: 1rem auto;
      transition: border-color 0.2s;
      width: 100%;
   }

   .pic-upload:hover {
      cursor: pointer;
   }

   #preview-images {
      width: 100%;
      display: grid;
      grid-template-columns: repeat(auto-fill, 100px);
      grid-gap: 10px;
   }

   #preview-images img {
      width: 100px;
      height: 140px;
      object-fit: contain;
      object-position: 50% 50%;
   }

   .upload-icon {
      margin-bottom: 10px;
   }

   .submit {
      width: 100%;
      margin: 10px 0;
   }

   .submit-button {
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

   .submit-button:hover {
      background-color: var(--kinda-white);
      color: var(--kinda-black);
      border-color: var(--kinda-black);
      font-weight: 600;
      cursor: pointer;
      transition-duration: 0.35s;
   }

   .add-description {
      margin: 10px 0 0;
   }

   .Subs {
      background-color: var(--kinda-white);
      margin: 2px;
      font-size: 12px;
   }

   .description {
      background-color: var(--kinda-white);
      border: 2px solid var(--borders);
   }

   .commento {
      border: none;
      max-width: 400px;
      max-height: 300px;
      border-radius: 8px;
      margin: 4px;
      background-color: #cfe3f6;
   }

   .what-book {
      margin-top: 40px;
   }

   .drop-list {
      width: 50%;
      border-style: solid;
      border-width: 0.2px;
      border-color: var(--borders);
      background-color: var(--kinda-white);
      height: 30px;
      border-radius: 8px;
      margin: 20px 0px;
      transition: all 0.2s;
   }
</style>
