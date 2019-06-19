<template>
    <div id="usertable" class="usertable">
        <el-table
        size="small"
        ref="usertable"
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
            <el-table-column align="center" width="150em;" :label="TableColumn.username" prop="username" ></el-table-column>
            <el-table-column align="center" width="100em;" :label="TableColumn.real_name" prop="real_name" >
                <template slot-scope="scope">
                    <span>{{scope.row.last_name+scope.row.first_name}}</span>
                </template>
            </el-table-column>
            <el-table-column align="center" width="100em;" :label="TableColumn.group" prop="group" >
                <template slot-scope="scope">
                    <el-tag size="small" type="info" v-for="(val,index) in scope.row.group" :key="index">{{val}}</el-tag>
                </template>
            </el-table-column>
            <el-table-column align="center" :label="TableColumn.permissions_group" prop="permissions_group" >
                <template slot-scope="scope">
                    <el-tag size="small" type="info" v-for="(val,index) in scope.row.permissions_group" :key="index">{{val}}</el-tag>
                </template>
            </el-table-column>
            <el-table-column align="center" width="200em;" :label="TableColumn.comment" prop="comment" ></el-table-column>
            <el-table-column align="center" width="100em;" :label="TableColumn.is_active" prop="is_active" >
                <template slot-scope="scope">
                    <el-tag @click.native="handleUserStatus(scope.$index,scope.row)" size="small" v-if="scope.row.is_active" type="success">已启用</el-tag>
                    <el-tag @click.native="handleUserStatus(scope.$index,scope.row)" size="small" v-else type="info">已锁定</el-tag>
                </template>
            </el-table-column>
            <el-table-column align="center" width="100em;" :label="TableColumn.is_superuser" prop="is_superuser" >
                <template slot-scope="scope">
                    <el-tag @click.native="handleUserIsSuper(scope.$index,scope.row)" size="small" v-if="scope.row.is_superuser">Yes</el-tag>
                    <el-tag @click.native="handleUserIsSuper(scope.$index,scope.row)" size="small" v-else type="info">No</el-tag>
                </template>
            </el-table-column>
            
            <el-table-column width="300em;" align="center" label="操作">
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
import { editUser } from '@/api/api.js';
export default {
    name: 'usertable',
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
        handleUserIsSuper($index,row) {
            if (row.is_superuser) {
                this.$confirm('确认取消用户超级管理员权限?', '提示',{
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                })
                .then(_=> {
                    var data = {'id':row.id,'is_superuser': 0}
                    editUser(data).then((response)=>{
                        if (response) {
                            row.is_superuser = false
                        }                
                        }).catch((error)=>{
                            console.log(error);    
                    })    
                })
                .catch(_=>{})
            }
            else {
                this.$confirm('确认赋予用户超级管理员权限?', '提示',{
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                })
                .then(_=> {
                    var data = {'id':row.id,'is_superuser': 1}
                    editUser(data).then((response)=>{
                        if (response) {
                            row.is_superuser = true
                        }                
                        }).catch((error)=>{
                            console.log(error);    
                    })    
                })
                .catch(_=>{})
            }
        },
        handleUserStatus($index,row) {
            if (row.is_active) {
                this.$confirm('确认锁定该用户?', '提示',{
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                })
                .then(_=> {
                    var data = {'id':row.id,'is_active': 0}
                    editUser(data).then((response)=>{
                        if (response) {
                            row.is_active = false
                        }                
                        }).catch((error)=>{
                            console.log(error);    
                    })    
                })
                .catch(_=>{})
            }
            else {
                this.$confirm('确认解锁该用户?', '提示',{
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                })
                .then(_=> {
                    var data = {'id':row.id,'is_active': 1}
                    editUser(data).then((response)=>{
                        if (response) {
                            row.is_active = true
                        }                
                        }).catch((error)=>{
                            console.log(error);    
                    })    
                })
                .catch(_=>{})
            }
        },
    }
}
</script>

<style>
.usertable .el-table th{
    user-select: auto
}
</style>
