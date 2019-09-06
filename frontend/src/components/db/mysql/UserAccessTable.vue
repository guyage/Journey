<template>
    <div id="useraccesstable" class="useraccesstable">
        <el-table
        size="small"
        ref="multipleTable"
        :data="TableData.slice((currentPage-1)*pagesize,currentPage*pagesize)"
        border
        strip
        style="width: 100%"
        @selection-change="handleSelectionChange">           
            <el-table-column align="center" type="selection" width="55"></el-table-column>
            <el-table-column align="center" type="index" label="序号" width="55">
                <template slot-scope="scope"><span>{{scope.$index+(currentPage - 1) * pagesize + 1}} </span></template>
            </el-table-column>    
            <!-- <el-table-column align="center" v-for="(val, key, index) in TableColumn" v-if=" key != 'id'" :key="index" :label="val" :prop="key" ></el-table-column> -->
            <el-table-column align="center" :label="TableColumn.username" width="100" prop="username" ></el-table-column>
            <el-table-column v-if="TableColumn.mysqlinst" align="center" :label="TableColumn.mysqlinst" prop="mysqlinst" ></el-table-column>
            <el-table-column v-if="TableColumn.mongodbinst" align="center" :label="TableColumn.mongodbinst" prop="mongodbinst" ></el-table-column>
            <el-table-column v-if="TableColumn.redisinst" align="center" :label="TableColumn.redisinst" prop="redisinst" ></el-table-column>
            <el-table-column v-if="TableColumn.mysqlinst" align="center" :label="TableColumn.user_access_db" prop="user_access_db" ></el-table-column>
            <el-table-column align="center" :label="TableColumn.create_time" prop="create_time" ></el-table-column>
            <el-table-column align="center" :label="TableColumn.status"  width="100" prop="status" >
                <template slot-scope="scope">
                    <el-tag size="small" type="danger" v-if="scope.row.status == 0">已禁止</el-tag>
                    <el-tag size="small" v-else-if="scope.row.status == 1">申请中</el-tag>
                    <el-tag size="small" type="success" v-else-if="scope.row.status == 2">使用中</el-tag>
                    <el-tag size="small" type="warning" v-else="scope.row.status == 3">已驳回</el-tag>
                </template>
            </el-table-column>
            <el-table-column align="center" :label="TableColumn.comment" prop="comment" ></el-table-column>
            <el-table-column v-if="userissuper" align="center" label="操作">
            <template slot-scope="scope">
                <el-button v-if="scope.row.status == 1" @click="handleEdit(scope.$index,scope.row,'agree')" size="mini" type="primary">同意</el-button>
                <el-button v-if="scope.row.status == 1" @click="handleEdit(scope.$index,scope.row,'reject')" size="mini" type="warning">驳回</el-button>
                <el-button v-if="scope.row.status == 2" @click="handleEdit(scope.$index,scope.row,'ban')" size="mini" type="warning">禁止</el-button>
                <el-button v-if="scope.row.status == 0" @click="handleEdit(scope.$index,scope.row,'grant')" size="mini" type="success">授予</el-button>
                <el-button @click="handleDelete(scope.$index,scope.row)" size="mini" type="danger">删除</el-button>
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
    </div>
</template>

<script>
import store from '@/store/store.js';
export default {
    name: 'useraccesstable',
    data () {
        return {
            // 分页参数
            total: 0,
            currentPage: 1,
            pagesize: 20,
            //
            userissuper: false,
            
        }
    },
    props: {
        TableData: {
            type: Array
        },
        TableColumn: {
            type: Object
        },
        editData: {
            type: Function
        },
        delData: {
            type: Function
        },
    },
    methods: {
        handleSelectionChange(val) {
            this.multipleSelection = val; 
        },
        current_change(currentPage){
            this.currentPage = currentPage;
        },
        handleDelete($index,row) {
            this.$confirm('确认删除?', '提示',{
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            })
            .then(_=> {
                var real_index = $index+(this.currentPage - 1) * this.pagesize  
                this.TableData.splice(real_index, 1)
                this.delData(row.id)
            })
            .catch(_=>{})
        },
        handleEdit($index,row,action) {
            let data = {}
            let info = ''
            if (action == 'agree') {
                data = {'id':row.id,'status':2}
                info = '确认同意用户权限申请?'
            }
            else if (action == 'reject') {
                data = {'id':row.id,'status':3}
                info = '确认驳回用户权限申请?'
            }
            else if (action == 'ban') {
                data = {'id':row.id,'status':0}
                info = '确认禁止用户权限?'
            }
            else if (action == 'grant') {
                data = {'id':row.id,'status':2}
                info = '确认重新授予用户权限?'
            }
            this.$confirm(info, '提示',{
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                })
                .then(_=> {
                    var real_index = $index+(this.currentPage - 1) * this.pagesize
                    this.TableData[real_index].status = data.status
                    this.editData(data)
                    
                })
                .catch(_=>{})
        },
    },
    mounted() {
        this.userissuper = store.getters.userissuper
    },
}
</script>

<style>
.useraccesstable .el-table th{
    user-select: auto
}
</style>
