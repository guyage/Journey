<template>
    <div id="navmenu" class="navmenu" >
        <label v-for="parentMenu in NavMenus" :key="parentMenu.id">
            
            <el-menu-item v-if="parentMenu.children.length == 0" :index="parentMenu.name" :route="parentMenu.path">
                <!-- <template slot="title"> -->
                    <icon-svg class="navmenu-menu-icon" :iconClass="parentMenu.icon"></icon-svg>
                    <span>{{ parentMenu.name }}</span>
                <!-- </template> -->
            </el-menu-item>
            <el-submenu v-if="parentMenu.children.length != 0" :index="parentMenu.name" :route="parentMenu.path">
                <template slot="title">
                    <icon-svg class="navmenu-menu-icon" :iconClass="parentMenu.icon"></icon-svg>
                    <span>{{ parentMenu.name }}</span>
                </template>
                    <el-menu-item v-for="childMenu in parentMenu.children" :key="childMenu.id" v-if="childMenu.mtype !=2" :index="childMenu.name" :route="childMenu.path">
                        <template slot="title">
                            <icon-svg class="navmenu-menu-icon" :iconClass="childMenu.icon"></icon-svg>
                        <span >{{ childMenu.name }}</span>
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
            breads:[],
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
            if (store.getters.menu) {
                this.NavMenus = store.getters.menu
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
}
.navmenu-menu-icon.svg-icon{
    margin-right: 0.5em;
}
</style>
