<script setup>
import { ref } from "vue";
import { RouterLink, useRouter, useRoute } from "vue-router";
import store from "../state/store";

// state to hold input fields
const email = ref('');
const password = ref('');
const loading = ref(false);
const message = ref('');

const router = useRouter();
const route = useRoute();

if (route.redirectedFrom) {
  message.value = 'Login to access that feature.'
}

// handle form submit
async function handleSubmit() {
  // set loading to true, since the next steps take some time and notify the user in UI.
  loading.value = true;
  message.value = '';

  const { data, error } = await store.login(email.value, password.value);

  // after completion above step, set loading to false.
  loading.value = false;

  if (error) {
    message.value = error.message;
  } else {
    message.value = 'Successfully logged in.'

    // redirect on successful login.
    setTimeout(() => {
      // redirect user to previous page they visited before landing on login page.
      if (route.redirectedFrom) {
        router.push(route.redirectedFrom);
      } else {
        router.replace('/');
      }
    }, 1500)
  }
}
</script>

<template>
  <div class="login-master-container content-container">
    <div class="login-box-form">
      <div class="login-left">
        <div class="logo-container">
          <img class="logo-img" src="../assets/images/LOGO.svg" alt="">
        </div>
        <div class="login-title-description">
          <p>A place for you to sell your old books and happiness... </p>
        </div>
      </div>

      <form class="login-right" @submit.prevent="handleSubmit">
        <div class="login-title-rhs">
          Login
        </div>

        <div class="no-account-text">
          <p class="no-account-text">Don't have an account?
            <RouterLink to="/register">Create Your Account</RouterLink>
          </p>
        </div>

        <div class="login-input-box-container">
          <div class="login-input-box-holder">
            Email
          </div>
          <input class="login-input-box" type="email" placeholder="Enter your email" v-model="email">
          <br>
          <div class="login-input-box-holder">
            Password
          </div>
          <input class="login-input-box" type="password" placeholder="password" v-model="password">
          <div class="forgot-password">
            forgot password ?
          </div>

          <div class="message-container">
            <span v-if="loading" class="loader"></span>
            <span v-if="message" class="message">{{ message }}</span>
          </div>

          <div class="login-button-container">
            <button class="login-button" type="submit">Login</button>
          </div>
        </div>
      </form>
    </div>
  </div>


</template>

<style>
  .login-master-container {
    background-image: url(../assets/images/Books-image.jpg);
    background-size: cover;
    width: 100%;
    row-gap: 30px;
    min-height: 100vh;
  }

  .login-master-container .message-container{
    width: 95%;
  }

  .login-box-form {
    display: grid;
    grid-template-columns: 1fr 1fr;
    align-self: center;
    justify-content: center;
    width: clamp(200px, 800px, 80vw);
    margin: 10vh auto;
  }

  /* left-side of the container */

  .login-left {
    background-color: var(--kinda-black);
    padding: 0px 30px;
    border-radius: 10px 0px 0px 10px;
  }

  .logo-container {
    margin: 40px 0 0;
  }

  .logo-img {
    width: 80%;
  }

  .login-title-description {
    margin: 10px 0;
    font-weight: 550;
    color: var(--kinda-white);
  }

  .login-title-description p{
    color: inherit;
  }

  /* right-side of the container  */

  .login-right {
    display: grid;
    background-color: var(--kinda-white);
    justify-content: center;
    padding: 50px;
    border-style: solid;
    border-radius: 0px 10px 10px 0px;
    border-color: var(--kinda-black);
  }

  .login-title-rhs {
    color: var(--kinda-black);
    font-weight: bold;
    font-size: 36px;
  }

  .no-account-text,
  .create-account {
    margin: 0 0 1rem;
    color: var(--kinda-black);
  }

  .login-input-box-container {
    display: flex;
    align-self: stretch;
    flex-direction: column;
    justify-items: center;
  }

  .login-input-box-holder {
    font-weight: 550;
    align-self: flex-start;
    color: var(--kinda-black);
  }

  .login-input-box {
    display: flex;
    width: 95%;
    margin: 10px 0px;
    border-style: solid;
    border-width: 1.6px;
    border-color: var(--kinda-grey);
    padding: 6px 8px;
    border-radius: 4px;
    color: var(--kinda-black);
    background-color: var(--kinda-white);
  }

  .forgot-password {
    color: var(--kinda-black);
    align-self: flex-end;
    font-size: 12px;
  }

  .login-button-container {
    display: flex;
    align-items: center;
    width: 100%;
  }

  .login-button {
    background-color: var(--kinda-black);
    color: var(--kinda-white);
    width: 100%;
    height: 34px;
    border-style: solid;
    border-width: 2px;
    border-color: var(--kinda-black);
    border-radius: 6px;
    font-size: 14px;
    font-weight: 550;
    transition: all 0.5s;
  }

  .login-button:hover {
    background-color: var(--kinda-white);
    color: var(--kinda-black);
    border-color: var(--kinda-black);
    font-weight: 600;
    cursor: pointer;
  }

  @media screen and (max-width: 700px){
    .login-box-form {
      grid-template-columns: 1fr;
      grid-template-rows: 200px 1fr;
      padding: 0;
    }

    .Login-img {
      width: 60%
    }

    .login-left{
      width: auto;
      border-radius: 10px 10px 0 0;
      text-align: center;

    }

    .login-right{
      border-radius: 0 0 10px 10px;
      padding: 20px 30px;
    }
  }
</style>