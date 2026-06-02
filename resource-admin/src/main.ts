import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import { useAdminStore } from './store/admin'

const app = createApp(App)
app.use(createPinia())
app.use(ElementPlus)
app.use(router)

// Init admin store
const adminStore = useAdminStore()
adminStore.init()

app.mount('#app')
