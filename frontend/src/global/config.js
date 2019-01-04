// 后台接口地址
// const baseurl = "http://sqlplatform.api.dev:8888/api"
// const baseurl = "http://sqlplatform.xs.jf/api"

const baseurl = process.env.baseUrl

// admin菜单
const AdminMenus = [
    {
        id: 1,                     // 菜单id，逐步递增
        parentMenuId: 0,           // 父菜单id，无父菜单，填写
        name: 'SQL_Platform',      // 菜单唯一名字
        alias: 'SQL_Platform',     // 菜单显示名字
        url: '/dashboard',                  // 菜单对应路由
        icon: 'icon-dashboard',     // 菜单图标(阿里svg图标名字)
        state: 'ENABLE',           // 菜单是否启用
        roles: 'admin',        
        childs: null               // 菜单是否有子菜单，有则列出，无则为null
    },
    {
        id: 3,
        parentMenuId : 0,
        name: 'user',
        alias: '用户',
        state: 'ENABLE',
        url: '/home',
        icon: 'icon-houtaiyonghuguanli',
        childs: [
            {   
                id: 3, 
                parentMenuId : 2,
                name: 'usermanger', 
                alias: '用户管理', 
                state: 'ENABLE',
                url: '/user', 
                icon: 'icon-yonghuguanli', 
                childs: null
            },
        ]
    },
    {
        id: 2,
        parentMenuId : 0,
        name: 'database',
        alias: '数据库',
        url: '/home',
        icon: 'icon-database',
        state: 'ENABLE',
        roles: 'admin',
        childs: [
            {   
                id: 3, 
                parentMenuId : 2,
                name: 'dbmanger', 
                alias: '数据库管理', 
                url: '/db', 
                icon: 'icon-suyaniconchanpinleibufenzuodaohangbufen84', 
                state: 'ENABLE',
                roles: 'admin',
                childs: null
            },
            {   
                id: 4, 
                parentMenuId : 2,
                name: 'dbuser', 
                alias: '数据库用户管理', 
                url: '/dbuser', 
                icon: 'icon-erji-yonghuguanli', 
                state: 'ENABLE',
                roles: 'dev',
                childs: null
            },
            {   
                id: 5, 
                parentMenuId : 2,
                name: 'dbmeta', 
                alias: '数据库元数据', 
                url: '/dbmeta', 
                icon: 'icon-shujukushili', 
                state: 'ENABLE',
                roles: 'admin',
                childs: null
            }
        ]
    },
    {
        id: 4,                     // 菜单id，逐步递增
        parentMenuId: 0,           // 父菜单id，无父菜单，填写
        name: 'SQL',      // 菜单唯一名字
        alias: 'SQL',     // 菜单显示名字
        url: '/sql',                  // 菜单对应路由
        icon: 'icon-SQLshujuji',     // 菜单图标(阿里svg图标名字)
        state: 'ENABLE',           // 菜单是否启用
        childs: [
            {   
                id: 5, 
                parentMenuId : 4,
                name: 'Query', 
                alias: 'Query', 
                state: 'ENABLE',
                url: '/query', 
                icon: 'icon-chaxun', 
                childs: null
            },
            {   
                id: 6, 
                parentMenuId : 4,
                name: 'Query2', 
                alias: 'Query2', 
                state: 'ENABLE',
                url: '/query2', 
                icon: 'icon-chaxun', 
                childs: null
            },
            {   
                id: 7, 
                parentMenuId : 4,
                name: 'SQLSoar', 
                alias: 'SQLSoar', 
                state: 'ENABLE',
                url: '/sqlsoar', 
                icon: 'icon-SQLshenhe', 
                childs: null
            },
        ]              
    },
]


// dev菜单
const NoramalMenus = [
    {
        id: 1,                     // 菜单id，逐步递增
        parentMenuId: 0,           // 父菜单id，无父菜单，填写
        name: 'SQL_Platform',      // 菜单唯一名字
        alias: 'SQL_Platform',     // 菜单显示名字
        url: '/dashboard',                  // 菜单对应路由
        icon: 'icon-appstore',     // 菜单图标(阿里svg图标名字)
        state: 'ENABLE',           // 菜单是否启用
        roles: 'admin',        
        childs: null               // 菜单是否有子菜单，有则列出，无则为null
    },
    {
        id: 4,                     // 菜单id，逐步递增
        parentMenuId: 0,           // 父菜单id，无父菜单，填写
        name: 'SQL',      // 菜单唯一名字
        alias: 'SQL',     // 菜单显示名字
        url: '/sql',                  // 菜单对应路由
        icon: 'icon-appstore',     // 菜单图标(阿里svg图标名字)
        state: 'ENABLE',           // 菜单是否启用
        childs: [
            {   
                id: 7, 
                parentMenuId : 4,
                name: 'dbmeta', 
                alias: '数据库元数据', 
                url: '/dbmeta', 
                icon: 'icon-database', 
                state: 'ENABLE',
                roles: 'admin',
                childs: null
            },
            {   
                id: 5, 
                parentMenuId : 4,
                name: 'Query', 
                alias: 'Query', 
                state: 'ENABLE',
                url: '/query', 
                icon: 'icon-database', 
                childs: null
            },
            {   
                id: 6, 
                parentMenuId : 4,
                name: 'Query2', 
                alias: 'Query2', 
                state: 'ENABLE',
                url: '/query2', 
                icon: 'icon-database', 
                childs: null
            },
            {   
                id: 7, 
                parentMenuId : 4,
                name: 'SQLSoar', 
                alias: 'SQLSoar', 
                state: 'ENABLE',
                url: '/sqlsoar', 
                icon: 'icon-database', 
                childs: null
            },
        ]              
    },
]



// 数据库表格对应列名
const db_columns = {
    id: 'id',
    dbname: '数据库',
    host: 'IP地址',
    port: '端口',
    version: '版本',
    comment: '备注'
}

const user_columns = {
    id: 'id',
    username: '用户名',
    last_name: '姓',
    first_name: '名',
    is_active: '状态',
    group: '用户组',
    email: '邮箱',
    accessdb: 'AccessDB',
    mobile: '手机',
    webcat: '微信',
    comment: '备注'
}




export { baseurl, AdminMenus, db_columns, user_columns,NoramalMenus};