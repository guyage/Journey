/*jshint esversion: 6 */
import axios from 'axios'
import qs from 'qs'
import router from '../router/router.js'
import { Message} from 'element-ui'
import { baseurl }  from '../global/config.js';
import store from '@/store/store.js'
import { getCookies } from '@/utils/auth.js'


// let loadinginstace; //load加载

// axios 全局参数
axios.defaults.baseURL = baseurl;
// 请求超时时间，默认5分钟
axios.defaults.timeout = 300000;


/**
 * axios请求拦截器
 * @param {object} config axios请求配置对象
 * @return {object} 请求成功或失败时返回的配置对象或者promise error对象
 * **/

axios.interceptors.request.use(
  config => {
    // Do something before request is sent
    // store.dispatch('SetLoading',true)
    if (store.getters.token) {
      // 让每个请求携带token-- ['Authorization']为自定义key 请根据实际情况自行修改
      config.headers['Authorization'] = 'JWT ' + getCookies('Authorization')
    }
    return config
  },
  error => {
    // Do something with request error
    console.log(error) // for debug
    Promise.reject(error)
  }
)

/**
 * axios 响应拦截器
 * @param {object} response 从服务端响应的数据对象或者error对象
 * @return {object} 响应成功或失败时返回的响应对象或者promise error对象
 **/

axios.interceptors.response.use(response => {
  // loadinginstace.close();  // 响应成功关闭loading
  // store.dispatch('SetLoading',false);
  return response
}, error => {
  if (error.response) {
    // store.dispatch('SetLoading',false)
    return Promise.resolve(error.response)
  }
  else if (error.request) {
    // store.dispatch('SetLoading',false)
    // console.log(error.request);
    return Promise.resolve(error.request);
    // return Promise.resolve(error.request)
  }
  
});

/**
 * 请求发出后检查返回的状态码,统一捕获正确和错误的状态码，正确就直接返回response,错误就自定义一个返回对象
 * @param {object} response 响应对象
 * @return {object} 响应正常就返回响应数据否则返回错误信息
 **/
function checkStatus (response) {
  // loading
  // 如果http状态码正常，则直接返回数据
  if (response && (response.status === 200 || response.status === 304 || response.status === 400)) {
    return response
    // 如果不需要除了data之外的数据，可以直接 return response.data
  } else {
  // 异常状态下，把错误信息返回去
    return statusCode(response)
  }
  // return {
  //   status: -404,
  //   msg: '网络异常'
  // }
}
// function checkStatus(response) {
//   // 如果http状态码正常，则直接返回数据
//   if  (response &&(response.status === 201 || response.status === 200 || response.status === 304)){
//     if (response.data.resultCode == '-1') {
//       Message.error({
//         message: '请求出错',
//         onClose: function () {
//           router.push({name: 'error-404'});
//         }
//       })
//     } else {
//       return response
//     }
//   }else {
//     // 异常状态下，把错误信息返回去
//     return {
//       status: -404,
//       msg: '网络异常'
//     }
//     // return statusCode(response)
//     // return {
//     //   data:{
//     //     status: 404,
//     //     resultCode:'-1',
//     //     resultMsg:'网络异常',
//     //   }
//     // }
//   }

// }

/**
 * 状态码
 */
function statusCode(response) {
  switch (response.status) {
    case 400:
      // console.log(response.data);
      if (response.data.non_field_errors) {
        console.log(response.data.non_field_errors);
        var msg = '登陆失败，请输入正确用户名及密码，如有疑问，请联系管理员!'
        var msg = response.data.non_field_errors + '登录失败，如有疑问，请联系管理员!'
        // var msg = response.data.non_field_errors
      }
      else {
        console.log(response.data);
        var msg = '请求异常，请联系管理员!错误信息：' + JSON.stringify(response.data)
      }
      Message.error({
        duration: 6000,
        message: msg,
        // onClose: function () {
        //   router.push({name: 'login'});
        // }
      })
      break;
    case 401:
      // console.log(response.data);
      Message.error({
        message: '未授权，请登录',
        onClose: function () {
          router.push({name: 'error-404'});
        }
      })
      break;
    case 403:
      Message.error({
        message: '未授权或认证失败，请重新登陆! 如有疑问，请联系管理员!',
        // duration: 6000,
        // onClose: function () {
        //   router.push({name: 'login'});
        // }
      })
      break;
    case 404:
      Message.error({
        message: '请求地址出错',
        // onClose: function () {
        //   router.push({name: 'error-404'});
        // }
      })
      break;
    case 408:
      Message.error({
        message: '请求超时',
        onClose: function () {
          router.push({name: 'error-404'});
        }
      })
      break;
    case 500:
      Message.error({
        message: '服务器内部错误',
        // onClose: function () {
        //   router.push({name: 'error-500'});
        // }
      })
      break;
    default:
      return response
  }
}



/**
 * 检查完状态码后需要检查后如果成功了就需要检查后端的状态码处理网络正常时后台语言返回的响应
 * @param {object} res 是后台返回的对象或者自定义的网络异常对象，不是http 响应对象
 * @return {object} 返回后台传过来的数据对象，包含code,message,data等属性，
 */
// function checkCode(res) {
//   // 如果code异常(这里已经包括网络错误，服务器错误，后端抛出的错误)，可以弹出一个错误提示，告诉用户
//     return statusCode(res)
// }
function checkCode(res) {
  // 如果code异常(这里已经包括网络错误，服务器错误，后端抛出的错误)，可以弹出一个错误提示，告诉用户
  if (res ) {
    return statusCode(res)
  }
  return res
}

// 请求方式的配置
export default {
  oPost(url, data) {  //  post
    return axios({
      method: 'post',
      url,
      data: data,
      // timeout: 50000,
      // headers: {
      //   'X-Requested-With': 'XMLHttpRequest',
      //   'Content-Type': 'application/json; charset=UTF-8'
      // }
    }).then(
      (response) => {
        return checkStatus(response)
      }
    ).then(
      (res) => {
        return checkCode(res)
      }
    )
  },
  oUpdate(url,data) {
    return axios({
      method: 'patch',
      url,
      data, data,
      // timeout: 5000, 
    }).then(
      (response) => {
        return checkStatus(response)
      }
    ).then(
      (res) => {
        return checkCode(res)
      }
    )
  },
  oDelete(url,params) {
    return axios({
      method: 'delete',
      url,
      params, params,
      // timeout: 5000, 
    }).then(
      (response) => {
        return checkStatus(response)
      }
    ).then(
      (res) => {
        return checkCode(res)
      }
    )
  },
  oGet(url,params) {  // get
    return axios({
      method: 'get',
      url,
      params, // get 请求时带的参数
      // timeout: 5000,
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    }).then(
      (response) => {
        return checkStatus(response)
      }
    ).then(
      (res) => {
        return checkCode(res)
      }
    )
  },
};
