<template>
    <div class="mysqluser">
        <div class="mysqluser-inst">
            <!-- <span style="float: left;margin-top: 5px;">MySQL实例：</span> -->
            <el-select  v-model="selectinst" placeholder="请选择MySQL实例" @change="handleSelect($event)">
                <el-option 
                v-for="item in instlist" 
                :key="item.instid"
                :label="item.instname"
                :value="item.instid">
                </el-option>
            </el-select>
            <el-input size="small" v-model="searchcontent" @keyup.enter.native="searchData" style="width: 200px;float: right;" placeholder="Search">
                <el-button @click="searchData" slot="append" icon="el-icon-search"></el-button>
            </el-input>
            <el-button size="small" style="float: right;margin-right: 5px;"  type="primary" @click="addMysqlUser">添加用户</el-button>
        </div>
        <div v-if="results.length > 0" class="mysqluser-results">
            <div class="mysqluser-results-tag">
                <el-tag >该实例包含数据库：</el-tag>
                <el-tag v-for="(val, key) in dblist" :key="key">{{val}}</el-tag>
            </div>
            <el-table v-if="results.length > 0" size="mini" style="width: 100%" highlight-current-row max-height="700" border :data="results.slice((currentPage-1)*pagesize,currentPage*pagesize)">
                <el-table-column  align="center" v-for="(val, key) in col" :fixed="key===0?true:false" :key="key" :label="val" :prop="val">
                </el-table-column>
                <el-table-column width="500px" align="center" label="操作">
                <template slot-scope="scope">
                    <el-button size="mini" type="primary"  @click="handleShowUser(scope.$index,scope.row)">查看权限</el-button>
                    <el-button size="mini" type="danger"  @click="handleDropUser(scope.$index,scope.row)">删除</el-button>
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
                    <el-card class="box-card">
                        <el-form ref="userform" :model="userform" label-width="100px">
                            <el-form-item label="用户名：">
                                <el-input style="width: 300px; float: left;" v-model="userform.username"></el-input>
                            </el-form-item>
                            <el-form-item label="IP：">
                                <el-input style="width: 300px; float: left;" v-model="userform.userip"></el-input>
                            </el-form-item>
                            <el-form-item label="用户密码：">
                                <el-input style="width: 300px; float: left;" show-password v-model="userform.userpwd"></el-input>
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
                                </el-radio-group>
                            </el-form-item>
                            <el-form-item style="padding-bottom: 40px;">
                                <el-button type="primary" @click="saveUser">添加</el-button>
                                <el-button @click="dialogVisible = false">取消</el-button>
                            </el-form-item>
                        </el-form>
                    </el-card>
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
import store from '@/store/store.js';
import { getUserAccessDb,getMysqlMeta,execMysqlUser } from '@/api/api.js';
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
            if (this.searchcontent.length > 0) {
                this.results = this.results.filter(item => item[this.col[0]].includes(this.searchcontent))
            }
            else {
                this.getUserList(this.selectinst)
            }
        },
        handleCurrentChange(currentPage){
            this.currentPage = currentPage;
        },
        handleSizeChange(val){
            this.pagesize = val;
        },
        handleSelect(val){
            this.selectinst = val
            if (this.selectinst) {
                this.getUserList(this.selectinst)
            }  
        },
        getUserList(instid) {
            execMysqlUser({'instid':instid,'type':'showusers'}).then((response) => {
                    if (response) {
                        this.col = response.data.col
                        this.results = response.data.results
                        this.dblist = response.data.dblist
                    }
                }).catch((error) => {
                    console.log(error);
                })
        },
        handleDropUser($index,row){
            let inst = ''
            inst = this.instlist.filter((item) => {return item.instid === this.selectinst})
            let real_index = $index+(this.currentPage - 1) * this.pagesize
            let dropinfo = '确认删除<strong style="color:red;">'+inst[0].instname+'</strong>中用户' + '<strong style="color:red;">' +row['user@host']+ '</strong>'
            this.results.splice(real_index, 1)
            this.$confirm(dropinfo, '提示',{
                dangerouslyUseHTMLString: true,
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning',
            })
            .then(_=> {
                this.dropUser(row['user@host'])
                this.$message.success('删除成功!');
            })
            .catch(_=>{})
        },
        dropUser(user) {
            if (user) {
                execMysqlUser({'instid':this.selectinst,'user':user,'type':'dropuser'}).then((response) => {
                    if (response) {
                        this.$message.success('MySQL用户删除成功!');
                    }
                }).catch((error) => {
                    this.$message.error('MySQL用户删除失败!');
                    console.log(error);
                })
            }
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
            }
        },
        saveUser(){
            var request_data = {}
            request_data.type = 'adduser'
            request_data.instid = this.selectinst
            request_data.grantuser = this.userform
            execMysqlUser(request_data).then((response) => {
                if (response) {
                    this.dialogVisible = false
                    if (response.data.col[0] == 'ok') {
                        let adduser = this.userform.username + '@' + '\'' +this.userform.userip + '\''
                        this.results.push(adduser)
                        this.getUserList(this.selectinst)
                        this.$message.success('MySQL用户添加成功!');
                    }
                    else {
                        this.$message.error('MySQL用户添加失败!');
                    }
                }
            }).catch((error) => {
                this.$message.error('MySQL用户添加失败!');
                console.log(error);
            })
        },
        showUserPri(user){
            if (user) {
                execMysqlUser({'instid':this.selectinst,'user':user,'type':'showuserpri'}).then((response) => {
                    if (response) {
                        this.userpricol = response.data.col
                        this.userpriresults = response.data.results
                    }
                }).catch((error) => {
                    console.log(error);
                })
            }
        },
        getInstList() {
            getUserAccessDb({'dbtype':'mysqlinst','username':store.getters.username}).then((response) => {
                if (response.data.results.length > 0) {
                    for (let i =0; i< response.data.results.length;i++) {
                        this.instlist.push({'instid':response.data.results[i].instid,'instname':response.data.results[i].instname})
                    }
                }
                else {
                    this.$notify({title: '提示',message:'无可访问数据库，请先申请数据库权限！',type: 'warning'})
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
.mysqluser .el-table th{
    user-select: auto
}
.mysqluser-userpriresults{
    text-align: left;
}
/* .mysqluser .el-scrollbar__wrap{
    overflow-x: scroll;
} */
.el-select-dropdown .el-scrollbar .el-scrollbar__wrap{
    overflow: scroll;
}
.mysqluser .mysqluser-inst{
    float: left;
    width: 100%;
}
.mysqluser .mysqluser-inst .el-select,.mysqluser .mysqluser-inst .el-button--primary{
    float: left;
}
.mysqluser .el-table--mini, .el-table--small, .el-table__expand-icon{
    font-size: 13px;
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
