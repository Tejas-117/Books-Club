<template>
   <div class="footer-container">
      <div class="footer-logo-title-container">
         <img src="../assets/images/LOGO-shorthand.svg" alt="" class="footer-logo">
         <div class="footer-logo-title">the book club</div>
      </div>
      <div class="footer-links">
         <div class="footer-link-title"><a class="footer-link-tag" href="">About us</a></div>
         <div class="footer-link-title"><a class="footer-link-tag" href="">Help</a></div>
         <div class="footer-link-title"><a class="footer-link-tag" href="">Terms & Conditions</a></div>
      </div>
   </div>
</template>

<style>   
.footer-container {
   display: flex;
   flex-direction: row;
   justify-content: space-between;
   background-color: var(--kinda-black);
   height: 60px;
   align-items: center;
   color: var(--kinda-white); 
   width: 100%; 
   margin-top: auto;
}

.footer-logo-title-container {
   display:flex;
   flex-direction: row;
   align-items: center;
} 

.footer-logo {
   height: 20px;
   margin: 0px 10px;
}

.footer-logo-title {
   font-size: 16px;
   color: var(--kinda-white);
}

.footer-links {
   margin: 0px 10px;
   display: flex;
   flex-direction: row;
}

.footer-link-title {
   font-size: 16px;
   margin: 0px 30px;
   text-decoration: none;
   color: var(--kinda-white);
   
}

.footer-link-title:hover {
   text-decoration: underline;
}

.footer-link-tag {
   text-decoration: none;
   color: var(--kinda-white);
}

@media screen and (max-width: 600px) {

   .footer-logo-title-container {
      margin-bottom: 30px;
   }

   .footer-logo {
      margin: 0px 10px 0px 0px;
   }

   .footer-logo-title {
      font-size: 18px;

   }

   .footer-links {
      flex-direction: column;
      justify-content: center;
      align-items: center;
   }

   .footer-link-title {
      margin : 10px 0px;
   }

   .footer-container {
      flex-direction: column;
      height: auto;
      padding: 20px 0px;
   }

}

</style>
