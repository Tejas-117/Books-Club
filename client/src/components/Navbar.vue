<script setup>
  import store from "../state/store";
  import { useRouter } from "vue-router";

  const router = useRouter();

  function handleLogout(event){
    store.logout();

    // after logging out redirect the user to login page.
    router.push('/login');
  }

  function updateSearchText(event){
    // update searchText in gloabl state and redirect to 'feeds' page.
    const searchText = event.target.value;
    store.searchText = searchText.toLowerCase().trim();
    router.push('/feeds');
  }

  function expandMobileNavbar(){
      const containerEle = document.querySelector('.hamburger-menu-container');
      containerEle.classList.toggle('reveal-mobile-navbar');
  }
</script>

<template>  
  <div class="nav-bar">
    <div class="header-logo" @click="router.push('/')">
        <div class="logo-background">
          <img class="logo-component-a" src="../assets/images/Book-Club-logo-component1.svg">
          <img class="logo-component-b" src="../assets/images/Book-Club-logo-component2.svg">
          <img class="logo-component-c" src="../assets/images/Book-Club-logo-component3.svg">
          <div class="logo-component-d"> Homepage </div>
        </div>
    </div>

    <div class="tablet-mobile-logo" @click="router.push('/')">
      <img class="mobile-tablet-header-icon"  src="../assets/images/LOGO-shorthand.svg" alt="">
    </div>
    
    <div class="mids">
      <input @input="updateSearchText($event)" class="searchbar" type="text" placeholder="Search books">
    </div>

    <div class="rhs-part">
      <div class="button-container" @click="router.push('/feeds')">
        <button class="nav-button">
          <img class="button-img" src="../assets/images/FeedSymbol.svg" alt="">
          <span class="button-label">Feeds</span>
        </button>
      </div>

      <div class="button-container" @click="router.push('/books/upload')">
          <button class="nav-button">
            <img class="button-img" id="upload-icon" src="../assets/images/UploadSymbol.svg" alt="">
            <span class="button-label">Upload</span>
          </button>
      </div>

      <div v-if="store?.user" class="button-container" @click="handleLogout">
        <button class="nav-button">
          <img class="button-img" src="../assets/images/LogoutSymbol.svg" alt="">
          <span class="button-label">Logout</span>
        </button>
      </div>

      <div v-if="store?.user" class="button-container">
        <RouterLink :to="`/users/profile/${store.user.user_id}`" :style="{ textDecoration: 'none'}">
          <button class="nav-button">
            <img v-if="store.user.profile" class="button-img" :src="store.user.profile" alt="">
            <img v-else class="button-img" src="../assets/images/default-profile.png" alt="">
            <span class="button-label">Profile</span>
          </button>
        </RouterLink>
      </div>
      
      <div v-if="!store.user" class="button-container" @click="router.push('/login')">
          <button class="nav-button">
            <img :style="{ background: 'black' }" class="button-img" src="../assets/images/LoginSymbol.svg" alt="">
            <span class="button-label">Login</span>
          </button>
      </div>
    </div>

    <button class="mobile-hamburger-menu" @click="expandMobileNavbar">
      <img class="hamburger-menu-img" src="../assets/images/hamburger-menu-icon.svg" alt="">
    </button>

    <div class="hamburger-menu-container">
      <button class="hamburger-button"  @click="expandMobileNavbar">
        <img class="hamburger-icon" src="../assets/images/hamburger-cancel-icon.svg">
        <span class="hamburger-button-label">Close</span>
      </button>

      <div class="hamburger-mids">
        <input @input="updateSearchText($event)" class="hamburger-searchbar" type="text" placeholder="Search books">
      </div>

      <button v-if="store?.user" class="hamburger-button">
        <RouterLink :to="`/users/profile/${store.user.user_id}`">
          <img v-if="store.user.profile" class="hamburger-icon" :src="store.user.profile">
          <img v-else class="hamburger-icon" src="../assets/images/default-profile.png">
          <span class="hamburger-button-label">Profile</span>
        </RouterLink>
      </button>

      <RouterLink to="/feeds">
        <button class="hamburger-button">
          <img class="hamburger-icon" src="../assets/images/hamburger-feeds-icon.svg">
          <span class="hamburger-button-label">Feeds</span>
        </button>
      </RouterLink>

      <RouterLink :to="`/books/upload`">
        <button v-if="store?.user" class="hamburger-button">
          <img class="hamburger-icon" src="../assets/images/hamburger-upload-icon.svg">
          <span class="hamburger-button-label">Upload</span>
        </button>
      </RouterLink>
      
      <button v-if="store?.user" class="hamburger-button" @click="handleLogout">
        <img class="hamburger-icon" src="../assets/images/hamburger-logout-icon.svg">
        <span class="hamburger-button-label">Logout</span>
      </button>
      
      <RouterLink v-else to="/login">
        <button class="hamburger-button">
          <img class="hamburger-icon" src="../assets/images/hamburger-profile-icon.svg">
          <span class="hamburger-button-label">Login</span>
        </button>
      </RouterLink>
    </div>
  </div>

</template>

<style>
.header-logo {
  display: flex;
  margin: 0px 10px 0px 0px;
  min-width: 300px;
  height: 30px;
}

.tablet-mobile-logo {
  display: none;
  align-items: center;
  justify-content: center;
  margin: 0px 20px;
}

.mobile-tablet-header-icon {
    height: 22px;
  }

