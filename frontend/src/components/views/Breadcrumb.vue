<template>
    <div id="breadcrumb" class="breadcrumb">
        <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item v-for="(item,index) in $route.meta.title" :key="index" >{{item}}</el-breadcrumb-item>
        <!-- <el-breadcrumb-item v-for="(bread,key) in currentPath" :key="key" >{{bread}}</el-breadcrumb-item> -->
        <!-- <icon-svg iconClass="icon-Logout"></icon-svg> -->
            <div class="right-header" id="right-header">
                <el-button title="项目GitHub" class="userinfo-button" @click="handleOpengit" size="mini" circle>
                    <icon-svg class="right-header-icon" iconClass="icongithub-fill"></icon-svg>
                </el-button>
                <el-button title="退出" class="logout-button" @click="handleLogout" size="mini" circle >
                    <icon-svg class="right-header-icon" iconClass="iconpoweroff"></icon-svg>
                </el-button>
            </div>
        </el-breadcrumb>
        
    </div>
</template>

<script>
import store from '@/store/store.js'
import { Logout } from '@/api/api.js'
export default {
    methods: {
        handleLogout () {
            this.$confirm('确认退出？', '提示', {
                confirmButtonText: '确认',
                cancelButtonText: '取消',
                type: 'warning'
            })
            .then(() => {
                Logout().then((response) => {
                    if (response) {
                        this.$store.dispatch('Logout').then(() =>{
                            this.$router.push({name:'login'})
                            // console.log(this.$router);
                            window.location.reload();                            
                        })
                        // this.$router.options.routes = []
                    }
                }).catch((error) => {
                    console.log(error); 
                })
            }).catch(() =>{   
            })
        },
        handleOpengit () {
            this.$confirm('是否打开项目GitHub？如有帮助，请start支持下。', '提示', {
                confirmButtonText: 'Yes',
                cancelButtonText: 'No',
                type: 'warning',
                dangerouslyUseHTMLString: true
            })
            .then(() => {
                window.open("https://github.com/guyage/Journey");  
            }).catch(() =>{   
            })
        }
    }
}
</script>

<style>
.breadcrumb .el-breadcrumb{
    line-height: 45px;
    border-bottom: 1px solid #ebeef5;
    height: 45px;
}
.breadcrumb .right-header{
    position: absolute;
    right: 20px;
}
.breadcrumb .userinfo-button.el-button.el-button{
    border: 0px;
    margin-left: 0px;
}
.breadcrumb .logout-button.el-button.el-button{
    border: 0px;
    margin-left: 0px;
}
.breadcrumb .right-header-icon.svg-icon{
    width:20px;
    height:20px;
}
</style>
