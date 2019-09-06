/*jshint esversion: 6 */

const obj_key = ['userperms','menu','router']

export function getCookies(Key) {
    if (sessionStorage.getItem(Key) == 'false') {
        return false;
    }
    else if (sessionStorage.getItem(Key) == 'true') {
        return true;
    }
    else if (obj_key.indexOf(Key) > -1) {
        return JSON.parse(sessionStorage.getItem(Key));
    }
    else {
        return sessionStorage.getItem(Key);
    }
    
}
  
export function setCookies(Key,value) {
    return sessionStorage.setItem(Key,value);
}
  
export function removeCookies(Key) {
    return sessionStorage.removeItem(Key);
}