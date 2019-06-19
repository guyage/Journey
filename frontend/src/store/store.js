/*jshint esversion: 6 */
import Vue from 'vue'
import Vuex from 'vuex'
import user from './modules/user.js'
import tagsview from './modules/tagsview.js'

import getters from './getters.js'
Vue.use(Vuex)

const store = new Vuex.Store({
    modules : {
        user,
        tagsview,
    },
    getters
})


export default store;