<script setup>
   import { onMounted, ref } from 'vue';
   import store from "../state/store";
   import Offer from "../components/Offer.vue";

   const offers = ref(null);

   const loading = ref(false);
   const message = ref('');

   // function to get data from API
   async function fetchData(){
      loading.value = true;
      message.value = 'Fetching data...'

      const url = import.meta.env.VITE_BASE_API_URL + `offers/?received=true`;
      const res = await fetch(url, {
         headers: {
            Authorization: `Bearer ${store.authTokens.access}`
         }
      })

      const { data } = await res.json();

      loading.value = false;
      message.value = '';

      if(res.status === 200){
         offers.value = data.offers;
      }
   }

   // function to accept/reject offer
   async function updateOffer(e, offerId, status){
      loading.value = true;
      message.value = 'Updating status of the offer';
      
      const url = import.meta.env.VITE_BASE_API_URL + `offers/${offerId}/`;
      
      const res = await fetch(url, {
         'method': 'PUT',
         'headers': {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${store.authTokens.access}`
         },
         body: JSON.stringify({ status: status })
      });
      const { data, error }= await res.json();
      
      loading.value = false;
      message.value = '';
      
      if(res.status === 200){
         // update the status of the offer in UI;
         const offerIdx = offers.value.findIndex(offer => offer.id === offerId);
         offers.value[offerIdx].status = data.status;
      }
      else{
         message.value = "Couldn't upate status of the offer!!";
      }
   }

   onMounted(fetchData);
</script>

<template>
   <div class="offer-container content-container">
      <h2>All offers received</h2>

      <!-- loader and message elements -->
      <div class="message-container" v-if="message || loading">
         <span v-if="loading" class="loader"></span>
         <span v-if="message" class="message">{{ message }}</span>
      </div>


      <div class="offers" v-if="offers">
            <Offer 
               v-for="offer in offers"
               :offer="offer" 
               :key="offer.id"
               :updateOffer="updateOffer"
            />
      </div>
   </div>
</template>

<style>
   .offer-container{
      width: 100%;
      background-image: url(../assets/images/feeds-background.jpg);
      background-size: cover;
      min-height: 100vh;
   }
   
   .offer-container .message-container{
      background-color: var(--kinda-white);
      box-shadow: -1px 3px 11px 3px rgba(110, 107, 107, 0.35);
      width: 300px;
      margin: 2rem auto;
   }

   .offers{
      max-width: 1200px;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
      padding: 2rem;
      margin: 0 auto;
   }

   .offer-container h2{
      text-align: center;
      text-decoration: underline;
   }

   @media screen and (max-width: 700px) {
      .offers{
         padding: 2rem;
         margin: 0 auto;
      }
   }

   @media screen and (max-width: 400px) {
      .offers{
         grid-template-columns: 1fr;
         padding: 2rem 1rem;
      }
   }
</style>