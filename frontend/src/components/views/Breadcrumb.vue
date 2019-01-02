<template>
    <div id="breadcrumb" class="breadcrumb">
        <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item v-for="(item,index) in $route.meta.title" :key="index" >{{item}}</el-breadcrumb-item>
        <!-- <el-breadcrumb-item v-for="(bread,key) in currentPath" :key="key" >{{bread}}</el-breadcrumb-item> -->
        <!-- <icon-svg iconClass="icon-Logout"></icon-svg> -->
            <div class="right-header" id="right-header">
                <el-button title="个人中心" class="userinfo-button" @click="handleLoginOut" size="mini" circle>
                    <icon-svg class="right-header-icon" iconClass="icon-user"></icon-svg>
                </el-button>
                <el-button title="退出" class="logout-button" @click="handleLoginOut" size="mini" circle >
                    <icon-svg class="right-header-icon" iconClass="icon-Logout"></icon-svg>
                </el-button>
            </div>
        </el-breadcrumb>
        
    </div>
</template>

<script>
import store from '@/store/store.js'
import Axios from '@/utils/axios.js';
export default {
    methods: {
        handleLoginOut () {
            this.$confirm('确认退出？', '提示', {
                confirmButtonText: '确认',
                cancelButtonText: '取消',
                type: 'warning'
            })
            .then(() => {
                Axios.oGet('/logout').then((response) => {
                    if (response) {
                        this.$store.dispatch('LoginOut').then(() =>{
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
