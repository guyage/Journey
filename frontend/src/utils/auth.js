import Cookies from 'js-cookie'

// const TokenKey = 'Authorization'

export function getCookies(TokenKey) {
    // return Cookies.get(TokenKey)
    return sessionStorage.getItem(TokenKey);
}
  
export function setCookies(TokenKey,token) {
    // var real_token = 'JWT ' + token
    // return Cookies.set(TokenKey, token,{expires:2})
    return sessionStorage.setItem(TokenKey,token);
}
  
export function removeCookies(TokenKey) {
    // return Cookies.remove(TokenKey)
    return sessionStorage.removeItem(TokenKey);
}