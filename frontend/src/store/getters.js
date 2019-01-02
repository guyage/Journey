const getters = {
    token: state => state.user.token,
    username: state => state.user.username,
    usergroup: state => state.user.usergroup,
    menus: state => state.user.menus,
    routers: state => state.user.routers,
    visitedViews: state => state.tagsview.visitedViews,
    cachedViews: state => state.tagsview.cachedViews,
}


export default getters;