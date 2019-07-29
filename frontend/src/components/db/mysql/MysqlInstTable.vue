<template>
    <div id="mysqlinsttable" class="mysqlinsttable">
        <el-table
        size="small"
        ref="mysqlinsttable"
        :data="TableData.slice((currentPage-1)*pagesize,currentPage*pagesize)"
        border
        strip
        style="width: 100%"
        @selection-change="handleSelectionChange">      
            <el-table-column align="center" type="selection" width="55"></el-table-column>
            <el-table-column align="center" type="index" label="序号" width="55">
                <template slot-scope="scope"><span>{{scope.$index+(currentPage - 1) * pagesize + 1}} </span></template>
            </el-table-column>
            <el-table-column align="center" :label="TableColumn.inst_name" prop="inst_name" ></el-table-column>
            <el-table-column align="center" width="100" :label="TableColumn.inst_host" prop="inst_host" ></el-table-column>
            <el-table-column align="center" width="80" :label="TableColumn.inst_port" prop="inst_port" ></el-table-column>
            <el-table-column align="center" width="80" :label="TableColumn.role" prop="role">
                <template slot-scope="scope">
                    <el-tag size="small" :type="scope.row.role=='Master'?'':'warning'">{{scope.row.role}}</el-tag>
                </template>
            </el-table-column>
            <el-table-column align="center" :label="TableColumn.manage_user" prop="manage_user" ></el-table-column>
            <el-table-column align="center" :label="TableColumn.read_user" prop="read_user" ></el-table-column>
            <el-table-column align="center" :label="TableColumn.services" prop="services" ></el-table-column>
            <el-table-column align="center" width="80" :label="TableColumn.version" prop="version" ></el-table-column>
            <el-table-column align="center" width="100" :label="TableColumn.is_enabled" prop="is_enabled" >
                <template slot-scope="scope">
                    <el-tag size="small" :type="scope.row.is_enabled=='ENABLED'?'success':'info'">{{scope.row.is_enabled}}</el-tag>
                </template>
            </el-table-column>
            <el-table-column align="center" :label="TableColumn.comment" prop="comment" ></el-table-column>
            <el-table-column align="center" label="操作" width="150">
                <template slot-scope="scope">
                    <el-button @click="handleEdit(scope.$index,scope.row)" size="mini" type="primary">编辑</el-button>
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
export default {
    name: 'mysqlinsttable',
    data () {
        return {
            // 分页参数
            total: 0,
            currentPage: 1,
            pagesize: 20,
        }
    },
    props: {
        TableData: {
            type: Array
        },
        TableColumn: {
            type: Object
        },
        delData: {
            type: Function
        },
        editData: {
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
        handleEdit($index,row) {
            this.editData(row.id)
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
                this.delData(row.id).then((response) => {
                    this.$message.success('删除成功!');
                })
            })
            .catch(_=>{})
        },
    }
}
</script>

<style>
.mysqlinsttable .el-table th{
    user-select: auto
}
</style>
