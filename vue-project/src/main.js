import './assets/main.css'

import {createApp} from 'vue'
import App from './App.vue'
import router from './router'
import store from '@/router/store';

//Element
import ElementPlus from 'element-plus'
import 'element-plus/theme-chalk/base.css'
import 'element-plus/dist/index.css'

//authing
import {createGuard} from "@authing/guard-vue3";

//sign pad
import VueSignaturePad from 'vue-signature-pad';


const app = createApp(App)


//Element
app.use(ElementPlus)

//sign pad
app.use(VueSignaturePad)


app.use(router)
app.use(store);

//authing
app.use(
    createGuard({
        appId: "62fc94595854df71f7bbe61e",
    })
);

app.mount('#app')
