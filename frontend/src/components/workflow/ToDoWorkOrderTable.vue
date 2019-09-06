<template>
    <div class="todoworkordertable">
        <el-row>
            <el-table
            size="mini"
            ref="multipleTable"
            :data="TableData.slice((currentPage-1)*pagesize,currentPage*pagesize)"
            strip
            style="width: 100%">
                <el-table-column type="expand">
                    <template slot-scope="props">
                        <el-form size="mini" label-position="left" inline class="demo-table-expand">
                            <el-form-item v-for="(val, key, index) in JSON.parse(props.row['content'])" :key="index" :label="key+':'">
                                <span>{{val}}</span>
                            </el-form-item>
                        </el-form>
                    </template>
                </el-table-column>
                <el-table-column align="center" :label="TableColumn.id" width="150" prop="id">
                    <template slot-scope="scope">
                        <el-link :href="'#/workorderdetail/'+'OpsOnline'+'-'+scope.row.id" type="primary">OpsOnline-{{scope.row.id}}</el-link>
                    </template>
                </el-table-column>
                <el-table-column align="center" :label="TableColumn.title" prop="title"></el-table-column>
                <el-table-column width="150" align="center" :label="TableColumn.status" prop="status" >
                    <template slot-scope="scope">
                        <el-tag size="small" type="success" v-if="scope.row.status == 2">已同意</el-tag>
                        <el-tag size="small" type="success" v-else-if="scope.row.status == 3">已完成</el-tag>
                        <el-tag size="small" type="danger" v-else-if="scope.row.status == 0">已终止</el-tag>
                        <el-tag size="small" type="danger" v-else-if="scope.row.status == -1">已失败</el-tag>
                        <el-tag size="small" type="danger" v-else-if="scope.row.status == 4">已驳回</el-tag>
                        <el-tag size="small" v-else="scope.row.status == 1">审批中</el-tag>
                    </template>
                </el-table-column>
                <el-table-column width="150" align="center" :label="TableColumn.creator" prop="creator"></el-table-column>
                <el-table-column width="200" align="center" :label="TableColumn.create_time" prop="create_time" >
                    <template slot-scope="scope">
                        {{scope.row.create_time | dateFormate}}
                    </template>
                </el-table-column>
                <el-table-column width="200" align="center" :label="TableColumn.update_time" prop="update_time" >
                    <template slot-scope="scope">
                        {{scope.row.update_time | dateFormate}}
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination
            background
            layout="total, prev, pager, next, jumper"
            :total="TableData.length"
            :page-size="pagesize"
            @current-change="current_change">
            </el-pagination>
        </el-row>
    </div>
</template>

<script>
import moment from 'moment';
import store from '@/store/store.js';
export default {
    name: 'todoworkordertable',
    data () {
        return {
            // 分页参数
            total: 0,
            currentPage: 1,
            pagesize: 15,
            
        }
    },
    props: {
        TableData: {
            type: Array
        },
        TableColumn: {
            type: Object
        },
    },
    filters: {
        dateFormate(date) {
            return moment(date).format("YYYY-MM-DD HH:mm:ss");
        }
    },
    methods: {
        current_change(currentPage){
            this.currentPage = currentPage;
        },
    }
}
</script>

<style>
.todoworkordertable .el-table__expanded-cell[class*=cell]{
    padding: 5px 62px;
}
.todoworkordertable .demo-table-expand {
    font-size: 0;
}
.todoworkordertable .demo-table-expand label {
    /* width: 100px; */
    font-size: 12px;
    color: #99a9bf;
}
.todoworkordertable .el-form-item__content{
    font-size: 12px;
}
.todoworkordertable .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 100%;
}
.todoworkordertable .el-table th{
    user-select: auto
}
</style>