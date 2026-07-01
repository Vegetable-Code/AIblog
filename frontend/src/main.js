 import { createApp } from 'vue'
 import { createPinia } from 'pinia'
 import App from './App.vue'
 import router from './router'
 import './style.css'
 import i18n, { initLocale } from './i18n'
 
 const app = createApp(App)
 app.use(createPinia())
 app.use(router)
 app.use(i18n)
 app.mount('#app')
 
 // Init locale detection (non-blocking)
 initLocale()
