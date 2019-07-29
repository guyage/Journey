<template>
    <div class="todoworkorder">
        <el-collapse v-model="activeNames">
            <el-collapse-item title="我的待办" name="1">
                <div class="user-operation" style="padding: 0.8em 0em 1em;">
                    <el-button @click="handleBatch" style="float: left;" size="small" type="primary">批量同意</el-button>
                    <!-- <el-select size="small" style="float: left;padding-left: 1px;" v-model="ordertype" @change="handleChange($event)" placeholder="请选择工单类型">
                        <el-option v-for=" (val,index) in ordertypelist" :key="index" :label="val" :value="val" ></el-option>
                    </el-select> -->
                    <!-- <el-input v-model="searchcontent" @keyup.enter.native="searchData" style="width: 200px;float: right;" size="small" placeholder="Search">
                        <el-button @click="searchData" slot="append" icon="el-icon-search"></el-button>
                    </el-input> -->
                </div>
                <ToDoWorkOrderTable
                ref="todoworkordertable"
                :TableColumn="table_columns"
                :TableData="table_data"
                :editData="editData">
                </ToDoWorkOrderTable>
            </el-collapse-item>
        </el-collapse>
    </div>
</template>

<script>
import store from '@/store/store.js';
import ToDoWorkOrderTable from './ToDoWorkOrderTable.vue';
import { ToDoWorkOrder,ChangeWorkOrderState } from '@/api/api.js';
export default {
    name: 'todoworkorder',
    components: {
        ToDoWorkOrderTable,
    },
    data () {
        return {
            activeNames: ['1'],
            //我的待办
            table_data: [],
            table_columns: {
                title: '主题',
                status: '工单状态',
                creator: '申请人',
                // operator: '操作人',
                create_time: '创建时间',
                update_time: '更新时间',
                comment: '备注'
            },
        }
    },
    watch: {
        // 如果路由发生变化，再次执行该方法
        "$route": "getDataList"
    },
    methods: {
        handleBatch() {
            let change_data = {};
            change_data.changetype = 'agree'
            change_data.operator = store.getters.username
            let batch_workorder = this.$refs.todoworkordertable.multipleSelection
            let workorderidlist = []
            for (let i=0;i<batch_workorder.length;i++) {
                workorderidlist.push(batch_workorder[i].id)
            }
            change_data.workorderid = workorderidlist
            this.editData(change_data)
        },
        getDataList() {
            ToDoWorkOrder({'username':store.getters.username}).then((response) => {
                this.table_data = response.data.results
            }).catch((error) => {
                console.log(error);
            })
        },
        editData(change_data) {
            ChangeWorkOrderState(change_data).then((response) => {
                this.getDataList()
            }).catch((error) => {
                console.log(error);
            })
        },
    },
    mounted() {
        this.getDataList()
    },
}
</script>

<style>
.todoworkorder .el-collapse-item__header.is-active,.todoworkorder .el-collapse-item__header{
    font-size: 16px;
    font-weight: bold;
    padding-left: 0.5em;
    border-bottom: 1px solid #dcdfe6;
}
</style>
