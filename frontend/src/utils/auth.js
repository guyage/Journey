/*jshint esversion: 6 */

export function getCookies(Key) {
    if (sessionStorage.getItem(Key) == 'false') {
        return false;
    }
    else if (sessionStorage.getItem(Key) == 'true') {
        return true;
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