// 后台接口地址
// const baseurl = "http://sqlplatform.api.dev:8888/api"
// const baseurl = "http://sqlplatform.xs.jf/api"

const baseurl = process.env.baseUrl

const Menus = [
	{
		id: 1,                     // 菜单id，逐步递增
        parentMenuId: 0,           // 父菜单id，无父菜单，填写
        name: 'Dashboard',      // 菜单唯一名字
        alias: 'Dashboard',     // 菜单显示名字
        url: '/dashboard',                  // 菜单对应路由
        icon: 'icon-dashboard',     // 菜单图标(阿里svg图标名字)
        state: 'ENABLE',           // 菜单是否启用
        roles: 'dev',        
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
        roles: 'admin',
        childs: [
            {   
                id: 21, 
                parentMenuId : 2,
                name: 'user', 
                alias: '用户',
				url: '/user', 				
                state: 'ENABLE',
                roles: 'admin',
                icon: 'icon-yonghuguanli', 
                childs: null
            },
        ]
    },
	{
        id: 3,
        parentMenuId : 0,
        name: 'database',
        alias: 'MySQL管理',
        url: '/home',
        icon: 'icon-database',
        state: 'ENABLE',
        roles: 'dev',
        childs: [
			{   
                id: 31, 
                parentMenuId : 3,
                name: 'mysqlinst', 
                alias: 'MySQL实例', 
                url: '/mysqlinst', 
                icon: 'icon-suyaniconchanpinleibufenzuodaohangbufen84', 
                state: 'ENABLE',
                roles: 'admin',
                childs: null
            },
            {   
                id: 32, 
                parentMenuId : 3,
                name: 'mysqldb', 
                alias: 'MySQL数据库', 
                url: '/mysqldb', 
                icon: 'icon-erji-yonghuguanli', 
                state: 'ENABLE',
                roles: 'admin',
                childs: null
            },
            {   
                id: 33, 
                parentMenuId : 3,
                name: 'mysqluser', 
                alias: 'MySQL用户', 
                url: '/mysqluser', 
                icon: 'icon-erji-yonghuguanli', 
                state: 'ENABLE',
                roles: 'admin',
                childs: null
            },
            {   
                id: 34, 
                parentMenuId : 3,
                name: 'dbmeta', 
                alias: 'MySQL元数据', 
                url: '/dbmeta', 
                icon: 'icon-shujukushili', 
                state: 'ENABLE',
                roles: 'dev',
                childs: null
            }
        ]
    },
	{
        id: 4,
        parentMenuId : 0,
        name: 'home',
        alias: 'Mongodb管理',
        url: '/home',
        icon: 'icon-database',
        state: 'ENABLE',
        roles: 'admin',
        childs: [
            {   
                id: 41, 
                parentMenuId : 4,
                name: 'mongodbinst', 
                alias: 'Mongodb实例', 
                url: '/mongodbinst', 
                icon: 'icon-suyaniconchanpinleibufenzuodaohangbufen84', 
                state: 'ENABLE',
                roles: 'admin',
                childs: null
            },
            {   
                id: 42, 
                parentMenuId : 4,
                name: 'mongodbdb', 
                alias: 'Mongodb数据库', 
                url: '/mongodbdb', 
                icon: 'icon-suyaniconchanpinleibufenzuodaohangbufen84', 
                state: 'ENABLE',
                roles: 'admin',
                childs: null
            },
        ]
    },
	{
        id: 6,
        parentMenuId : 0,
        name: 'home',
        alias: 'Redis管理',
        url: '/home',
        icon: 'icon-database',
        state: 'ENABLE',
        roles: 'admin',
        childs: [
            {   
                id: 61, 
                parentMenuId : 6,
                name: 'redisdb', 
                alias: 'Redis实例', 
                url: '/redisdb', 
                icon: 'icon-suyaniconchanpinleibufenzuodaohangbufen84', 
                state: 'ENABLE',
                roles: 'admin',
                childs: null
            },
        ]
    },
	{
        id: 7,
        parentMenuId: 0,
        name: 'Query',
        alias: 'Query',
        url: '/home',
        icon: 'icon-SQLshujuji',
        state: 'ENABLE',
		roles: 'dev',
        childs: [
            {   
                id: 71, 
                parentMenuId : 7,
                name: 'QuerySQL', 
                alias: 'Query', 
                url: '/query', 
                icon: 'icon-chaxun',
				state: 'ENABLE',
				roles: 'dev',
                childs: null
            },
            {   
                id: 72, 
                parentMenuId : 7,
                name: 'QuerySQL2', 
                alias: 'QuerySQL2',
				url: '/query2',
                icon: 'icon-chaxun',
				state: 'ENABLE',
				roles: 'dev',
                childs: null
            },
            {   
                id: 73, 
                parentMenuId : 7,
                name: 'QueryMongodb',
                alias: 'QueryMongodb',
                url: '/querymongodb', 
                icon: 'icon-chaxun',
				state: 'ENABLE',
				roles: 'dev',
                childs: null
            },
            {   
                id: 74, 
                parentMenuId : 7,
                name: 'QueryRedis', 
                alias: 'QueryRedis',
                url: '/queryredis',
                icon: 'icon-chaxun',
				state: 'ENABLE',
				roles: 'dev',
                childs: null
            },
            {   
                id: 75, 
                parentMenuId : 7,
                name: 'SQLSoar', 
                alias: 'SQLSoar',
                url: '/sqlsoar', 
                icon: 'icon-SQLshenhe',
				state: 'ENABLE',
				roles: 'dev',
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

const mongodbinst_columns = {
    id: 'id',
    instname: '实例名称',
    host: 'IP地址',
    port: '端口',
    version: '版本',
    comment: '备注'
}




export { baseurl, mongodbinst_columns,db_columns, user_columns,Menus};