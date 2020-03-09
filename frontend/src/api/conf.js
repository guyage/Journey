/*jshint esversion: 6 */
import request from '../utils/request.js';

////---------------------conf文件下api
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

// 系统日志
export const getCrudEvent = params => { return request.post('/crudevent/',params) };
