/*jshint esversion: 6 */
import { getCookies, setCookies, removeCookies } from '@/utils/auth.js';
import { Login, LdapAuth } from '@/api/api.js';
import { Menus } from '@/global/menu.js';

const TokenKey = 'Authorization'
const UserNameKey = 'username'
const UserGroupKey = 'usergroup'
const UserIsSuperKey = 'userissuper'
const UserPermissionsGroupKey = 'userpermissionsgroup'
const MenuKey = 'menus'
const RouterNameKey = 'routers'

const user = {
    state: {
        username: '',
        usergroup: '',
        userissuper: getCookies(UserIsSuperKey),
        token: getCookies(TokenKey),
        menus: '',
        routers: [],
        userpermissionsgroup: []
    },


    mutations: {
        SET_TOKEN : (state, token) => {
            state.token = token
        },
        SET_USERNAME : (state, username) => {
            state.username = username
        },
        SET_ISSUPER : (state, userissuper) => {
            state.userissuper = userissuper
        },
        SET_USERGROUP : (state, usergroup) => {
            state.usergroup = usergroup
        },
        SET_USERPERMISSIONSGROUP : (state, userpermissionsgroup) => {
            state.userpermissionsgroup = userpermissionsgroup
        },
        SET_ROUTERS: (state, routers) => {
            state.routers = routers
        },
        SET_MENUS: (state, menus) => {
            state.menus = menus
        },
    },

    actions: {
        GenerateRoutes({commit}, RouterMap) {
            return new Promise(resolve => {
                if (RouterMap.issuper) {
                    // setCookies(RouterNameKey,RouterMap.dynamicrouter)
                    // localStorage.setItem(RouterNameKey,JSON.stringify(RouterMap.dynamicrouter));
                    // setCookies(RouterNameKey,RouterMap.dynamicrouter)
                    commit('SET_ROUTERS', RouterMap.dynamicrouter)
                } else {
                    var devrouter = RouterMap.dynamicrouter
                    for (var index in devrouter) {
                        var temprouter = devrouter[index].children.filter( i => i.meta.issuper === false)
                        devrouter[index].children = temprouter
                        // setCookies(RouterNameKey,devrouter)
                    }
                    commit('SET_ROUTERS', devrouter)
                }
                resolve()
            })
        },
        GenerateMenus({commit}, issuper) {
            return new Promise(resolve => {
                if (issuper) {
                    // setCookies(MenuKey,AdminMenus)
                    commit('SET_MENUS', Menus)
                }
                else {
                    commit('SET_MENUS', Menus.filter(item => item.issuper === false));
                }
                resolve()
            })
        },
        NormalLogin ({commit}, userinfo) {
            return new Promise((resolve, reject) => {
                Login(userinfo).then((response) => {
                    commit('SET_TOKEN',response.data.token);
                    commit('SET_USERNAME',response.data.username);
                    commit('SET_ISSUPER',response.data.is_superuser);
                    setCookies(TokenKey,response.data.token);
                    setCookies(UserNameKey,response.data.username);
                    setCookies(UserIsSuperKey,response.data.is_superuser);
                    resolve(response);
                }).catch(error => {
                    reject(error)
                })
            })
        },
        Logout({commit}) {
            return new Promise((resolve, reject) => {
                commit('SET_MENUS', '');
                commit('SET_ROUTERS', []);
                removeCookies(UserIsSuperKey);
                removeCookies(UserNameKey);
                removeCookies(TokenKey);
                resolve()
            })
        },
        SetUserInfo ({commit}, userinfo) {
            commit('SET_USERNAME',userinfo.username)
        },
        LdapLoginIn({commit}, userinfo) {
            return new Promise((resolve, reject) => {
                LdapAuth(userinfo).then((response) => {
                    if (response) {
                        setCookies(TokenKey,response.data.token);
                        setCookies(UserNameKey,response.data.username);
                        setCookies(UserIsSuperKey,response.data.is_superuser);
                        commit('SET_ISSUPER',response.data.is_superuser);
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
    }
}

export default user;