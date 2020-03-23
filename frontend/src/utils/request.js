/*jshint esversion: 6 */
//引入axios
import axios from 'axios';
import router from '../router/router.js';
import { Message} from 'element-ui'
import store from '@/store/store.js';
import { getCookies } from '@/utils/auth.js';
import { log } from 'util';

let cancel ,promiseArr = {}
const CancelToken = axios.CancelToken;

const baseurl = process.env.baseUrl

// axios 全局参数
axios.defaults.baseURL = baseurl;

//设置默认请求头
// axios.defaults.headers = {
//     'X-Requested-With': 'XMLHttpRequest'
// }
// 请求超时时间，默认5分钟
axios.defaults.timeout = 300000;

//请求拦截器
axios.interceptors.request.use(config => {
    if (store.getters.token) {
      // 让每个请求携带token-- ['Authorization']为自定义key 请根据实际情况自行修改
      config.headers['Authorization'] = 'JWT ' + getCookies('Authorization')
      //发起请求时，取消掉当前正在进行的相同请求
      // if (promiseArr[config.url]) {
      //   promiseArr[config.url]('操作取消')
      //   promiseArr[config.url] = cancel
      // } 
      // else {
      //     promiseArr[config.url] = cancel
      // }
    }
    return config
}, error => {
    return Promise.reject(error)
})

//响应拦截器即异常处理
axios.interceptors.response.use(response => {
    return response
}, err => {
    if (err && err.response) {
      switch (err.response.status) {
        case 400:
          if (err.response.data.non_field_errors) {
            err.message = '登陆失败，请输入正确用户名及密码，如有疑问，请联系管理员!'
          }
          else {
            err.message = '请求异常，请联系管理员!错误信息：' + JSON.stringify(err.response.data)
          }
          break;
        case 401:
          err.message = '未授权，请重新登录'
          router.push({
            path: "/login",
            // query:{
            //  参数
            //   clearProject:true
            // }
          });
          break;
        case 403:
          err.message = '拒绝访问'
          break;
        case 404:
          err.message = '请求错误,未找到该资源'
          break;
        case 405:
          err.message = '请求方法未允许'
          break;
        case 408:
          err.message = '请求超时'
          break;
        case 500:
          err.message = '服务器端出错'
          break;
        case 501:
          err.message = '网络未实现'
          break;
        case 502:
          err.message = '网络错误'
          break;
        case 503:
          err.message = '服务不可用'
          break;
        case 504:
          err.message = '网络超时'
          break;
        case 505:
          err.message = 'http版本不支持该请求'
          break;
        default:
          err.message = `连接错误${err.response.status}`
      }
    } else {
      err.message = err.toString()
    }
    Message.error({message: err.message})
    return Promise.reject(err);
})

export default {
  //get请求
  get (url,param) {
      return new Promise((resolve,reject) => {
          axios({
          method: 'get',
          url,
          params: param,
          // cancelToken: new CancelToken(c => {
          //     cancel = c
          // })
          }).then(res => {
            resolve(res)
          }).catch((err) => {
            reject(err)
          })
      })
  },
  //post请求
  post (url,param) {
      return new Promise((resolve,reject) => {
          axios({
          method: 'post',
          url,
          data: param,
          // cancelToken: new CancelToken(c => {
          //     cancel = c
          // })
          }).then(res => {
            resolve(res)
          }).catch((err) => {
            reject(err)
          })
      })
  },
  //patch请求
  patch (url,param) {
    return new Promise((resolve,reject) => {
        axios({
        method: 'patch',
        url,
        data: param,
        // cancelToken: new CancelToken(c => {
        //     cancel = c
        // })
        }).then(res => {
          resolve(res)
        }).catch((err) => {
          reject(err)
        })
    })
  },
  //delete请求
  delete (url,param) {
    return new Promise((resolve,reject) => {
        axios({
        method: 'delete',
        url,
        params: param,
        // cancelToken: new CancelToken(c => {
        //     cancel = c
        // })
        }).then(res => {
          resolve(res);
        }).catch((err) => {
          reject(err);
        })
    })
  },
};