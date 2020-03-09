<template>
    <div class="approvalgroup">
        <el-col class="approvalgroup-col" :span="6">
            <el-card class="approvalgroup-card" shadow="hover">
                <div slot="header" class="clearfix">
                    <span>工单审批组</span>
                    <el-button @click="isadd = true;newrole = ''" style="float: right; padding: 3px 0" type="text">添加</el-button>
                </div>
                <div class="approvalgrouplist" >
                    <el-tree 
                    :data="ftree_data_list" 
                    :props="ftreeProps" 
                    @node-click="handleFTreeNode">
                    <span slot-scope="{ node, data }">
                        <span>
                            <icon-svg class="menus-tree-icon" iconClass="icondian"></icon-svg>
                        </span>
                        <span>
                            {{ node.label }}
                        </span>
                        <!-- <span style="float:right;" >
                            <el-button type="text" size="mini" @click="handleDelRole(node, data)">Delete</el-button>
                        </span> -->
                    </span>
                    </el-tree>
                    <div v-if="isadd" style="margin-top:5px;">
                        <el-input v-model="newdata" size="mini" placeholder="请输入工单审批组名称"></el-input>
                        <div style="margin-top:5px;">
                            <el-button @click="handleSaveFTree" size="mini" type="primary" plain >save</el-button>
                            <el-button @click="isadd = false;" size="mini" type="danger" plain >cancel</el-button>
                        </div>
                    </div>
                </div>
            </el-card>
        </el-col>
        <el-col class="approvalgroup-col" :span="12">
            <el-card class="approvalgroup-card" shadow="hover">
                <div slot="header" class="clearfix">
                    <span>工单审批组用户</span>
                    <el-button style="float: right; padding: 3px 0" @click="handleEditSTree" type="text">保存</el-button>
                </div>
                <div class="approvalgrouplist" style="text-align:left;">
                    <el-transfer
                    v-model="userselected"
                    :data="userlist"
                    :titles="['审批组外', '审批组内']">
                    </el-transfer>
                </div>
            </el-card>
        </el-col>
    </div>
</template>

<script>
import {getUser} from '@/api/user.js';
import { getApprovalGroup,addApprovalGroup,editApprovalGroup } from '@/api/workorder.js';
export default {
    name: 'approvalgroup',
    data () {
        return {
            newdata: '',
            ftree_data_list: [],
            ftreeProps: {
                label: 'approver_group_name'
            },
            selectapprovalgroup: '',
            isadd: false,
            userselected: [],
            userlist: [],
        }
    },
    methods: {
        handleFTreeNode(data) {
            this.selectapprovalgroup = data.id
            this.userselected = data.hasuser
        },
        handleSaveFTree() {
            if (this.newdata) {
                addApprovalGroup({'approver_group_name':this.newdata}).then((response) => {
                    this.isadd = false
                    this.$message.success('添加成功!');
                    this.getApprovalGroupData()
                }).catch((error) => {
                    console.log(error);
                    this.$message.error('添加失败!');
                })
            }
        },
        handleEditSTree() {
            let req_data = {}
            if (this.selectapprovalgroup) {
                req_data.id = this.selectapprovalgroup
                req_data.userselected = this.userselected
                this.$confirm('确认修改!')
                .then(_=> {
                    this.editApprovalGroupdata(req_data)
                })
                .catch(_=>{})
            }
            else {
                this.$notify({title: '提示',message:'请选择工单审批组!',type: 'warning'})
            }
        },
        editApprovalGroupdata(req_data) {
            editApprovalGroup(req_data).then((response) => {
                this.$message.success('保存成功!');
                this.getApprovalGroupData()
            }).catch((error) => {
                console.log(error);
                this.$message.error('保存失败!');
            });
        },
        getApprovalGroupData() {
            getApprovalGroup().then((response) => {
                this.ftree_data_list = response.data
            })
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
        this.getApprovalGroupData()
        this.getUserData()
    }
}
</script>

<style>
.approvalgroup .el-card__header {
    padding: 5px 5px;
}
.approvalgroup  .el-card__body {
    padding: 10px;
}
.approvalgroup  .clearfix {
    text-align: left;
    padding-left: 10px;
}
.approvalgroup .el-tree-node__expand-icon.is-leaf{
    display: none;
}
.approvalgroup .approvalgroup-col{
    padding-right: 5px;
}
.approvalgroup{
    font-size: 14px;
}
.approvalgroup .el-tree-node.is-current.is-focusable {
    color:#409EFF;
}
</style>