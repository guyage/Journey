/*jshint esversion: 6 */
import request from '../utils/request.js';

//Login
export const Login = params => { return request.post('/login',params) };
//ldap认证登陆
export const LdapAuth = params => { return request.post('/ldapauth',params) };
//Logout
export const Logout = () => { return request.get('/logout') };

////全局配置
// 邮件配置
export const getMailConfig = () => { return request.get('/mailconfig/')};
export const setMailConfig = params => {
    if ('id' in params) {
        return request.patch('/mailconfig/'+params.id+'/',params); 
    }
    else {
        return request.post('/mailconfig/',params);
    }
};
//测试邮件功能
export const execMailTest = params => { return request.post('/mailtest/',params) };
// QueryLimit配置
export const getQueryLimit = () => { return request.get('/querylimit/')};
export const setQueryLimit = params => {
    if (params.id >0) {
        return request.patch('/querylimit/'+params.id+'/',params); 
    }
    else {
        return request.post('/querylimit/',params);
    }
};
// 导出白名单
export const getDumpWhiteList = () => { return request.get('/dumpwhitelist/')};
export const delDumpWhiteList = params => { return request.delete('/dumpwhitelist/'+params.id+'/')};
export const addDumpWhiteList = params => { return request.post('/dumpwhitelist/',params)};
export const editDumpWhiteList = params => { return request.patch('/dumpwhitelist/'+params.id+'/',params)};
export const searchDumpWhiteList = params => { return request.get('/dumpwhitelist/'+'?search='+params.searchcontent) };

////用户管理
//用户组
export const getUserGroupList = params => {
    if (params) {
        return request.get('/usergroup/'+params.id+'/');
    }
    else {
        return request.get('/usergroup/');
    }
};
export const searchUserGroup = params => { return request.get('/usergroup/'+'?search='+params.searchcontent) };
export const addUserGroup = params => { return request.post('/usergroup/',params) };
export const delUserGroup = params => { return request.delete('/usergroup/'+params.id+'/') };
export const editUserGroup = params => { return request.patch('/usergroup/'+params.id+'/',params) };

//用户
export const getUserList = params => {
    if (params) {
        return request.get('/user/'+params.id+'/');
    }
    else {
        return request.get('/user/');
    }
};
export const searchUser = params => { return request.get('/user/'+'?search='+params.searchcontent) };
export const addUser = params => { return request.post('/user/',params) };
export const delUser = params => { return request.delete('/user/'+params.id+'/') };
export const editUser = params => { return request.patch('/user/'+params.id+'/',params) };

////db
//mysqlinst
export const getMysqlInst = params => {
    if (params) {
        return request.get('/mysqlinst/'+params.id+'/');
    }
    else {
        return request.get('/mysqlinst/');
    }
};
export const searchMysqlInst = params => { return request.get('/mysqlinst/'+'?search='+params.searchcontent) };
export const addMysqlInst = params => { return request.post('/mysqlinst/',params) };
export const delMysqlInst = params => { return request.delete('/mysqlinst/'+params.id+'/') };
export const editMysqlInst = params => { return request.patch('/mysqlinst/'+params.id+'/',params) };

////useraccessmysql
export const getUserAccessMysql = params =>  { return request.get('/useraccessmysql/',params); }
export const addUserAccessMysql = params => { return request.post('/useraccessmysql/',params) };
export const editUserAccessMysql = params => { return request.patch('/useraccessmysql/'+params.id+'/',params) };
export const delUserAccessMysql = params => { return request.delete('/useraccessmysql/'+params.id+'/') };
export const searchUserAccessMysql = params => { return request.get('/useraccessmysql/'+'?search='+params.searchcontent) };
////mysqlmanager
export const getMysqlMeta = params => { return request.post('/mysqlmeta/',params); }

////get user access db
export const getUserAccessDb = params =>  { return request.post('/useraccessdb/',params); }

////mysqluser
export const execMysqlUser = params =>  { return request.post('/mysqluser/',params); }
////mysqlstatus
export const getMysqlStatus = params =>  { return request.post('/mysqlstatus/',params); }

////query
//querysql
export const execQuerySql = params =>  { return request.post('/querysql/',params); }