.nav-bar {
  background-color: var(--kinda-black);
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  height: 60px;
  width: 100%;
  border: none;
  align-items: center;
  position: fixed;
  z-index: 1000;
}

.header-logo {
  padding: 0px 10px;
}

.logo-background {
  position: relative; 
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 128px;
  height:26px;
  background-color: var(--kinda-white);
  transition: all 0.35s;
}

.logo-background:hover {
  background-color: var(--kinda-black);
}

.logo-background:hover .logo-component-d {
  left: 55px;
  width: 81.36px;  
} 

.logo-background:hover .logo-component-c {
  transform: rotate(180deg);
}


.logo-component-a  {
  position: absolute;
  height: 26px;
  display: flex;
  padding: 0px 10px;
  align-self: center;
  cursor: pointer;
}

.logo-component-b {
  position: absolute;
  height: 26px;
  z-index: 2;
  left:19px;
}

.logo-component-b:hover {
  cursor:pointer;
}

.logo-component-c {
  position: absolute;
  z-index: 3;
  width: 16px;
  left: 27.8px;
  top: 8.5px;
  transition: all 0.35s ;
}

.logo-component-d {
  z-index: 1;
  position: absolute;
  left: 20px; 
  width: 20px;
  overflow: hidden;
  top: 4.7px;
  display: flex;
  background-color: transparent;
  font-weight: 600;
  font-size: 12px;
  padding: 0px 6px;
  border-radius : 14px;
  color: var(--kinda-white);
  border: solid 1px var(--kinda-white);
  transition: all 0.4s;
}

.logo-component-d:hover {
  background-color: var(--kinda-white);
  color: var(--kinda-black);
  cursor: pointer;
}

.logo-title {
  font-size: 22px;
  font-weight: 700;
  height: 30px;
  color: var(--kinda-white);
}

.mids {
  display: flex;
  flex-direction: row;
  align-self: center;
  max-height: 60px;
}

.searchbar {
  background-color: var(--kinda-white);
  height: 32px;
  width: 260px;
  border-radius: 25px;
  padding: 0px 20px;
  color: var(--kinda-black);
  transition: all 0.35s;
}

.searchbar:focus {
  border-radius: 4px;
  outline: none;
  border-left: solid 4px var(--very-close-black);
}

.search-button {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 30px;
  width: 30px;
  margin: 0px 20px;
  background-color: var(--kinda-white);
  border-radius: 15px;
}

.search-symbol-pic {
  width: 24px;
  border-radius: 15px;
  border: none;
  margin: none;
}

.rhs-part {
  display: flex;
  flex-direction: row;
  max-height: 60px;
  width: 300px;
  justify-content: flex-end;
  margin-right:10px;
}

.button-container {
  display: inline-flex;
  margin: 0px 10px;
}

.nav-button {
  display: flex;
  align-items: center;
  background-color: var(--kinda-white);
  border-radius: 15px;
  padding: 0px;
  width: 30px;
  transition: all 0.35s ;
  overflow:hidden;
  cursor: pointer;
}

.nav-button:hover {
  width: 100px;
  color:var(--kinda-black);
}


.button-img {
  width: 30px;
  height: 30px;
  transition: all 0.35s ease-in;
  border-radius: 50%;
}

.button-label {
  margin: 0px 10px;
  background-color: var(--kinda-white);
  color: inherit;
  font-weight: bold;
}

.mobile-hamburger-menu {
  position: relative;
  background-color: transparent;
  padding: 0px;
  display:none;
  margin: 0px 20px;
}

.hamburger-menu-img {
  height: 20px;
}

.hamburger-menu-container {
  width: 160px;
  position: absolute;
  right: -160px;
  top: 0;
  z-index:4;
  display: flex;
  flex-direction: column;
  transition: all 0.35s ease-out;
}

.hamburger-button {
  display: flex;
  align-items: center;
  justify-content: center;;
  background-color: var(--kinda-black);
  color:var(--kinda-white);
  opacity: 95%;
  padding: 10px 20px;
  cursor: pointer;
}

.hamburger-button a {
  text-decoration: none;
  display: flex;
  align-items: center;
  justify-content: center;;
  background-color: var(--kinda-black);
  color:var(--kinda-white);
  opacity: 95%;
}

.hamburger-button a img {
  border-radius: 50%;
}

.hamburger-icon {
  height: 22px;
  margin: 0px 10px; 
}

.hamburger-button-label {
  padding: 0px 10px;
  font-size: 18px;
  font-weight: 500;
  color: var(--kinda-white);
}

.hamburger-mids {
  padding: 10px;
  background-color: var(--kinda-black);
  opacity: 95%;
}

.hamburger-searchbar {
  width: 100%;
  height: 30px;
  border-radius: 20px;
  padding: 0px 10px;
  transition: all 0.35s;
}

.hamburger-searchbar:focus {
  border-radius: 4px;
  border-left: solid 4px #76B900;
  outline: none;
}

.reveal-mobile-navbar{
  right: 0px;
}

/* TODO: Make Navbar responsive */
@media screen and (max-width:900px) {
  
  .header-logo {
    display: none;
  }

  .tablet-mobile-logo {
    display: flex;
  }

  .rhs-part {
    display:none;
  }

  .mobile-hamburger-menu {
    display: flex;
  }

  .hamburger-mids {
    display:none;
  }
}

@media screen and (max-width:500px) {


  .mids {
    position: relative;
  }

  .searchbar {
    display:none;
  }

  .hamburger-mids {
    display: flex;
  }
}
</style>
