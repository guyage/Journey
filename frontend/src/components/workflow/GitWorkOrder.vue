<template>
    <div class="gitworkorder">
        <el-divider content-position="left">新建Git工单</el-divider>
        <div class="gitworkorder-form" style="float: left;width:40%;">
            <el-form v-loading="loading"  label-width="100px">
                <el-form-item label="主题：">
                    <el-input v-model="title"></el-input>
                </el-form-item>
                <el-form-item label="Git账户：">
                    <el-input :disabled="true" v-model="git_user"></el-input>
                </el-form-item>
                <el-form-item label="Git项目：" prop="git_permission">
                    <el-select v-model="git_project" filterable multiple placeholder="请选择Git项目">
                        <el-option 
                        v-for="item in gitprojectslist" 
                        :key="item.pid" 
                        :label="item.pname" 
                        :value="item.pname">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item style="float:left;" label="Git权限：" prop="git_permission">
                    <el-radio-group v-model="git_permission">
                        <el-radio label="Developer">读写</el-radio>
                        <el-radio label="Reporter">只读</el-radio>
                        <el-radio label="None">移除权限</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item style="clear:both;" label="描述：">
                    <el-input type="textarea" v-model="describe"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button :loading="issumit" style="float: left;" type="primary" @click="handleSubmit">提交工单</el-button>
                    <el-button style="float: left;" @click="handleCancel">取消</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<script>
import store from '@/store/store.js';
import { getGitLabInfo,addWorkOrder } from '@/api/api.js';
export default {
    name:'gitworkorder',
    data () {
        return {
            loading: false,
            issumit: false,
            gitprojectslist: [],
            // 请求参数
            title: '',
            creator: '',
            operation_group: 'git',
            order_type: 'git',
            describe: '',
            git_user: '',
            git_project: [],
            git_permission: '',
        }
    },
    methods: {
        handleCancel() {
            this.issumit = false
            this.$router.push({ path: '/myworkorder'})
        },
        handleSubmit() {
            this.issumit = true
            let gitworkorder_data = {}
            let git_data = {}
            if (this.title && this.git_user && this.git_project.length >0 && this.git_permission) {
                gitworkorder_data.title = this.title;
                gitworkorder_data.creator = store.getters.username;
                gitworkorder_data.operation_group = this.operation_group;
                gitworkorder_data.order_type = this.order_type;
                gitworkorder_data.describe = this.describe;
                git_data.git_user = this.git_user;
                git_data.git_project = this.git_project.join(',');
                git_data.git_permission = this.git_permission;
                gitworkorder_data.content = JSON.stringify(git_data)
                addWorkOrder(gitworkorder_data).then((response) => {
                    this.$message.success('申请成功!');
                    this.issumit = false
                    this.$router.push({ path: '/myworkorder'})
                }).catch((error) => {
                    console.log(error);
                    this.issumit = false
                    this.$message.error('申请失败!');
                })
            }
            else {
                this.$notify({title: '提示',message:'主题、Git账户、Git项目、Git权限必填项!',type: 'warning'})
                this.issumit = false
            }
            
        },
        getGitLabInfo(reqdata) {
            this.loading = true
            getGitLabInfo(reqdata).then((response) => {
                this.gitprojectslist = response.data.results
                this.loading = false;
            }).catch((error) => {
                console.log(error);
                this.loading = false;
            })
        },
        InitWorkOrderData() {
            this.getGitLabInfo({'reqtype':'projects'})
            this.git_user = store.getters.username
        }
    },
    mounted() {
        this.InitWorkOrderData()
    },
}
</script>

<style>
.gitworkorder .el-select{
    display: block;
}
</style>
