<template>
    <div class="usergroup">
        <el-col class="usergroup-col" :span="6">
            <el-card class="usergroup-card" shadow="hover">
                <div slot="header" class="clearfix">
                    <span>用户组</span>
                    <el-button v-if="user_has_perms.indexOf('user:usergroup:add')>-1 || user_issuper" @click="isadd = true;newusergroup = ''" style="float: right; padding: 3px 0" type="text">添加</el-button>
                </div>
                <div class="usergrouplist" style="text-align:left;">
                    <el-tree 
                    :data="usergrouplist" 
                    :props="UserGroupProps" 
                    @node-click="handleUserGroupTree">
                    <span class="custom-tree-node" slot-scope="{ node, data }">
                        <span>
                            <icon-svg style="vertical-align:middle;" class="menus-tree-icon" iconClass="icondian"></icon-svg>
                            {{ node.label }}
                        </span>
                    </span>
                    </el-tree>
                    <div v-if="isadd" style="margin-top:5px;">
                        <el-input v-model="newusergroup" size="mini" placeholder="请输入用户组名"></el-input>
                        <div style="margin-top:5px;">
                            <el-button @click="handleSaveUserGroup" size="mini" type="primary" plain >save</el-button>
                            <el-button @click="isadd = false;" size="mini" type="danger" plain >cancel</el-button>
                        </div>
                    </div>
                    
                </div>
            </el-card>
        </el-col>
        <el-col class="usergroup-col" :span="12">
            <el-card class="usergroup-card" shadow="hover">
                <div slot="header" class="clearfix">
                    <span>用户组用户</span>
                    <el-button v-if="user_has_perms.indexOf('user:usergroup:edit')>-1 || user_issuper" style="float: right; padding: 3px 0" @click="handleEditUserGroup()" type="text">保存</el-button>
                </div>
                <div class="usergrouplist" style="text-align:left;">
                    <el-transfer
                    v-model="userselected"
                    :data="userlist"
                    :titles="['用户组外', '用户组内']">
                    </el-transfer>
                </div>
            </el-card>
        </el-col>
    </div>
</template>

<script>
import store from '@/store/store.js';
import { getUserGroup,getUser,addUserGroup,editUserGroup } from '@/api/user.js';
export default {
    name: 'usergroup',
    data () {
        return {
            // 用户权限参数
            user_issuper: false,
            user_has_perms:[],
            usergrouplist: [],
            UserGroupProps: {
                label: 'group'
            },
            selectusergroup: '',
            isadd: false,
            newusergroup: '',
            // 用户组用户参数
            userlist: [],
            userselected: [],
        }
    },
    methods: {
        handleEditUserGroup() {
            let req_data = {}
            req_data.id = this.selectusergroup
            req_data.userselected = this.userselected
            this.$confirm('确认修改!')
            .then(_=> {
                editUserGroup(req_data).then((response) => {
                    this.$message.success('保存成功!');
                    this.getUserGroupData()
                }).catch((error) => {
                    console.log(error);
                    this.$message.error('保存失败!');
                })
            })
            .catch(_=>{})
        },
        handleSaveUserGroup() {
            if (this.newusergroup) {
                addUserGroup({'group':this.newusergroup}).then((response) =>{
                    this.isadd = false
                    this.$message.success('添加成功!');
                    this.getUserGroupData()
                }).catch((error) => {
                    console.log(error);
                    this.$message.error('添加失败!');
                });
            }
            else {
                this.$notify({title: '提示',message:'用户组名不能为空!',type: 'warning'})
            }
        },
        handleUserGroupTree(data) {
            console.log(data);
            this.selectusergroup = data.id
            this.userselected = data.hasuser
        },
        getUserGroupData() {
            getUserGroup().then((response) => {
                this.usergrouplist = response.data
            }).catch((error) => {
                console.log(error);
            })
        },
        getUserData() {
            getUser().then((response) => {
                response.data.forEach((userinfo,i) => {
                    this.userlist.push({label: userinfo.last_name+userinfo.first_name, key: userinfo.id})
                })
            }).catch((error) => {
                console.log(error);
            });
        },
    },
    mounted() {
        this.getUserData()
        this.getUserGroupData()
        this.user_has_perms = store.getters.userperms 
        this.user_issuper = store.getters.userissuper
    },
}
</script>

<style>
.usergroup .el-card__header {
    padding: 5px 5px;
}
.usergroup  .el-card__body {
    padding: 10px;
}
.usergroup  .clearfix {
    text-align: left;
    padding-left: 10px;
}
.usergrouplist .el-tree-node__expand-icon.is-leaf{
    display: none;
}
.usergroup .usergroup-col{
    padding-right: 5px;
}
.usergroup{
    font-size: 14px;
}
.usergroup .el-tree-node.is-current.is-focusable {
    color:#409EFF;
}
.usergroup .custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 14px;
    padding-right: 8px;
}
</style>