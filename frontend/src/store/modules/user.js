/*jshint esversion: 6 */
import { getCookies, setCookies, removeCookies } from '@/utils/auth.js'
import Axios from '@/utils/axios.js'
import {AdminMenus,NoramalMenus} from '@/global/config.js'

const TokenKey = 'Authorization'
const UserNameKey = 'username'
const UserGroupKey = 'usergroup'
const MenuKey = 'menus'
const RouterNameKey = 'routers'

const user = {
    state: {
        username: '',
        usergroup: '',
        token: getCookies(TokenKey),
        menus: '',
        routers: []
    },


    mutations: {
        SET_TOKEN : (state, token) => {
            state.token = token
        },
        SET_USERNAME : (state, username) => {
            state.username = username
        },
        SET_USERGROUP : (state, usergroup) => {
            state.usergroup = usergroup
        },
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
                    commit('SET_MENUS', AdminMenus)
                }
                else {
                    // setCookies(MenuKey,NoramalMenus)
                    commit('SET_MENUS', NoramalMenus)
                }
                resolve()
            })
        },
        NormalLoginIn ({commit}, userinfo) {
            return new Promise((resolve, reject) => {
                Axios.oPost('/login',userinfo).then((response) => {
                    if (response) {
                        setCookies(TokenKey,response.data.token);
                        setCookies(UserNameKey,response.data.username);
                        setCookies(UserGroupKey,response.data.group);
                        commit('SET_USERGROUP',response.data.group);
                        commit('SET_TOKEN',response.data.token);
                        commit('SET_USERNAME',response.data.username);
                        resolve();
                    } 
                    else  {
                        reject('Login Faild!')
                    }
                }).catch(error => {
                    reject(error)
                })
            })
        },
        LdapLoginIn({commit}, userinfo) {
            return new Promise((resolve, reject) => {
                Axios.oPost('/ldapauth',userinfo).then((response) => {
                    if (response) {
                        setCookies(TokenKey,response.data.token);
                        setCookies(UserNameKey,response.data.username);
                        setCookies(UserGroupKey,response.data.group);
                        commit('SET_USERGROUP',response.data.group);
                        commit('SET_TOKEN',response.data.token);
                        commit('SET_USERNAME',response.data.username);
                        resolve();
                    }
                    else  {
                        reject('Login Faild!')
                    } 
                }).catch(error => {
                    reject(error)
                })
            })
        },
        GetUserInfo ({commit}, username) {
            var url = '/userinfo/' + username + '/'
            return new Promise((resolve, reject) => {
                Axios.oGet(url).then((response) => {
                    if (response) {
                        setCookies(UserGroupKey,response.data.group)
                        commit('SET_USERGROUP',response.data.group)
                        resolve(response)
                    } 
                    else  {
                        reject('GetUserInfo Faild!')
                    }
                }).catch(error => {
                    reject(error)
                })
            })
        },
        
        SetUserInfo ({commit}, userinfo) {
            commit('SET_USERGROUP',userinfo.usergroup)
            commit('SET_USERNAME',userinfo.username)
        },
        LoginOut({commit}) {
            return new Promise((resolve, reject) => {
                commit('SET_MENUS', '');
                commit('SET_ROUTERS', []);
                removeCookies(UserGroupKey);
                removeCookies(UserNameKey);
                removeCookies(TokenKey);
                
                resolve()
            })
        }
    }
}

export default user;