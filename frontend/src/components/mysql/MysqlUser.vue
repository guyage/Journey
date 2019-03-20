<template>
    <div class="mysqluser">
        <div class="mysqluser-inst">
            <el-select  v-model="selectinst" placeholder="请选择查询数据库" @change="handleSelect">
                <el-option 
                v-for="item in instlist" 
                :key="item.id"
                :label="item.id"
                :value="item.instname">
                </el-option>
            </el-select>
            <el-button style="margin-left: 5px;" type="primary" @click="getUserList">获取用户</el-button>
            
            <el-input v-model="searchcontent" @keyup.enter.native="searchData" style="width: 200px;float: right;" placeholder="Search">
                <el-button @click="searchData" slot="append" icon="el-icon-search"></el-button>
            </el-input>
            <el-button style="float: right;margin-right: 5px;"  type="primary" @click="addMysqlUser">添加用户</el-button>
        </div>
        <div v-if="results.length > 0" class="mysqluser-results">
            <div class="mysqluser-results-tag">
                <el-tag >该实例包含数据库：</el-tag>
                <el-tag v-for="(val, key) in dblist" :key="key">{{val}}</el-tag>
            </div>
            <el-table v-if="results.length > 0" size="mini" style="width: 100%" highlight-current-row max-height="500" border :data="results.slice((currentPage-1)*pagesize,currentPage*pagesize)">
                <el-table-column  align="center" v-for="(val, key) in col" :fixed="key===0?true:false" :key="key" :label="val" :prop="val">
                </el-table-column>
                <el-table-column width="500px" align="center" label="操作">
                <template slot-scope="scope">
                    <el-button size="mini" type="primary" plain @click="handleShowUser(scope.$index,scope.row)">查看权限</el-button>
                    <el-button size="mini" type="danger" plain @click="handleDropUser(scope.$index,scope.row)">删除</el-button>
                </template>
                </el-table-column>
            </el-table>
            <el-pagination
            v-if="results.length > 0"
            background
            layout="total, sizes,prev, pager, next, jumper"
            :total="results.length"
            :page-sizes="[10, 20, 30]"
            :page-size="pagesize"
            @current-change="handleCurrentChange"
            @size-change="handleSizeChange">
            </el-pagination>
        </div>
        <div class="mysqluser-userpriresults">
            <el-dialog
            :title="isadduser?'添加MySQL用户':'用户权限'"
            :visible.sync="dialogVisible"
            width="50%">
            <div v-if="isadduser">
                <div class="mysqluser-userpri-adduser">
                    <el-form ref="userform" :model="userform" label-width="100px">
                        <el-form-item label="用户名：">
                            <el-input style="width: 300px; float: left;" v-model="userform.username"></el-input>
                        </el-form-item>
                        <el-form-item label="IP：">
                            <el-input style="width: 300px; float: left;" v-model="userform.userip"></el-input>
                        </el-form-item>
                        <el-form-item label="用户密码：">
                            <el-input style="width: 300px; float: left;" v-model="userform.userpwd"></el-input>
                        </el-form-item>
                        <el-form-item label="数据库操作：">
                            <el-checkbox-group v-model="userform.userpri">
                            <el-checkbox label="SELECT" name="userpri"></el-checkbox>
                            <el-checkbox label="INSERT" name="userpri"></el-checkbox>
                            <el-checkbox label="UPDATE" name="userpri"></el-checkbox>
                            <el-checkbox label="DELETE" name="userpri"></el-checkbox>
                            </el-checkbox-group>
                        </el-form-item>
                        <el-form-item label="数据库：">
                            <el-radio-group v-model="userform.userpridb">
                            <el-radio v-for="(val, key) in dblist" :key="key" :label="val"></el-radio>
                            <!-- <el-radio label="线下场地免费"></el-radio> -->
                            </el-radio-group>
                        </el-form-item>
                        <el-form-item>
                            <el-button type="primary" @click="saveUser">添加</el-button>
                            <el-button @click="dialogVisible = false">取消</el-button>
                        </el-form-item>
                    </el-form>
                </div>
                <div class="mysqluser-userpri-adduser-button">
                    <!-- <el-button @click="addAccessDb" type="primary">保存</el-button> -->
                </div>
            </div>
            <div v-if="!isadduser">
                <el-card shadow="always" class="user-tableb-card">
                <div slot="header" >
                    <span>用户</span><el-tag>{{selectuser}}</el-tag><span>权限如下：</span>
                </div>
                <div v-for="i in userpriresults" :key="i" class="text item">
                    {{i}}
                </div>
            </el-card>
            <span slot="footer">
                <el-button style="margin-top: 10px;" @click="dialogVisible = false">取 消</el-button>
                <el-button style="margin-top: 10px;" type="primary" @click="dialogVisible = false">确 定</el-button>
            </span>
            </div>
            </el-dialog>
        </div>
    </div>
</template>

