import './assets/css/main.css'
import 'bootstrap/dist/css/bootstrap.min.css'

import OpenLayersMap from 'vue3-openlayers'
import 'vue3-openlayers/styles.css';

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

export const piniaInstance = createPinia();

app.use(piniaInstance)
app.use(router)
app.use(OpenLayersMap);

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
        const isAuthenticated = localStorage.getItem('token');
        if (!isAuthenticated) {
            next({ name: 'login' })
        } else {
            next()
        }
    } else {
        next()
    }
});


app.mount('#app')


import 'bootstrap/dist/js/bootstrap.js'
