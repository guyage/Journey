/*jshint esversion: 6 */
import {Menus} from '@/global/config.js'
import { getCookies, setCookies, removeCookies } from '@/utils/auth.js'

const MenuKey = 'menus'
const RouterNameKey = 'routers'

const permissions = {
    state: {
        menus: '',
        routers: []
    },

    mutations: {
        SET_ROUTERS: (state, routers) => {
            state.routers = routers
        },
        SET_MENUS: (state, menus) => {
            state.menus = menus
        }
    },
    actions: {
        GenerateRoutes({commit}, RouterMap) {
            return new Promise(resolve => {
                if (RouterMap.roles == 'admin') {
                    // setCookies(RouterNameKey,RouterMap.dynamicrouter)
                    // localStorage.setItem(RouterNameKey,JSON.stringify(RouterMap.dynamicrouter));
                    // setCookies(RouterNameKey,RouterMap.dynamicrouter)
                    commit('SET_ROUTERS', RouterMap.dynamicrouter)
                    
                } else {
                    var devrouter = RouterMap.dynamicrouter
                    for (var index in devrouter) {
                        var temprouter = devrouter[index].children.filter( i => i.meta.roles === 'dev')
                        devrouter[index].children = temprouter
                        // setCookies(RouterNameKey,devrouter)
                        commit('SET_ROUTERS', devrouter)
                    }
                }
                resolve()
            })
        },
        GenerateMenus({commit}, roles) {
            return new Promise(resolve => {
                if (roles == 'admin') {
                    // setCookies(MenuKey,AdminMenus)
                    commit('SET_MENUS', Menus)
                }
                else {
                    // setCookies(MenuKey,NoramalMenus)
                    commit('SET_MENUS', Menus)
                }
                resolve()
            })
        }
    }
}


export default permissions