<template>
    <div id="myworkorder" class="myworkorder">
        <el-collapse v-model="activeNames">
            <el-collapse-item title="我创建的" name="1">
                <div class="user-operation" style="padding: 0.8em 0em 1em;">
                    <!-- <el-button @click="handleNeworder" style="float: left;" icon="el-icon-edit" size="small" type="primary">新建工单</el-button> -->
                    <!-- <el-select size="small" style="float: left;padding-left: 1px;" v-model="ordertype" @change="handleChange($event)" placeholder="请选择工单类型">
                        <el-option v-for="(val,index) in ordertypelist" :key="index" :label="val" :value="val" ></el-option>
                    </el-select> -->
                    <el-input v-model="searchcontent" @keyup.enter.native="searchData" style="width: 200px;float: right;" size="small" placeholder="Search">
                        <el-button @click="searchData" slot="append" icon="el-icon-search"></el-button>
                    </el-input>
                </div>
                <br>
                <!-- <el-divider></el-divider> -->
                <WorkOrderTable
                :TableColumn="table_columns"
                :TableData="table_data">
                </WorkOrderTable>
            </el-collapse-item>
        </el-collapse>     
    </div>
</template>

<script>
import store from '@/store/store.js';
import WorkOrderTable from './WorkOrderTable.vue';
import { getWorkOrder } from '@/api/api.js';
export default {
    name: 'myworkorder',
    components: {
        WorkOrderTable,
    },
    data() {
        return {
            activeNames: ['1'],
            searchcontent: '',
            ordertype: '',
            ordertypelist: ['git','email'],
            userpermissionsgroup: [],
            //我创建的工单列表
            table_data: [],
            table_columns: {
                title: '主题',
                order_type: '工单类型',
                status: '工单状态',
                creator: '创建人',
                
                // operator: '操作人',
                create_time: '创建时间',
                update_time: '更新时间',
                comment: '备注'
            },
        }
    },
    watch: {
        // 如果路由发生变化，再次执行该方法
        "$route": "getMyWorkOrder"
    },
    methods: {
        handleChange(val) {
            console.log();            
        },
        handleNeworder() {
            this.$router.push({ path: '/newworkorder'}) 
        },
        searchData() {
            if (this.searchcontent) {
                searchUserAccessMysql({searchcontent:this.searchcontent}).then((response) => {
                    this.table_data = response.data
                }).catch((error) => {
                    console.log(error);
                })
            }
            else {
                this.getDataList()
            }
        },
        getMyWorkOrder() {
            getWorkOrder().then((response) => {
                this.table_data = response.data
            }).catch((error) => {
                console.log(error);
            })
        },
    },
    mounted() {
        this.getMyWorkOrder()
    },

}
</script>

<style>
.myworkorder .el-collapse-item__header.is-active,.myworkorder .el-collapse-item__header{
    font-size: 16px;
    font-weight: bold;
    padding-left: 0.5em;
    border-bottom: 1px solid #dcdfe6;
}
</style>
