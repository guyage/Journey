<template>
    <div id="db">
        <div class="filter-container" style="overflow:hidden; padding-bottom:10px;">
            <el-button @click="changeUpdateButton" style="float: left;" icon="el-icon-edit" size="small" type="primary">添加</el-button>
            <el-input v-on:change="inputchange" v-model="searchcontent" @keyup.enter.native="searchData" style="width: 200px;float: right;" size="small" placeholder="Search">
                <el-button @click="searchData" slot="append" icon="el-icon-search"></el-button>
            </el-input>
        </div>
        <!-- // 对应table -->
        <Table 
        ref="datatable" 
        v-bind:apiurl="api"
        :getDataDetail="getDataDetail"
        :openDataDialog="openDialog"                    
        :removeData="delData" 
        :TableData="results" 
        :TableColumn="columns">
        </Table>
        <DbDialog 
        ref="datadialog" 
        :editurl="editapi" 
        :editFun="updateData"
        :apiurl="api"
        :addFun="addData" 
        :form="dbform" 
        :rules="dbrules"  
        :show.sync="show">
        </DbDialog>
    </div>
</template>

<script>
import axios from 'axios'
import Axios from '@/utils/axios.js';
import Table from '@/components/views/Table.vue';
import DbDialog from './DbDialog.vue';
import { db_columns } from '@/global/config.js';
export default {
    name: 'db',
    data() {
        return {
            dbform: {
                dbname: '',
                host: '',
                port: '',
                adminuser: '',
                password: '',
                version: '',
                comment: '',
                is_enabled: ''
            },
            dbrules: {
                dbname: [
                    { required: true, message: '请输入数据库', trigger: 'blur' }
                ],
                host: [
                    { required: true, message: '请输入IP地址', trigger: 'blur' }
                ],
                port: [
                    { required: true, message: '请输入端口', trigger: 'blur' }
                ],
                version: [
                    { required: true, message: '请输入版本', trigger: 'blur' }
                ],
                is_enabled: [
                    { required: true, message: '请确认是否启用', trigger: 'blur' }
                ]
            },
            results: [],
            columns: {},
            show: false,
            api: '/db/',
            resdetail: {},
            editapi: '',
            searchcontent: '',
        }
    },
    methods: {
        // 获取database列表
        getDataList(url) {         
            Axios.oGet(url).then((response)=>{
                if (response) {
                    this.results = response.data
                }                        
            }).catch((error) => {
                console.log(error);
            })
        },
        // 搜索database
        searchData() {
            if (this.searchcontent) {
                var searchurl = this.api + '?search=' + this.searchcontent
                this.getDataList(searchurl)
            }
            else {
                this.getDataList(this.api)
            }
            
        },
        // 添加database
        addData(url,data) {
            Axios.oPost(url,data).then((response)=>{
                if (response) {
                    this.results.push(response.data)
                    this.$message.success('数据保存成功!');
                }
            }).catch((error)=>{
                console.log(error);
                
            })
        },
        // 获取database明细
        getDataDetail(id) {
            this.$refs.datadialog.isUpdate = true
            var url = this.api + id + '/'
            this.editapi = url
            Axios.oGet(url).then((response)=>{
                if (response) {
                    this.resdetail = response.data          
                    this.dbform = this.resdetail
                }               
            }).catch((error) => {
                console.log(error);
            }) 
        },
        // 修改database信息
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
        // 删除database
        delData(id) {
            var url = this.api + id + '/'
            Axios.oDelete(url).then((response)=>{
            }).catch((error)=>{
                console.log(error);                
            })
        },
        inputchange(value) {
            console.log(value);
        },
        openDialog () {
            this.show = true;
        },
        changeUpdateButton() {
            this.$refs.datadialog.isUpdate = false;
            this.openDialog()
            // this.$refs.dbdialog.resetForm('form');
        }
    },
    
    created () {
        this.columns = db_columns;
    },
    mounted() {
        this.getDataList(this.api)        
    },
    components:{
        Table,
        DbDialog,
    }
}
</script>

<style>

</style>
