// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'

import store from './store/store.js'
import router from './router/router.js';
// element 组件
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
// vue-codemirror 编辑组件
import VueCodemirror from 'vue-codemirror';
import 'codemirror/lib/codemirror.css';
// 阿里svg图标
import './assets/iconfont/iconfont.css';
import './assets/iconfont/iconfont.js';
import IconSvg from './components/iconsvg/IconSvg.vue';
// form making
import FormMaking from 'form-making'
import 'form-making/dist/FormMaking.css'
Vue.use(FormMaking)
//全局进度条
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
// 引入echarts
import echarts from 'echarts'
Vue.prototype.$echarts = echarts
//全局注册icon-svg
Vue.component('icon-svg', IconSvg)
//全局配置vue-codemirror
Vue.use(VueCodemirror)

Vue.use(ElementUI);

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
