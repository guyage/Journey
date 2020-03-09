/*jshint esversion: 6 */
import request from '../utils/request.js';

//Login
export const Login = params => { return request.post('/login',params) };
//ldap认证登陆
export const LdapAuth = params => { return request.post('/ldapauth',params) };
//Logout
export const Logout = () => { return request.get('/logout') };










