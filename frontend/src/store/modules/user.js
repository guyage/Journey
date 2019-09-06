/*jshint esversion: 6 */
import { getCookies, setCookies, removeCookies } from '@/utils/auth.js';
import { Login, LdapAuth } from '@/api/api.js';
// import { Menus } from '@/global/menu.js';

const TokenKey = 'Authorization'
const UserNameKey = 'username'
const UserIsSuperKey = 'userissuper'
const UserPerms = 'userperms'
const MenuKey = 'menu'
const RouterKey = 'router'

const user = {
    state: {
        username: '',
        userissuper: getCookies(UserIsSuperKey),
        token: getCookies(TokenKey),
        menu: getCookies(MenuKey),
        router: [],
        userperms: getCookies(UserPerms),
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
        SET_ROUTER: (state, router) => {
            state.router = router
        },
        SET_MENU: (state, menu) => {
            state.menu = menu
        },
        SET_USERPERMS: (state, userperms) => {
            state.userperms = userperms
        },
    },

    actions: {
        GenerateRoutes({commit}, dynamicrouter) {
            let userrouter = getCookies(RouterKey)
            return new Promise(resolve => {
                let realrouter = dynamicrouter
                for (let index in realrouter) {
                    if (realrouter[index].children) {
                        let temprouter = realrouter[index].children.filter( i => userrouter.indexOf(i.path) >-1)
                        realrouter[index].children = temprouter
                    }
                }
                commit('SET_ROUTER',userrouter);
                resolve(realrouter)
            })
        },
        NormalLogin ({commit}, userinfo) {
            return new Promise((resolve, reject) => {
                Login(userinfo).then((response) => {
                    commit('SET_TOKEN',response.data.token);
                    setCookies(TokenKey,response.data.token);
                    commit('SET_USERNAME',response.data.username);
                    setCookies(UserNameKey,response.data.username);
                    commit('SET_ISSUPER',response.data.is_superuser);
                    setCookies(UserIsSuperKey,response.data.is_superuser);
                    // 菜单及路由及权限
                    commit('SET_MENU',response.data.menu);
                    setCookies(MenuKey,JSON.stringify(response.data.menu));
                    // commit('SET_ROUTER',response.data.router);
                    setCookies(RouterKey,JSON.stringify(response.data.router));
                    commit('SET_USERPERMS',response.data.perms);
                    setCookies(UserPerms,JSON.stringify(response.data.perms));
                    resolve(response);
                }).catch(error => {
                    reject(error)
                })
            })
        },
        Logout({commit}) {
            return new Promise((resolve, reject) => {
                removeCookies(TokenKey);
                removeCookies(UserNameKey);
                removeCookies(UserIsSuperKey);
                removeCookies(MenuKey);
                removeCookies(RouterKey);
                removeCookies(UserPerms);
                commit('SET_TOKEN', '');
                commit('SET_USERNAME', '');
                commit('SET_ISSUPER', '');
                commit('SET_MENU', []);
                commit('SET_ROUTER', []);
                commit('SET_USERPERMS', []);
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
                        commit('SET_TOKEN',response.data.token);
                        setCookies(TokenKey,response.data.token);
                        commit('SET_USERNAME',response.data.username);
                        setCookies(UserNameKey,response.data.username);
                        commit('SET_ISSUPER',response.data.is_superuser);
                        setCookies(UserIsSuperKey,response.data.is_superuser);
                        // 菜单及路由及权限
                        commit('SET_MENU',response.data.menu);
                        setCookies(MenuKey,JSON.stringify(response.data.menu));
                        // commit('SET_ROUTER',response.data.router);
                        setCookies(RouterKey,JSON.stringify(response.data.router));
                        commit('SET_USERPERMS',response.data.perms);
                        setCookies(UserPerms,JSON.stringify(response.data.perms));
                        resolve(response);
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