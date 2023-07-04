<script setup>
   import { ref } from 'vue';

   const props = defineProps({
      offer: Object,
      updateOffer: Function
   });

   const offer = ref(props.offer);
</script>

<template>
   <div class="offer">
      <div class="offer-book-info">
         <p>
            <span class="label">My book:</span>
            <RouterLink :to="`/books/${offer.posted_book.id}`">
               {{ offer.posted_book.title }}
            </RouterLink>
         </p>
         <p v-if="offer.exchange_book">
            <span class="label">Exchange book:</span> 
            <RouterLink :to="`/books/${offer.exchange_book.id}`">
               {{ offer.exchange_book.title }}
            </RouterLink>
         </p>
         <p>
            <span class="label">Status:</span>
            <span :class="offer.status">{{ offer.status }}</span>
         </p>
         <p>
            <span class="label">Offer Posted on:</span>
            {{ offer.created_on }}
         </p>
      </div>

      <div class="purchase-info">
         <p><span class="label">Purpose: </span> 
            {{ offer.for_purchase ? (offer.price > 0) ? 'Sell' : 'Give away' : 'Exchange' }}
         </p>
         <p v-if="offer.for_purchase">
            <span class="label">Price:</span>
            {{ '₹ ' + offer.price }}
         </p>
      </div>
      
      <div class="buyer-info">
         <p>
            <span class="label">Buyer:</span>
            <RouterLink :to="`/users/profile/${offer.buyer.id}`">
               {{ offer.buyer.first_name + ' ' + offer.buyer.last_name }}
            </RouterLink>
         </p>
         <p>
            <span class="label">Message:</span>
            {{ offer.description }}
         </p>
      </div>

      <div class="action-btns">
         <button v-if="(offer.status === 'processing') || (offer.status === 'rejected')" class="accept-btn" @click="updateOffer($event, offer.id, 'accepted')">Accept</button>
         <button v-if="(offer.status === 'processing') || (offer.status === 'accepted')" class="reject-btn" @click="updateOffer($event, offer.id, 'rejected')">Reject</button>
      </div>
   </div>
</template>

<style>
   .offer{
      display: flex;
      flex-direction: column;
      justify-content: center;
      margin: 1rem;
      /* border: 2px solid var(--kinda-grey); */
      box-shadow: -1px 3px 8px -1px rgba(0,0,0,0.5);
      padding: 1rem;
      background-color:  var(--kinda-white);
      border-radius: 6px;
   }

   .offer-book-info{
      border: 1px solid var(--kinda-grey);
      padding: 5px;
      border-radius: 5px;
   }

   .purchase-info{
      margin: 10px 0;
      border: 1px solid var(--kinda-grey);
      padding: 5px;
      border-radius: 5px;
   }

   .buyer-info{
      border: 1px solid var(--kinda-grey);
      padding: 5px;
      border-radius: 5px;
   }

   .label{
      font-weight: bold;
      text-decoration: none;
      margin-right: 10px;
   }

   .offer p{
      display: flex;
      margin: 5px 0;
   }

   .processing, .accepted, .rejected{
      color: white;
      padding: 2px 5px;
      border-radius: 5px;
   }

   .processing{
      background-color: blue;
   }

   .rejected{
      background-color: red;
   }

   .accepted{
      background-color: green;
   }

   .action-btns{
      display: flex;
      flex-direction: column;
   }

   .offer button{
      color: white;
      padding: 5px 10px;
      border-radius: 5px;
      margin: 5px 0;
      cursor: pointer;
   }

   .accept-btn{
      background-color: green;
   }
   
   .reject-btn{
      background-color: red;
   }
</style>