<template>
    <div id="generaltable" class="generaltable">
        <el-table
        size="small"
        ref="generaltable"
        :data="TableData.slice((currentPage-1)*pagesize,currentPage*pagesize)"
        border
        strip
        style="width: 100%"
        @selection-change="handleSelectionChange">           
            <el-table-column align="center" type="selection" width="55"></el-table-column>
            <el-table-column align="center" type="index" label="序号" width="55">
                <template slot-scope="scope"><span>{{scope.$index+(currentPage - 1) * pagesize + 1}} </span></template>
            </el-table-column>    
            <el-table-column align="center" v-for="(val, key, index) in TableColumn" v-if=" key != 'id'" :key="index" :label="val" :prop="key" ></el-table-column>
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
    name: 'generaltable',
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
.generaltable .el-table th{
    user-select: auto
}
</style>
