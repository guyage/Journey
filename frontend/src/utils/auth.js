/*jshint esversion: 6 */

const obj_key = ['userperms','menu','router']

export function getCookies(Key) {
    if (localStorage.getItem(Key) == 'false') {
        return false;
    }
    else if (localStorage.getItem(Key) == 'true') {
        return true;
    }
    else if (obj_key.indexOf(Key) > -1) {
        return JSON.parse(localStorage.getItem(Key));
    }
    else {
        return localStorage.getItem(Key);
    }
    
}
  
export function setCookies(Key,value) {
    return localStorage.setItem(Key,value);
}
  
export function removeCookies(Key) {
    return localStorage.removeItem(Key);
}