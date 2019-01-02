<template>
    <div id="userpermission" class="userpermission">
        <el-dialog
        title="用户权限配置"
        :visible.sync="visible"
        @close="$emit('update:show', false)"
        :show="show"
        :before-close="handleClose">
            <div class="userpermission-accessdb">
                <div class="userpermission-accessdb-title">
                    <span>配置用户可访问数据库：</span>
                </div>
                <div class="userpermission-accessdb-checkbox">
                    <el-checkbox-group size="medium" v-model="useraccessdb">
                        <el-checkbox v-for="(item,index) in dblist"  :key="index" :label="item"></el-checkbox>
                    </el-checkbox-group>
                    <!-- <el-transfer v-model="useraccessdb" :data="dblist"></el-transfer> -->
                </div>
                <div class="userpermission-accessdb-button">
                    <el-button @click="addAccessDb" type="primary">保存</el-button>
                </div>
            </div>
        </el-dialog>
    </div>
</template>

<script>
import Axios from '@/utils/axios.js';
export default {
    data() {
        return {
            visible: this.show,
            useraccessdb: [],
            dblist: [],
            dblistapi: '/db/',
            accessdbapi: '/user/'
        }
    },
    props: {
        // havedb:{
        //     type: Array
        // },
        userid: {
            type: Number
        },
        show: {
            type: Boolean,
            default: false
        }
    },
    methods: {
        addAccessDb() {
            var accessdburl = this.accessdbapi + this.userid.toString() + '/'
            // this.useraccessdb = this.havedb
            // console.log(this.username);
            // console.log(this.useraccessdb);
            var accessdb = {}
            // accessdb.username = this.username
            accessdb.accessdb = this.useraccessdb.toString()
            Axios.oUpdate(accessdburl,accessdb).then((response) => {
                if (response) {
                    this.visible = false
                }
            }).catch((error) => {
                console.log(error); 
            })
        },
        
        // 获取database列表
        getDataList(url) {         
            Axios.oGet(url).then((response)=>{
                if (response) {
                    for (var i=0;i<response.data.length;i++) {
                        this.dblist.push(response.data[i].dbname)
                        // this.dblist.push({key: response.data[i].id ,label: response.data[i].dbname})
                    }
                }                      
            }).catch((error) => {
                console.log(error);
            })
        },
        handleClose(done) {
            this.$confirm('确认关闭!')
                .then(_=> {
                    done();
                })
                .catch(_=>{})
        },  
    },
    watch: {
        show() {
            this.visible = this.show
        }
    },
    mounted() {
        this.getDataList(this.dblistapi)
        // this.useraccessdb = this.havedb
        // console.log('this.useraccessdb',this.useraccessdb);
            
    },
}
</script>

<style>
.userpermission-accessdb-title{
    width: 20%;
    float: left;
}
.el-checkbox-group{
    margin-left: 20%;
}
.el-checkbox{
    display: -webkit-box;
    margin-left: 1%;
    margin-top: 1px;
}
.el-checkbox+.el-checkbox{
    margin-left: 1%;
}
.el-checkbox__label{
    font-size: 16px;
}
.userpermission-accessdb-button{
    margin-top: 30px;
}
</style>
