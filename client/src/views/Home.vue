<script setup>
   import { onMounted, onUnmounted } from 'vue';
   import { RouterLink } from 'vue-router';

   // function to animate scroll
   function animateElementsOnScroll(e){
      // get all containers that should be animated.
      const allContainers = document.querySelectorAll('.home-sub-section');

      const windowHeight = window.innerHeight;
      const elementVisibleHeight = 100;
      
      // for each container if the container top reaches certain level, animate it.
      allContainers.forEach(container => {
         const containerTopHeight = container.getBoundingClientRect().top;

         if((windowHeight - elementVisibleHeight) > containerTopHeight){
            container.classList.add('home-sub-section-active');
         } else {
            container.classList.remove('home-sub-section-active');            
         }
      })
   }

   onMounted(() => {
      // add eventListener to animate on scroll on 'mount'
      window.addEventListener('scroll', animateElementsOnScroll);
   })

   onUnmounted(() => {
      // remove event listener on 'onmount'
      window.removeEventListener('scroll', animateElementsOnScroll);
   })

</script>

<template>
   <div class="home-content-container">
      <div class="home-top-stuff">
         <div class="top-lhs">
            <h1 class="home-intro-title">
               Presenting, a platform meant for book enthusiast
            </h1>

            <div class="intro-info-container">
               <h2 class="home-intro-sub">
                  A place like never before for book enthusiast to rule on.
               </h2>

               <p class="home-intro-desc">
                  A social media website based on books where you can upload the books you have to sell, exchange or give it away for free.
                  Meet people with similar book interests &amp; exchange books with them. Explore and hear people's reviews of books.
               </p>
            </div>
         </div>
         <div class="home-top-rhs">
            <div class="home-intro-img-container">
               <img class="home-intro-img" src="../assets/images/home-intro-logo.svg">
            </div>
         </div>
      </div>

      <div class="home-container-a home-sub-section">
         <div class="home-feeds-lhs">
            <h1 class="home-title">
               Look out for your favourites...
            </h1> 

            <p class="home-feature-desc">
               Have a look at the uploads of other book club users worldwide. Add filters to your search and search the book
               you need by its name and author.
            </p>
         </div>

         <div class="home-feeds-rhs">
               <img class="homepage-feeds-img" src="../assets/images/homepage-feeds-img.svg">
         </div>
      </div>

      
      <div class="home-container-b home-sub-section">
         <div class="home-postview-lhs">
            <img class="homepage-postview-img" src="../assets/images/homepage-postview-img.svg" alt="">
         </div>

         <div class="home-postview-rhs">
            <h1 class="home-title">
               Check out the details of the uploaded books
            </h1>

            <p class="home-feature-desc">
               Check out the details of the book you like as a post in the book club's post view page.
               Get to know the genre and the uploaders opinion on the book you like. Upload a book you want to sell, exchange or give away
               to other book club users.
            </p>
         </div>
      </div>

      <div class="home-container-a home-sub-section">
         <div class="home-comments-lhs">
            <h1 class="home-title">
               Speak out your opinion on the book
            </h1>

            <p class="home-feature-desc">
               Let others know your opinion on the uploaded book via comments feature.
               Check out other's opinion on the book in the comments section.
            </p>
         </div>

         <div class="home-comments-rhs">
            <img class="homepage-comments-img" src="../assets/images/homepage-comments-img.svg" alt="">
         </div>
      </div>

      <div class="home-container-b home-sub-section">
         <div class="home-profile-rhs">
            <img class="homepage-profile-img" src="../assets/images/homepage-profile-img.svg" alt="">
         </div>

         <div class="home-profile-lhs">
            <h1 class="home-title">
               Define yourself to others and vice versa...
            </h1>

            <p class="home-feature-desc">
               Maintain your own profile. Get to know other users by looking at their interests 
               in their profiles and meet with the people you share similar interests.
            </p>
         </div>
      </div>

      <div class="home-container-a home-sub-section">
         <div class="home-offers-lhs">
            <h1 class="home-title">
               Buy, Sell, Exchange or giveaway !
            </h1>

            <p class="home-feature-desc">
               Sell your uploaded books, trade it or give it away for free to other users 
               and buy, exchange or request books uploaded by other users for free.  
            </p>
         </div>

         <div class="home-offers-rhs">
            <img class="homepage-offers-img" src="../assets/images/homepage-offers-img.svg" alt="">
         </div>
      </div>

      <div class="join-us-container">
         <h1 class="join-title">
            Join our journey. Become a member of the Book Club today. 
         </h1>

         <RouterLink to="/register">
            <button class="homepage-register-button">
               Join Now
            </button>
         </RouterLink>
      </div>
   </div>
</template>


