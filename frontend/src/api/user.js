/*jshint esversion: 6 */
import request from '../utils/request.js';

////---------------------user文件夹组件api
export const getMenus = params => {
    if (params) {
        return request.get('/menu/'+params.id+'/');
    }
    else {
        return request.get('/menu/');
    }
};
export const searchMenus = params => { return request.get('/menu/'+'?search='+params.searchcontent) };
export const addMenus = params => { return request.post('/menu/',params)};
export const editMenus = params => { return request.patch('/menu/'+params.id+'/',params)};
////---------------------user文件夹组件api
// perms
export const getPerms = params => {
    if (params) {
        return request.get('/perms/'+params.id+'/');
    }
    else {
        return request.get('/perms/');
    }
};
export const searchPerms = params => { return request.get('/perms/'+'?search='+params.searchcontent) };
export const addPerms = params => { return request.post('/perms/',params)};
export const editPerms = params => { return request.patch('/perms/'+params.id+'/',params)};
export const delPerms = params => { return request.delete('/perms/'+params.id+'/') };
// role
export const getRole = params => {
    if (params) {
        return request.get('/role/'+params.id+'/');
    }
    else {
        return request.get('/role/');
    }
};
export const addRole = params => { return request.post('/role/',params)};
export const editRole = params => { return request.patch('/role/'+params.id+'/',params)};
// user
//用户
export const getUser = params => {
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

// 用户组
export const getUserGroup = params => {
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