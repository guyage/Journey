import Vue from 'vue'
import Vuex from 'vuex'
import user from './modules/user.js'
import permissions from './modules/permissions.js'
import tagsview from './modules/tagsview.js'
import getters from './getters.js'
Vue.use(Vuex)

const store = new Vuex.Store({
    modules : {
        user,
        tagsview
        // permissions
    },
    getters
})


export default store;