<script>
import Axios from '@/utils/axios.js';
export default {
    name: 'mysqluser',
    data () {
        return {
            searchcontent: '',
            // 用户权限弹出框参数
            dialogVisible: false,
            // 分页参数
            total: 0,
            currentPage: 1,
            pagesize: 20,
            currenttab: 0,
            selectinst: '',
            instlist: [],
            results: [],
            col: [],
            userpri: '',
            userpricol: [],
            userpriresults: [],
            selectuser: '',
            dblist: [],
            // 添加用户参数
            isadduser: false,
            userform: {
                username: '',
                userip: '',
                userpwd: '',
                userpri: [],
                userpridb: ''
            }
            

        }
    },
    methods: {
        searchData() {
            this.results = this.results.filter(item => item[this.col[0]].includes(this.searchcontent))
        },
        handleCurrentChange(currentPage){
            this.currentPage = currentPage;
        },
        handleSizeChange(val){
            this.pagesize = val;
        },
        handleSelect(val){
            this.selectinst = val  
        },
        handleDropUser($index,row){
            var real_index = $index+(this.currentPage - 1) * this.pagesize
            var dropinfo = '确认删除<strong style="color:red;">'+this.selectinst+'</strong>中用户' + '<strong style="color:red;">' +row['user@host']+ '</strong>'
            this.results.splice(real_index, 1)
            this.$confirm(dropinfo, '提示',{
                dangerouslyUseHTMLString: true,
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            })
            .then(_=> {
                this.dropUser(row['user@host'])
                this.$message.success('删除成功!');
            })
            .catch(_=>{})
        },
        dropUser(user) {
            var url = '/mysqluser/'
            var request_data = {}
            request_data.type = 'dropuser'
            request_data.instname = this.selectinst
            request_data.user = user
            Axios.oPost(url,request_data).then((response)=>{
                if (response) {
                    if (response.data.col[0] == 'ok') {
                        this.$message.success('MySQL用户删除成功!');
                        
                    }
                    else {
                        this.$message.error('MySQL用户删除失败!');
                    }
                }                        
            }).catch((error) => {
                console.log(error);
            })
        },
        handleShowUser($index,row){
            this.dialogVisible = true
            this.isadduser = false
            this.selectuser = row['user@host']
            this.showUserPri(this.selectuser)
        },
        addMysqlUser() {
            if (this.selectinst) {
                this.dialogVisible = true
                this.isadduser = true
                var url = '/mysqluser/'
                var request_data = {}
                request_data.type = 'adduserlist'
                request_data.instname = this.selectinst
                Axios.oPost(url,request_data).then((response)=>{
                    if (response) {
                        this.dblist = response.data.dblist
                    }                        
                }).catch((error) => {
                    console.log(error);
                })
            }
            
        },
        saveUser(){
            console.log(this.userform);
            var url = '/mysqluser/'
            var request_data = {}
            request_data.type = 'adduser'
            request_data.instname = this.selectinst
            request_data.grantuser = this.userform
            Axios.oPost(url,request_data).then((response)=>{
                if (response) {
                    this.dialogVisible = false
                    if (response.data.col[0] == 'ok') {
                        var adduser = this.userform.username + '@' + '\'' +this.userform.userip + '\''
                        this.results.push(adduser)
                        this.$message.success('MySQL用户添加成功!');
                    }
                    else {
                        this.$message.error('MySQL用户添加失败!');
                    }
                }                        
            }).catch((error) => {
                console.log(error);
            })
            
        },
        showUserPri(user){
            var url = '/mysqluser/'
            var request_data = {}
            request_data.type = 'showuserpri'
            request_data.instname = this.selectinst
            request_data.user = user
            Axios.oPost(url,request_data).then((response)=>{
                if (response) {
                    this.userpricol = response.data.col
                    this.userpriresults = response.data.results
                }                        
            }).catch((error) => {
                console.log(error);
            })
        },
        getUserList() {
            if (this.instlist) {
                var url = '/mysqluser/'
                var request_data = {}
                request_data.type = 'showusers'
                request_data.instname = this.selectinst
                Axios.oPost(url,request_data).then((response)=>{
                    if (response) {
                        this.col = response.data.col
                        this.results = response.data.results
                        this.dblist = response.data.dblist
                    }                        
                }).catch((error) => {
                    console.log(error);
                })
            }
        },
        getInstList() {
            var url = '/mysqlinst/'
            Axios.oGet(url).then((response)=>{
                if (response) {
                    for (var i =0; i< response.data.length;i++) {
                        var insts = {}
                        insts.id = i
                        insts.instname = response.data[i].instname
                        this.instlist.push(insts)
                    }
                }                        
            }).catch((error) => {
                console.log(error);
            })
        }
    },
    mounted() {
        this.getInstList()
    },
}
</script>

<style>
.mysqluser .mysqluser-inst{
    float: left;
    width: 100%;
}
.mysqluser .mysqluser-inst .el-select,.mysqluser .mysqluser-inst .el-button--primary{
    float: left;
}
.mysqluser .el-table--mini, .el-table--small, .el-table__expand-icon{
    font-size: 14px;
}
.mysqluser .mysqluser-results-db{
    clear: both;
    float: left;
}
.mysqluser .mysqluser-results-tag{
    clear: both;
    float: left;
    padding-top: 0.5em;
}
.mysqluser-userpriresults .el-tag{
    float: none;
}
.mysqluser-userpriresults .el-card__header{
    text-align: left
}
.mysqluser-userpriresults .el-card__body{
    text-align: left
}
.mysqluser-userpriresults .text {
    font-size: 16px;
}
.mysqluser-userpri-adduser .el-checkbox{
    display: table-cell;
    padding-right: 15px;
}
.mysqluser-userpri-adduser .el-checkbox__label{
    padding-left: 5px;
}
.mysqluser-userpri-adduser .el-form-item__content{
    position: absolute;
}
</style>
