<template>
    <div class="permstables">
        <el-table
        size="small"
        :data="TableData.slice((currentPage-1)*pagesize,currentPage*pagesize)"
        :tree-props="{children: 'children', hasChildren: 'hasChildren'}"
        row-key="id"
        border
        strip>
            <el-table-column prop="api" :label="TableColumn.api"></el-table-column>
            <el-table-column prop="name" :label="TableColumn.name"></el-table-column>
            <el-table-column prop="perms" :label="TableColumn.perms"></el-table-column>
            <el-table-column prop="del_flag" :label="TableColumn.del_flag">
                <template slot-scope="scope">
                    <el-tag size="small" style="color:#13c2c2;background-color:#e6fffb;border-color:#87e8de" v-if="scope.row.del_flag == 0">正常</el-tag>
                    <el-tag size="small" v-else-if="scope.row.del_flag == -1" type="info">禁用</el-tag>
                </template>
            </el-table-column>
            <el-table-column width="300em;" align="center" label="操作">
            <template slot-scope="scope">
                <el-button v-if="scope.row.del_flag == 0" @click="handleData(scope.$index,scope.row,'disable')" size="mini" type="warning">禁用</el-button>
                <el-button v-if="scope.row.perms == ''" @click="handleDelData(scope.$index,scope.row)" size="mini" type="danger">删除</el-button>
                <el-button v-else-if="scope.row.del_flag == -1" @click="handleData(scope.$index,scope.row,'enable')" size="mini" type="success">启用</el-button>
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
    name: 'permstables',
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
        delData: {
            type: Function
        },
        editData: {
            type: Function
        },
    },
    methods: {
        current_change(currentPage){
            this.currentPage = currentPage;
        },
        handleDelData(index,row) {
            this.$confirm('确认删除?', '提示',{
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            })
            .then(_=> {
                console.log(row);
                this.delData({'id':row.id})
                // this.delData(row.id).then((response) => {
                //     this.$message.success('删除成功!');
                // })
            })
            .catch(_=>{})
        },
        handleData(index,row,type) {
            if (type == 'edit') {
                console.log(row);
                
            }
            else if (type == 'disable') {
                let req_data = {'id':row.id,'del_flag':-1}
                this.editData(req_data)
            }
            else if (type == 'enable') {
                let req_data = {'id':row.id,'del_flag':0}
                this.editData(req_data)
            }
        },
    }
}
</script>

<style>

</style>