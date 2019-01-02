<template>
    <div id="usertable" class="usertable">
        <el-table
        size="mini"
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
            <el-table-column align="center" width="200" :label="TableColumn.username" prop="username" ></el-table-column>
            <el-table-column align="center" width="60" :label="TableColumn.last_name" prop="last_name" ></el-table-column>
            <el-table-column align="center" width="60" :label="TableColumn.first_name" prop="first_name" ></el-table-column>
            <!-- <el-table-column align="center"  :label="TableColumn.accessdb" prop="accessdb" ></el-table-column> -->
            <el-table-column align="center"  :label="TableColumn.email" prop="email" ></el-table-column>
            <el-table-column align="center"  :label="TableColumn.mobile" prop="mobile" ></el-table-column>
            <!-- <el-table-column align="center"  :label="TableColumn.webcat" prop="webcat" ></el-table-column> -->
            <!-- <el-table-column align="center" v-for="(val, key, index) in TableColumn" v-if=" key != 'id'" :key="index" :label="val" :prop="key" ></el-table-column> -->
            <el-table-column align="center" width="100" :label="TableColumn.is_active" prop="is_active" >
                <template slot-scope="scope">
                    <el-tag @click.native="handleUserStatus(scope.$index,scope.row)" size="small" v-if="scope.row.is_active" type="success">已启用</el-tag>
                    <el-tag @click.native="handleUserStatus(scope.$index,scope.row)" size="small" v-else type="info">已锁定</el-tag>
                </template>
            </el-table-column> 
            <el-table-column align="center" label="AccessDB" width="100">
                <template slot-scope="scope">
                    <el-button @click="handleAccessDB(scope.$index,scope.row)" size="mini" type="primary" plain>查看</el-button>
                </template>
            </el-table-column> 
            <el-table-column align="center" label="操作" width="260">
            <template slot-scope="scope">
                <el-button class="user-table-button-accessdb" @click="handleConfig(scope.$index,scope.row)" size="mini" type="info">配置数据库</el-button>
                <el-button @click="handleUpdate(scope.$index,scope.row)" size="mini" type="primary">编辑</el-button>
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
        <UserPermission
        ref="userpermission"
        :show.sync="show"
        :userid="userid">
        </UserPermission>
        <el-dialog
        title="AccessDB"
        :visible.sync="accessdbdialog"
        width="30%">
        <el-card shadow="always" class="user-tableb-card">
            <div slot="header" >
                <el-tag>{{cardheader}} </el-tag><span> 可访问数据库：</span>
            </div>
            <div v-for="i in accessdb" :key="i" class="text item">
                {{i}}
            </div>
        </el-card>
        <span slot="footer">
            <el-button @click="accessdbdialog = false">取 消</el-button>
            <el-button type="primary" @click="accessdbdialog = false">确 定</el-button>
        </span>
        </el-dialog>
    </div>
</template>


<script>
import UserPermission from './UserPermission.vue';
import Axios from '@/utils/axios.js';
export default {
    data() {
        return {
            accessdbdialog: false,
            // 分页参数
            total: 0,
            currentPage: 1,
            pagesize: 20,
            show: false,
            userid: 0,
            accessdbapi: '/user/',
            accessdb: '',
            cardheader:''
        }
    },
    props: {
        apiurl: {
            type: String
        },
        TableData: {
            type: Array
        },
        TableColumn: {
            type: Object
        },
        removeData: {
            type: Function
        },
        updateData: {
            type: Function
        },
        getDataDetail: {
            type: Function
        },
        openDataDialog: {
            type: Function
        },
    },
    methods: {
        handleUserStatus($index,row) {
            var url = '/user/' + row.id + '/'
            if (row.is_active) {
                this.$confirm('确认锁定该用户?', '提示',{
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                })
                .then(_=> {
                    var data = {'is_active': 0}
                    Axios.oUpdate(url,data).then((response)=>{
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
                    var data = {'is_active': 1}
                    Axios.oUpdate(url,data).then((response)=>{
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
        handleAccessDB($index,row) {
            this.accessdbdialog = true
            this.cardheader = row.username
            var url = '/userinfo/' + row.username + '/'
            Axios.oGet(url).then((response)=>{
                if (response) {
                    this.accessdb = response.data.accessdb.split(",")
                }                        
            }).catch((error) => {
                console.log(error);
            })
        },
        handleConfig($index,row) {
            this.userid = row.id
            var accessdburl = this.accessdbapi + row.id.toString() + '/'
            Axios.oGet(accessdburl).then((response) => {
                if (response.data.accessdb) {
                    this.$refs.userpermission.useraccessdb = response.data.accessdb.split(",")
                    // this.havedb = response.data.accessdb.split(",")
                    // this.useraccessdb =  response.data.accessdb
                }
                else {
                    this.$refs.userpermission.useraccessdb = []
                }
            }).catch((error) => {
                console.log(error);
            })
            this.openDialog()
        },
        deleteData(index, id) {
            var real_index = index+(this.currentPage - 1) * this.pagesize   
            this.TableData.splice(real_index, 1)
            this.removeData(id)
        },
        handleSelectionChange(val) {
            this.multipleSelection = val;
            console.log(val);           
        },
        handleDelete($index,row) {
            this.$confirm('确认删除?', '提示',{
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            })
            .then(_=> {
                this.deleteData($index,row.id)
                this.$message.success('删除成功!');
            })
            .catch(_=>{})
        },
        handleUpdate($index,row) {
            this.getDataDetail(row.id)
            this.openDataDialog()
        },
        current_change(currentPage){
            this.currentPage = currentPage;
        },
        // 控制弹窗
        openDialog () {
            this.show = true;
        },
    },
    components: {
        UserPermission
    }
}
</script>

<style>
.usertable .el-table--mini, .el-table--small, .el-table__expand-icon{
    font-size: 14px;
}
.usertable .el-card__header{
    text-align: left
}
.usertable .el-card__body{
    text-align: left
}
.usertable .text {
    font-size: 16px;
}
.usertable .user-tableb-card{
    /* width: 480px; */
    /* height: 500px; */

}
.user-table-button-accessdb{
    background-color:darkturquoise;
    border-color:darkturquoise
}
</style>
