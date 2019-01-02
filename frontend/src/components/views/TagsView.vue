<template>
    <div class="tagsview">
        <el-scrollbar>
            <!-- <span @click="open" class="nav-tab-span">aaa</span> -->
            <!-- <el-tag size="small" closable></el-tag> -->
            <router-link 
            v-for="item in visitedViews"
            :key="item.path"
            ref="tag"
            :to="{ path: item.path, query: item.query, fullPath: item.fullPath }">
            <el-tag :class="isActive(item)?'active':''" size="small" closable @close.prevent.stop="closeSelectedTag(item)">
                <!-- <i @click="refreshSelectedTag(item)" class="el-icon-refresh"></i> -->
                {{item.tag}}
            </el-tag>
            <!-- {{item.tag}}
            <span class="el-icon-close" @click.prevent.stop="closeSelectedTag(item)" /> -->
            </router-link>
        </el-scrollbar>
        <div class="tagsview-button">
            <el-dropdown size="mini" type="primary">
                <el-button type="info" plain size="mini">
                    标签选项<i class="el-icon-arrow-down el-icon--right"></i>
                </el-button>
                <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item @click.native="closeAllTags">关闭所有</el-dropdown-item>
                    <el-dropdown-item @click.native="closeOthersTags">关闭其他</el-dropdown-item>
                </el-dropdown-menu>
            </el-dropdown>
        </div>
    </div>
</template>

<script>
import store from '@/store/store.js';
export default {
    data () {
        return {
           selectedTag: {} 
        }
    },
    computed: {
        visitedViews() {
            return this.$store.state.tagsview.visitedViews
        }
    },
    watch: {
        $route(to) {
            this.addViewTags()
            this.selectedTag = Object.assign({},to,{tag: to.meta.tag || 'no-title'})
        },
    },
    methods: {
        isActive(route) {
            return route.path === this.$route.path
        },
        addViewTags() {
            const { name } = this.$route
            if (name) {
                this.$store.dispatch('addView',this.$route)
            }
        },
        closeSelectedTag(view) {
            this.$store.dispatch('delView', view).then(({visitedViews}) => {
                if (this.isActive(view)) {
                    const latestView = visitedViews.slice(-1)[0]
                    if (latestView) {
                        this.$router.push(latestView)
                    }
                    else {
                        this.$router.push({ path: '/dashboard'})
                    }
                }
            })
        },
        // refreshSelectedTag(view) {
        //     this.$store.dispatch('delCachedView', view).then(() => {
        //         const { fullPath } = view
        //         console.log('fullPath',fullPath);
        //         this.$nextTick(() => {
        //             this.$router.replace({
        //                 path: fullPath
        //             })
        //         })
        //     })
        // },
        closeAllTags() {
            this.$store.dispatch('delAllViews')
            this.$router.push({ path: '/dashboard'})
        },
        closeOthersTags() {
            this.$router.push(this.selectedTag)
            this.$store.dispatch('delOthersViews', this.selectedTag).then(() => {
            })
        },
    }
}
</script>

<style>
.tagsview-button{
    float: right;
    margin-top: -50px;
}
.tagsview .el-scrollbar{
    height: 30px;
    margin-top: 5px;
}
.tagsview .el-tag--small{
    float: left;
    margin: 0 2px;
    color: #495060;
    background-color: #fff;
    border: 1px solid #d8dce5;
}
.tagsview .el-tag.el-tag--small.active{
    color: #fff;
    background-color: #42b983;
    border-color: #42b983;
}
.tagsview .el-tag .el-icon-close{
    color: #495060;
}
.tagsview .el-tag.el-tag--small.active .el-icon-close{
    color: #fff;
}
.tagsview .el-tag.el-tag--small.active::before{
    content: "";
    background: #fff;
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    position: relative;
    margin-right: 2px;
}
.el-dropdown-menu--mini{
    top: 70px !important;
}
.el-button--info:focus, .el-button--info:hover{
    background: #48D1CC;
    border-color:#48D1CC
}
</style>