<style>

   *{
      color: var(--kinda-white);
   }

   .home-content-container {
      padding: 80px 20px 20px 20px;
      background-color: var(--kinda-black);
   }

   .home-intro-title {
      font-size: 48px;
      margin-bottom: 50px;
      color: var(--kinda-white);
   }

   .home-top-stuff {
      display: grid;
      grid-template-columns: 4.8fr 3fr;

   }

   .home-top-rhs {
      display: grid;
      justify-content: center;
      align-items: center;
   }

   .intro-info-container {
      display: relative;
      display: flex;
      flex-direction: column; 
      padding: 50px 0px;
   }

   .home-intro-sub {
      font-size: 28px;
      display: flex;
      color: var(--kinda-white);
      padding-left: 4%;
   }

   .home-intro-desc {
      max-width: 110vh;
      font-size: 16px;
      margin: 20px 0px;
      color: var(--kinda-white);
      padding-left: 4%;
   }

   .home-intro-img-container {
      top: 140px;
      right: 0px;
      display: flex;
   }

   .home-intro-img {
      height: 500px;
      width: 500px;
      object-fit: contain;
      object-position: top;
      padding: 0px;
   }

   .home-container-a {
      display: grid;
      grid-template-columns: 3fr 2fr;
      column-gap: 20px;
      padding: 20px;
      height: 340px;
      align-items: center;
      margin: 25px 0px;
      border-radius: 10px;
      background-image: linear-gradient(-45deg, #6495ed,#D0DFF9);
   }

   .home-container-b {
      display: grid;
      grid-template-columns: 2fr 3fr;
      column-gap: 20px;
      padding: 20px;
      height: 340px;
      align-items: center;
      margin: 25px 0px;
      border-radius: 10px;
      background-image: linear-gradient(-45deg ,#4cb7ad,#B7E2DE );
   }

   .home-sub-section{
      position: relative;
      transform: translateY(150px) scale(0.9);
      opacity: 0;
      transition: 0.5s all linear;
   }

   .home-sub-section-active{
      opacity: 1;
      transform: translateY(0px) scale(1);
   }

   .home-sub-section-active .homepage-feeds-img{
      object-position: bottom;
   }
   
   .home-sub-section-active .homepage-postview-img{
      object-position: right;
   }

   .home-title {
      font-size: 28px;
      display: flex;
      padding-left: 4%;
   }

   .home-feature-desc {
      font-size: 16px;
      margin: 20px 0px;
      padding-left: 4%;
   }

   .home-feeds-rhs {
      width: 100%;
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: center;
      transition: all 0.35s;
   }

   .homepage-feeds-img {
      object-fit:cover ;
      object-position: top;
      width: 400px;
      height: 300px;
      transition: all 1.5s;
   }


   .home-postview-lhs {
      display: grid;
      justify-content: center;
   }


   .homepage-postview-img {
      height:300px; 
      width: 550px;
      object-fit: cover;
      object-position: left;
      transition: all 2.4s;
   }

   .home-comments-rhs {
      display: grid;
      justify-content: center;
      align-items: center;
   }
   
   .homepage-comments-img {
      width: 500px;
      height: 300px;
      object-fit: cover;
      object-position: bottom right;
   }
   
   .home-profile-rhs {
      display: grid;
      justify-content: center;
      align-items: center;
   }

   .homepage-profile-img {
      width: 500px;
      height: 300px;
      object-fit: contain;
   }

   .home-offers-rhs {
      display: grid;
      justify-content: center;
      align-items: center;
   }

   .homepage-offers-img {
      height: 300px;

   }

   .join-us-container {
      display: flex;
      flex-direction: column;
      padding: 20px;
      height: 340px;
      align-items: center;
      margin: 20px 0px;
   }

   .join-us-container a{
      margin: 40px 0;
   }

   .join-title {
      font-size: 40px;
      color: var(--kinda-white);
   }


   .homepage-register-button {
      padding: 8px 20px;
      border: solid 2px var(--kinda-white);
      font-size: 20px;
      font-weight: 600;
      background-color: var(--kinda-white);
      border-radius: 30px;
      width: 300px;
      transition: all 0.35s;
      text-decoration: none;
   }

   .homepage-register-button:hover {
      background-color: var(--kinda-black);
      border-color: var(--kinda-white);
      color: var(--kinda-white);
      cursor: pointer;
   }

   @media screen and (max-width: 930px) {
      
      .home-intro-title {
         font-size: 40px;
      }

      .home-intro-sub {
         font-size: 20px;
      }

      .home-intro-desc {
         font-size: 12px;
      }

      .home-intro-img {
         height: 250px;
         width: 250px;
      }

      .home-container-a {
         display: flex;
         flex-direction: column;
         height: 100%;
      }

      .home-container-b {
         display: flex;
         flex-direction: column-reverse;
         height: 100%;
      }

      .home-title {
         font-size: 24px;;
      }

      .home-feature-desc {
         font-size: 14px;
      }

      .homepage-feeds-img {
         width: 240px;
         height: 200px;
      }

      .homepage-postview-img {
         height: 160px;
         width: 260px;
      }

      .homepage-profile-img {
         height: 300px;
         width: 260px;
      }

      .homepage-comments-img {
         width: 240px;
         height: 150px;
      }

      .homepage-offers-img {
         height: 150px;
      }


   }

   @media screen and (max-width: 500px) {

      .home-intro-img-container {
         display: none;
      }

      .home-top-stuff {
         display: flex;
      }

      .home-intro-title {
         font-size: 30px;
      }

      .home-top-rhs {
         display: none;
      }


      .join-title {
         font-size: 30px;
      }

      .homepage-register-button {
         width: 200px;
         font-size: smaller;
      }
   }

</style>
