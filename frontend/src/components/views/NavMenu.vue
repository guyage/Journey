<template>
    <div id="navmenu">
        <label v-for="parentMenu in NavMenus" :key="parentMenu.id">
            <el-menu-item v-if="parentMenu.childs == null&&parentMenu.state==='ENABLE'" :index="parentMenu.alias" :route="parentMenu.url">
                <template slot="title">
                    <!-- <svg class="icon" aria-hidden="true">
                        <use xlink:href="#icon-database"></use>
                    </svg> -->
                    <icon-svg :iconClass="parentMenu.icon"></icon-svg>
                    <span>{{ parentMenu.alias }}</span>
                </template>
            </el-menu-item>
            <el-submenu v-if="parentMenu.childs != null&&parentMenu.state==='ENABLE'" :index="parentMenu.alias" :route="parentMenu.url">
                <template slot="title">
                    <icon-svg :iconClass="parentMenu.icon"></icon-svg>
                    <span>{{ parentMenu.alias }}</span>
                </template>
                    <el-menu-item v-for="childMenu in parentMenu.childs" v-if="childMenu.state==='ENABLE'" :key="childMenu.id" :index="childMenu.alias" :route="childMenu.url">
                        <template slot="title">
                            <icon-svg :iconClass="childMenu.icon"></icon-svg>
                        <span >{{ childMenu.alias }}</span>
                        </template>
                    </el-menu-item>
            </el-submenu>
        </label>         
    </div>
    
</template>

<script>
import store from '@/store/store.js'
export default {
    data() {
        return {
            NavMenus: [],
            breads:[]
        }       
    },
    mounted () {
        this.setMenu()
    },
    methods:{
        handleMenuSelect(index,indexPath){
            this.breads = indexPath
            console.log(indexPath);    
        },
        setMenu() {
            if (store.getters.menus) {
                this.NavMenus = store.getters.menus
            }
        }
    }
}
</script>


<style>
.el-menu{
    width: 200px!important;
    height: 100%;
    text-align: left;
    /* overflow: scroll; */
}
</style>
