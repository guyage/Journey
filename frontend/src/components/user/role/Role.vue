<template>
    <div id="role" class="role">
        <el-col class="role-col" :span="4">
            <el-card class="role-card" shadow="hover">
                <div slot="header" class="clearfix">
                    <span>角色</span>
                    <el-button @click="isadd = true;newrole = ''" style="float: right; padding: 3px 0" type="text">添加</el-button>
                </div>
                <div class="rolelist" >
                    <el-tree 
                    :data="rolelist" 
                    :props="roleProps" 
                    @node-click="handleRoleTree">
                    <span class="custom-tree-node" slot-scope="{ node, data }">
                        <span>
                            <icon-svg style="vertical-align:middle;" class="menus-tree-icon" iconClass="icondian"></icon-svg>
                            {{ node.label }}
                        </span>
                        <span >
                            <el-button type="text" size="mini" @click="handleDelRole(node, data)">Delete</el-button>
                        </span>
                    </span>
                    </el-tree>
                    <div v-if="isadd" style="margin-top:5px;">
                        <el-input v-model="newrole" size="mini" placeholder="请输入角色名"></el-input>
                        <div style="margin-top:5px;">
                            <el-button @click="handleSaveRole" size="mini" type="primary" plain >save</el-button>
                            <el-button @click="isadd = false;" size="mini" type="danger" plain >cancel</el-button>
                        </div>
                    </div>
                </div>
            </el-card>
        </el-col>
        <el-col class="role-col" :span="8">
            <el-card class="role-card" shadow="hover">
                <div slot="header" class="clearfix">
                    <span>角色权限</span>
                    <el-button style="float: right; padding: 3px 0" @click="handleEditRole('role_perms')" type="text">保存</el-button>
                </div>
                <div class="text item" style="text-align:left;">
                    <el-tree
                    ref="menustree"
                    :data="menuslist" 
                    :props="menuProps"
                    show-checkbox
                    node-key="id"
                    :default-checked-keys="roleHasmenu"
                    :check-strictly='true'>
                    <span class="custom-tree-node" style="margin-left:5px;" slot-scope="{ node, data }">
                        <span>
                            <icon-svg class="menus-tree-icon" :iconClass="data.icon"></icon-svg>
                        </span>
                        <span>
                            {{ node.label }}
                        </span>            
                    </span>
                    </el-tree>
                </div>
            </el-card>
        </el-col>
        <el-col class="role-col" :span="12">
            <el-card class="role-card" shadow="hover">
                <div slot="header" class="clearfix">
                    <span>角色用户</span>
                    <el-button style="float: right; padding: 3px 0" @click="handleEditRole('role_users')" type="text">保存</el-button>
                </div>
                <div class="rolelist" style="text-align:left;">
                    <el-transfer
                    v-model="userselected"
                    :data="userlist"
                    :titles="['角色外', '角色内']">
                    </el-transfer>
                </div>
            </el-card>
        </el-col>
        
    </div>
</template>

<script>
import { getRole,getMenus,addRole,getUser,editRole } from '@/api/user.js';
export default {
    name: 'role',
    data () {
        return {
            roleProps: {
                label: 'name'
            },
            menuProps: {
                label: 'name'
            },
            rolelist: [],
            menuslist: [],
            roleHasmenu: [],
            selectrole: '',
            isadd: false,
            newrole: '',
            // 角色用户参数
            userlist: [],
            userselected: [],
        }
    },
    methods: {
        resetChecked() {
            this.$refs.menustree.setCheckedKeys([]);
        },
        handleDelRole(node, data) {
            let parent = node.parent;
            let children = parent.data.children || parent.data;
            let index = children.findIndex(d => d.id === data.id);
            children.splice(index, 1);
        },
        handleRoleTree(data) {
            if (this.selectrole == data.id) {
            }
            else {
                this.resetChecked()
                this.selectrole = data.id
                this.roleHasmenu = data.hasmenu
                this.userselected = data.hasuser
            }
        },
        handleSaveRole() {
            if (this.newrole) {
                addRole({'name':this.newrole}).then((response) =>{
                    this.isadd = false
                    this.$message.success('添加成功!');
                    this.getRoleData()
                }).catch((error) => {
                    console.log(error);
                    this.$message.error('添加失败!');
                });
            }
        },
        handleEditRole(type) {
            let req_data = {}
            req_data.id = this.selectrole
            if (type == 'role_perms') {
                let permsselected = []
                this.$refs.menustree.getCheckedNodes().forEach((selectperms,i) =>{
                    permsselected.push(selectperms.id)
                });
                req_data.type = 'role_perms'
                req_data.permsselected = permsselected
            }
            else if (type == 'role_users') {
                req_data.type = 'role_users'
                req_data.userselected = this.userselected
            }
            this.$confirm('确认修改!')
            .then(_=> {
                this.editRoleData(req_data)
            })
            .catch(_=>{})
        },
        editRoleData(req_data) {
            editRole(req_data).then((response) => {
                this.$message.success('保存成功!');
                this.getRoleData()
            }).catch((error) => {
                console.log(error);
                this.$message.error('保存失败!');
            });
        },
        getRoleData () {
            getRole().then((response) => {
                this.rolelist = response.data
            }).catch((error) => {
                console.log(error);
            });
        },
        getMenusData() {
            getMenus().then((response) => {
                this.menuslist = response.data
            }).catch((error) => {
                console.log(error);
            });
        },
        getUserData () {
            getUser().then((response) => {
                response.data.forEach((userinfo,i) => {
                    this.userlist.push({label: userinfo.last_name+userinfo.first_name, key: userinfo.id})
                })
            }).catch((error) => {
                console.log(error);
            });
        },
    },
    mounted () {
        this.getRoleData()
        this.getMenusData()
        this.getUserData()
    }
}
</script>

<style>
.role .el-card__header {
    padding: 5px 5px;
}
.role  .el-card__body {
    padding: 10px;
}
.role  .clearfix {
    text-align: left;
    padding-left: 10px;
}
.rolelist .el-tree-node__expand-icon.is-leaf{
    display: none;
}
.role .role-col{
    padding-right: 5px;
}
.role{
    font-size: 14px;
}
.role .el-tree-node.is-current.is-focusable {
    color:#409EFF;
}
.role .custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 14px;
    padding-right: 8px;
}
.role .el-checkbox{
    width: 100%;
}
/* 设置滚动条的样式 */
.role .el-transfer-panel__list::-webkit-scrollbar {
    width: 4px;
    height: 6px;
}
/* 滚动槽 */
.role .el-transfer-panel__list::-webkit-scrollbar-track{
    border-radius: 2px;
    /* background: hsla(220,4%,58%,.3); */
    /* background: rgba(0, 0, 0, 0.3); */
}
/* 滚动条滑块 */
.role .el-transfer-panel__list::-webkit-scrollbar-thumb{
    border-radius: 2px;
    background: hsla(220,4%,58%,.3);
    /* background: rgba(0, 0, 0, 0.3); */
}
</style>
