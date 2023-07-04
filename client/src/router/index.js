import { createRouter, createWebHistory } from 'vue-router'
import store from '../state/store';

import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import Feeds from "../views/Feeds.vue";
import BookPost from "../views/BookPost.vue";
import UploadBook from "../views/UploadBook.vue";
import UserProfile from "../views/UserProfile.vue";
import EditUserProfile from "../views/EditUserProfile.vue";
import EditBook from "../views/EditBook.vue";
import Offers from "../views/Offers.vue";
import AboutUs from "../views/AboutUs.vue";

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home // 'home' page
  },
  {
    path: '/login',
    name: 'login',
    component: Login // 'login' page
  },
  {
    path: '/register',
    name: 'register',
    component: Register // 'register' page
  },
  {
    path: '/feeds',
    name: 'feeds',
    component: Feeds // 'feeds' page
  },
  {
    path: '/books/upload',
    name: 'uploadBook',
    component: UploadBook // 'upload book' page
  },
  {
    path: '/books/:id',
    name: 'bookPost',
    component: BookPost // 'post' page
  },
  {
    path: '/books/:id/edit',
    name: 'editBookPost',
    component: EditBook, // 'edit book' page
  },
  {
    path: '/users/profile/:id',
    name: 'userProfile',
    component: UserProfile // user 'profile' page
  },
  {
    path: '/users/profile/:id/edit',
    name: 'editUserProfile',
    component: EditUserProfile, // edit 'profile' page
    beforeEnter: (to, from) => {
      // allow only user to edit their profile.
      if(to.params.id != store.user.user_id){
        return false;
      }

      return true;
    }
  },
  {
    path: '/offers',
    name: 'viewOffers',
    component: Offers // view 'offers' page
  },
  {
    path: '/about-us',
    name: 'aboutUs',
    component: AboutUs // 'about-us' page
  }
];

const history = createWebHistory();

const router = createRouter({
  history, routes
})

router.beforeEach((to, from) => {
  // Perform 'user-authentication' based on state and 'protect' routes.

  // Routes which should be only accessed by authenticated users.
  const protectedRoutes = [
    '/books/upload', 
    '/books/:id', 
    '/books/:id/edit',
    '/users/profile/:id',
    '/users/profile/:id/edit',
    '/offers'
  ];
  
  // if user is not authenticated, do not allow to visit 'protectedRotues'. 
  if (store.user === null){
    for (const protectedRoute of protectedRoutes) {
      if(to.matched[0].path === protectedRoute){
        return { path: '/login' };
      }
    }
  }

  return true;
})

export default router;