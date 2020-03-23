/*jshint esversion: 6 */

const UserRouter = [
    { 
        path: '/menu', 
        component: resolve => require(['@/components/user/menus/Menus.vue'],resolve), 
        name: 'menu',
        meta: { tag: '菜单路由', title: ['用户权限','菜单路由']},
    },
    { 
        path: '/perms', 
        component: resolve => require(['@/components/user/perms/Perms.vue'],resolve), 
        name: 'perms',
        meta: { tag: '接口权限', title: ['用户权限','接口权限']},
    },
    { 
        path: '/role', 
        component: resolve => require(['@/components/user/role/Role.vue'],resolve), 
        name: 'role',
        meta: { tag: '角色', title: ['用户权限','角色']},
    },
    { 
        path: '/user', 
        component: resolve => require(['@/components/user/user/User.vue'],resolve), 
        name: 'user',
        meta: { tag: '用户', title: ['用户权限','用户']},
    },
    { 
        path: '/usergroup', 
        component: resolve => require(['@/components/user/usergroup/UserGroup.vue'],resolve), 
        name: 'usergroup',
        meta: { tag: '用户组', title: ['用户权限','用户组']},
    },
]

export default UserRouter;