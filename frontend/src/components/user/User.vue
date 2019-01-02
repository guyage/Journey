<template>
    <div id="user" class="user">
        <div class="filter-container" style="overflow:hidden; padding-bottom:10px;">
            <el-button @click="changeUpdateButton" style="float: left;" icon="el-icon-edit" size="small" type="primary">添加</el-button>
            <el-input v-on:change="inputchange" v-model="searchcontent" @keyup.enter.native="searchData" style="width: 200px;float: right;" size="small" placeholder="Search">
                <el-button @click="searchData" slot="append" icon="el-icon-search"></el-button>
            </el-input>
        </div>
        <UserTable
        ref="datatable"
        :apiurl="api"
        :getDataDetail="getDataDetail"
        :openDataDialog="openDialog"
        :removeData="delData"                   
        :TableData="results" 
        :TableColumn="columns">
        </UserTable>
        <UserDialog
        ref="datadialog"
        :editurl="editapi"
        :editFun="updateData"
        :apiurl="api"
        :addFun="addData"
        :form="form"
        :rules="rules"
        :show.sync="show">
        </UserDialog>
    </div>
</template>

<script>
import Axios from '@/utils/axios.js';
import axios from 'axios'
import UserTable from './UserTable.vue';
import UserDialog from './UserDialog.vue';
import { user_columns } from '@/global/config.js';
export default {
    name: 'user',
    data() {
        return {
            form: {
                username: '',
                last_name: '',
                first_name: '',
                password: '',
                group: '',
                email: '',
                mobile: '',
                webcat: '',
                comment: ''
            },
            rules: {
                username: [
                    { required: true, message: '请输入用户名', trigger: 'blur' }
                ],
                group: [
                    { required: true, message: '请输入用户组', trigger: 'blur' }
                ],
                email: [
                    { required: true, message: '请输入邮箱', trigger: 'blur' }
                ],
            },
            results: [],
            columns: {},
            api: '/user/',
            show: false,
            resdetail: {},
            editapi: '',
            searchcontent: '',
        }
    },
    methods: {
        // 获取数据列表
        getDataList(url) {
            Axios.oGet(url).then((response)=>{
                if (response) {
                    this.results = response.data
                }                          
            }).catch((error) => {
                console.log('aaa',error);
            })
        },
        // 搜索数据
        searchData() {
            if (this.searchcontent) {
                var searchurl = this.api + '?search=' + this.searchcontent
                this.getDataList(searchurl)
            }
            else {
                this.getDataList(this.api)
            }            
        },
        // 添加数据
        addData(url,data) {    
            Axios.oPost(url,data).then((response)=>{
                if (response) {
                    this.results.push(response.data)
                    this.$message.success('数据保存成功!');
                }                 
            }).catch((error) => {
                console.log(error);
            })
        },
        // 获取数据明细
        getDataDetail(id) {
            this.$refs.datadialog.isUpdate = true
            var url = this.api + id + '/'
            this.editapi = url
            Axios.oGet(url).then((response)=>{
                if (response) {
                    this.resdetail = response.data          
                    this.form = this.resdetail
                }               
            }).catch((error) => {
                console.log(error);
            })
        },
        // 修改数据
        updateData(url,data) {
            Axios.oUpdate(url,data).then((response)=>{
               if (response) {
                   this.getDataList(this.api)
                   this.$message.success('数据编辑成功!');
               }                
            }).catch((error)=>{
                console.log(error);    
            }) 
        },
        // 删除数据
        delData(id) {
            var url = this.api + id + '/'
            Axios.oDelete(url).then((response)=>{
            }).catch((error)=>{
                console.log(error);                
            })
        },
        // 控制弹窗
        openDialog () {
            this.show = true;
        },
        // 控制添加和修改按钮
        changeUpdateButton() {
            this.$refs.datadialog.isUpdate = false;
            this.openDialog()
            // this.$refs.dbdialog.resetForm('form');
        },
        // 搜索框改变触发功能
        inputchange(searchcontent) {
            if(!searchcontent) {
                this.getDataList(this.api) 
            }
        },
    },
    created () {
        this.columns = user_columns;
    },
    mounted() {
        this.getDataList(this.api)        
    },
    components: {
        UserTable,
        UserDialog
    }
}
</script>

<style>

</style>
