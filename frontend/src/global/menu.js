/*jshint esversion: 6 */
const Menus = [
    {
		id: 1,                          // 菜单id，逐步递增
        parentMenuId: 0,                // 父菜单id，无父菜单，填写
        name: 'Dashboard',              // 菜单唯一名字
        alias: 'Dashboard',             // 菜单显示名字
        url: '/dashboard',              // 菜单对应路由
        icon: 'icon-dashboard',         // 菜单图标(阿里svg图标名字)
        state: 'ENABLE',                // 菜单是否启用
        issuper: false,        
        childs: null  
    },
    {
        id: 2,
        parentMenuId: 0,
        name: 'usermanger',
        alias: '用户管理',
        url: '/home',
        icon: 'icon-houtaiyonghuguanli',
        state: 'ENABLE',
        issuper: true,
        childs: [
            {   
                id: 21, 
                parentMenuId : 2,
                name: 'user', 
                alias: '用户',
				url: '/user', 				
                state: 'ENABLE',
                issuper: true,
                icon: 'icon-yonghuguanli', 
                childs: null
            },
            {   
                id: 22, 
                parentMenuId : 2,
                name: 'usergroup', 
                alias: '用户组',
				url: '/usergroup', 				
                state: 'ENABLE',
                issuper: true,
                icon: 'icon-yonghuguanli', 
                childs: null
            },
            {   
                id: 23, 
                parentMenuId : 2,
                name: 'permissionsgroup', 
                alias: '权限组',
				url: '/permissionsgroup', 				
                state: 'ENABLE',
                issuper: true,
                icon: 'icon-yonghuguanli', 
                childs: null
            },
        ]
    },
    {
        id: 4,
        parentMenuId: 0,
        name: 'dbmanger',
        alias: 'MySQL管理',
        url: '/home',
        icon: 'icon-houtaiyonghuguanli',
        state: 'ENABLE',
        issuper: true,
        childs: [
            {   
                id: 41, 
                parentMenuId : 4,
                name: 'mysqlinst', 
                alias: 'MySQL实例',
				url: '/mysqlinst', 				
                state: 'ENABLE',
                issuper: true,
                icon: 'icon-yonghuguanli', 
                childs: null
            },
            {   
                id: 42, 
                parentMenuId : 4,
                name: 'mysqlmeta', 
                alias: 'MySQL元数据',
				url: '/mysqlmeta', 				
                state: 'ENABLE',
                issuper: true,
                icon: 'icon-yonghuguanli', 
                childs: null
            },
            {   
                id: 43, 
                parentMenuId : 4,
                name: 'mysqluser', 
                alias: 'MySQL用户',
				url: '/mysqluser', 				
                state: 'ENABLE',
                issuper: true,
                icon: 'icon-yonghuguanli', 
                childs: null
            },
            {   
                id: 44, 
                parentMenuId : 4,
                name: 'mysqlstatus', 
                alias: 'MySQL实例状态',
				url: '/mysqlstatus', 				
                state: 'ENABLE',
                issuper: true,
                icon: 'icon-yonghuguanli', 
                childs: null
            },
        ]
    },
    {
        id: 7,
        parentMenuId: 0,
        name: 'dbmanger',
        alias: 'MongoDB管理',
        url: '/home',
        icon: 'icon-houtaiyonghuguanli',
        state: 'ENABLE',
        issuper: true,
        childs: [
            {   
                id: 71, 
                parentMenuId : 7,
                name: 'mongodbinst', 
                alias: 'MongoDB实例',
				url: '/mongodbinst', 				
                state: 'ENABLE',
                issuper: true,
                icon: 'icon-yonghuguanli', 
                childs: null
            },
        ]
    },
    {
        id: 8,
        parentMenuId: 0,
        name: 'dbmanger',
        alias: 'Redis管理',
        url: '/home',
        icon: 'icon-houtaiyonghuguanli',
        state: 'ENABLE',
        issuper: true,
        childs: [
            {   
                id: 81, 
                parentMenuId : 8,
                name: 'redisinst', 
                alias: 'Redis实例',
				url: '/redisinst', 				
                state: 'ENABLE',
                issuper: true,
                icon: 'icon-yonghuguanli', 
                childs: null
            },
        ]
    },
    {
        id: 5,
        parentMenuId: 0,
        name: 'dbmanger',
        alias: '数据库权限',
        url: '/home',
        icon: 'icon-houtaiyonghuguanli',
        state: 'ENABLE',
        issuper: false,
        childs: [
            {   
                id: 51, 
                parentMenuId : 5,
                name: 'useraccessmysql', 
                alias: 'MySQL权限',
				url: '/useraccessmysql', 				
                state: 'ENABLE',
                issuper: false,
                icon: 'icon-yonghuguanli', 
                childs: null
            },
            {   
                id: 52, 
                parentMenuId : 5,
                name: 'useraccessmongodb', 
                alias: 'MongoDB权限',
				url: '/useraccessmongodb', 				
                state: 'ENABLE',
                issuper: false,
                icon: 'icon-yonghuguanli', 
                childs: null
            },
            {   
                id: 53, 
                parentMenuId : 5,
                name: 'useraccessredis', 
                alias: 'Redis权限',
				url: '/useraccessredis', 				
                state: 'ENABLE',
                issuper: false,
                icon: 'icon-yonghuguanli', 
                childs: null
            },
        ]
    },
    {
        id: 3,
        parentMenuId: 0,
        name: 'noticemanger',
        alias: '全局配置',
        url: '/home',
        icon: 'icon-houtaiyonghuguanli',
        state: 'ENABLE',
        issuper: true,
        childs: [
            {   
                id: 31, 
                parentMenuId : 3,
                name: 'mailconfig', 
                alias: '邮件配置',
				url: '/mailconfig', 				
                state: 'ENABLE',
                issuper: true,
                icon: 'icon-yonghuguanli', 
                childs: null
            },
            {   
                id: 32, 
                parentMenuId : 3,
                name: 'querylimit', 
                alias: 'QueryLimit',
				url: '/querylimit', 				
                state: 'ENABLE',
                issuper: true,
                icon: 'icon-yonghuguanli', 
                childs: null
            },
            {   
                id: 33, 
                parentMenuId : 3,
                name: 'dumpwhitelist', 
                alias: '导出白名单',
				url: '/dumpwhitelist', 				
                state: 'ENABLE',
                issuper: true,
                icon: 'icon-yonghuguanli', 
                childs: null
            },
        ]
    },
    {
        id: 6,
        parentMenuId: 0,
        name: 'dbmanger',
        alias: 'Query',
        url: '/home',
        icon: 'icon-chaxun',
        state: 'ENABLE',
        issuper: false,
        childs: [
            {   
                id: 61, 
                parentMenuId : 6,
                name: 'mysqlmeta', 
                alias: 'MySQL元数据',
				url: '/mysqlmeta', 				
                state: 'ENABLE',
                issuper: false,
                icon: 'icon-shujukushili', 
                childs: null
            },
            {   
                id: 62, 
                parentMenuId : 6,
                name: 'querysql', 
                alias: 'QuerySql',
				url: '/querysql', 				
                state: 'ENABLE',
                issuper: false,
                icon: 'icon-SQLshenhe', 
                childs: null
            },
            {   
                id: 63, 
                parentMenuId : 6,
                name: 'querymongodb', 
                alias: 'QueryMongodb',
				url: '/querymongodb', 				
                state: 'ENABLE',
                issuper: false,
                icon: 'icon-SQLshenhe', 
                childs: null
            },
            {   
                id: 64, 
                parentMenuId : 6,
                name: 'queryredis', 
                alias: 'QueryRedis',
				url: '/queryredis', 				
                state: 'ENABLE',
                issuper: false,
                icon: 'icon-SQLshenhe', 
                childs: null
            },
        ]
    },
    {
        id: 9,
        parentMenuId: 0,
        name: 'dbmanger',
        alias: '工单系统',
        url: '/home',
        icon: 'icon-chaxun',
        state: 'ENABLE',
        issuper: false,
        childs: [
            {   
                id: 93, 
                parentMenuId : 9,
                name: 'newworkorder', 
                alias: '新建工单',
				url: '/newworkorder', 				
                state: 'ENABLE',
                issuper: false,
                icon: 'icon-shujukushili', 
                childs: null
            },
            {   
                id: 91, 
                parentMenuId : 9,
                name: 'myworkorder', 
                alias: '我创建的',
				url: '/myworkorder', 				
                state: 'ENABLE',
                issuper: false,
                icon: 'icon-shujukushili', 
                childs: null
            },
            {   
                id: 92, 
                parentMenuId : 9,
                name: 'todoworkorder', 
                alias: '我的待办',
				url: '/todoworkorder', 				
                state: 'ENABLE',
                issuper: false,
                icon: 'icon-shujukushili', 
                childs: null
            },
        ]
    },
]



export { Menus };