<script setup>
   import { nextTick, onMounted, ref } from 'vue';
   import { useRoute, useRouter } from 'vue-router';
   import store from '../state/store';

   const route = useRoute();
   const router = useRouter();

   // get book-id from url params.
   const bookId = route.params.id;

   // represents 'book' that's being edited.
   const book = ref(null);

   // represents 'form-data'.
   const title = ref('');
   const description = ref('');
   const address = ref('');
   const city = ref('');
   const state = ref('');
   const country = ref('');
   const for_sale = ref(1);
   const price = ref();
   const author = ref('');
   const publisher = ref('');
   const isbn = ref('');

   // other util state.
   const loading = ref(false);
   const message = ref('');

   const BASE_API_URL = import.meta.env.VITE_BASE_API_URL;

   // get initial data of the book to edit.
   async function fetchData() {
      loading.value = true;
      message.value = 'Loading...';

      const url = BASE_API_URL + `books/${bookId}`;
      const res = await fetch(url, {
         headers: {
            Authorization: `Bearer ${store.authTokens.access}`
         }
      });

      const { data, error } = await res.json();

      loading.value = false;
      message.value = '';

      // if data is fetched successfully.
      if (res.status === 200) {
         book.value = data.book;

         // if 'logged-in' user is not the 'owner' of the book post redirect them.
         if (book.value.user.id !== store.user.user_id) {
            message.value = 'Unauthorized!!';
            router.push('/feeds');
         }
      }
      else {
         message.value = error.message;
      }
   }

   // submit edited info to the API.
   async function handleSubmit(){
      const payload = {
         title: title.value,
         description: description.value,
         address: address.value,
         city: city.value,
         state: state.value,
         country: country.value,
         author: author.value,
         publisher: publisher.value,
         isbn: isbn.value,
      }
      
      const formData = new FormData();
      for (const key in payload) {
         // add only input values which are not empty.
         if (payload[key]) {
            formData.append(key, payload[key]);
         }
      }

      // if book is not for sale or price is not specified, price defaults to 0
      if(for_sale.value == 0 || !price.value){
         price.value = 0;
      }

      formData.append('for_sale', for_sale.value);
      formData.append('price', price.value);


      // append uploaded images.
      const uploadedImages = Array.from(document.querySelector('#file').files);
      uploadedImages.forEach(image => formData.append('images', image));

      // append images to be deleted.
      const deletedImages = document.querySelectorAll('.delete-image');
      deletedImages.forEach(image => formData.append('delete_images', image.id));

      // append categories
      const allCategoriesSelected = document.querySelectorAll('.interest-active');
      allCategoriesSelected.forEach(category => formData.append('categories', category.innerText.toLowerCase()));

      loading.value = true;
      message.value = 'Submitting response...'

      // submit data to API
      const url = BASE_API_URL + `books/${bookId}/`;
      const res = await fetch(url, {
         method: 'PUT',
         headers: {
            Authorization: `Bearer ${store.authTokens.access}`
         },
         body: formData
      });

      loading.value = false;
      message.value = ''

      const { data, error } = await res.json();
      if(res.status === 200){
         message.value = data.message;
         router.push(`/books/${bookId}`);
      }
      else{
         message.value = error.message;
      }
   }

   onMounted(async () => {
      await fetchData(); // await till data is fetched.
      await nextTick(); // await till DOM is updated.

      if(!book.value){
         return
      }

      // update initial data to be in 'form input' elements.
      title.value = book.value.title;
      description.value = book.value.description;
      address.value = book.value.address;
      city.value = book.value.city;
      state.value = book.value.state;
      country.value = book.value.country;
      for_sale.value = (book.value.for_sale) ? 1 : 0;
      price.value = book.value.price;
      author.value = book.value.author;
      publisher.value = book.value.publisher;
      isbn.value = book.value.isbn;

      // show current categories of the book as active categories.
      const allCategoriesOptions = document.querySelectorAll('.interest-button');
      const allBookCategories = new Set(book.value.categories.map(category => category.text)); // makes look-up time faster.

      Array.from(allCategoriesOptions).forEach(category => {
         const categoryText = category.innerText.toLowerCase();

         if (allBookCategories.has(categoryText)) {
            category.classList.add('interest-active'); // add 'active' class to current book categories before updation.
         }
      });
   });

   // function to preview uploaded images.
   function previewUploadedImages(e, previewAtId) {
      // get element to preview at.
      const previewAt = document.getElementById(previewAtId);
      previewAt.innerHTML = 'Images uploaded: ';

      // get all files uploaded by the user.
      const uploadedFileList = e.target.files;

      // calculate max number of images to upload.
      const deletedImagesCount = document.querySelectorAll('.delete-image').length;
      const currentImagesCount = book.value.images.length;
      const maxImagesToUpload = 4 - (currentImagesCount - deletedImagesCount);

      function readFile(index) {
         if (index >= Math.min(maxImagesToUpload, uploadedFileList.length)) {
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
               Edit book
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
            
            <!-- display current images of the book -->
            Select image to delete.
            <div v-if="book?.images.length" class="current-book-images">
                  <img v-for="image in book.images" :id="image.filename" :src="image.url" alt="" @click="(e) => e.target.classList.toggle('delete-image')">
            </div>

            <!-- input images of the book -->
            <div class="title-upload-img">
               Upload an image of your book :
            </div>

            <input type="file" accept="image/*" name="image" id="file" style="display:none" multiple
               @input="previewUploadedImages($event, 'preview-images')">
            <label for="file">
               <div class="pic-upload">
                  <img class="upload-icon" src="../assets/images/upload-icon.png">
                  Upload book images (Max 4, including current images)
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
   .current-book-images{
      width: 100%;
      display: grid;
      grid-template-columns: repeat(auto-fill, 100px);
      grid-gap: 10px;
   }

   .current-book-images img{
      width: 100px;
      height: 100px;
      cursor: pointer;
   }

   .current-book-images img:hover{
      transform: scale(0.9);
   }

   .delete-image{
      opacity: 0.25;
   }

</style>