<template>
    <div class="todoworkorder">
        <el-row>
            <WorkOrderTable
            :TableColumn="table_columns"
            :TableData="table_data"
            :TableFilterData="ordertypenamelist">
            </WorkOrderTable>
        </el-row>
    </div>
</template>

<script>
import {getToDoWorkOrder,getWorkOrderType} from '@/api/workflow.js';
import WorkOrderTable from './WorkOrderTable.vue';
export default {
    name: 'todoworkorder',
    components: {
        WorkOrderTable,
    },
    data() {
        return {
            table_data: [],
            table_columns: {
                id: '工单号',
                ordertypename: '工单类型',
                title: '主题',
                status: '工单状态',
                creator: '创建人',
                create_time: '创建时间',
                update_time: '更新时间',
            },
            ordertypenamelist: [],
        }
    },
    watch: {
        // 如果路由发生变化，再次执行该方法
        "$route": "getToDoWorkOrderData"
    },
    methods: {
        getToDoWorkOrderData() {
            getToDoWorkOrder().then((response) => {
                this.table_data = response.data.results
            })
        },
        getWorkOrderTypeName() {
            getWorkOrderType().then((response) => {
                for (let i=0;i<response.data.length;i++) {
                    let ordertype_name = response.data[i].ordertype
                    this.ordertypenamelist.push({'text':ordertype_name,'value':ordertype_name})
                }
            })
        }
    },
    mounted () {
        this.getToDoWorkOrderData()
        this.getWorkOrderTypeName()
    }
}
</script>

<style>

</style>