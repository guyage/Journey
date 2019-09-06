/*jshint esversion: 6 */
const getters = {
    token: state => state.user.token,
    username: state => state.user.username,
    userperms: state => state.user.userperms,
    userissuper: state => state.user.userissuper,
    menu: state => state.user.menu,
    router: state => state.user.router,
    visitedViews: state => state.tagsview.visitedViews,
    cachedViews: state => state.tagsview.cachedViews,
}


export default getters;