/*jshint esversion: 6 */
const getters = {
    token: state => state.user.token,
    username: state => state.user.username,
    usergroup: state => state.user.usergroup,
    userissuper: state => state.user.userissuper,
    userpermissionsgroup: state => state.user.userpermissionsgroup,
    menus: state => state.user.menus,
    routers: state => state.user.routers,
    visitedViews: state => state.tagsview.visitedViews,
    cachedViews: state => state.tagsview.cachedViews,
}


export default getters;