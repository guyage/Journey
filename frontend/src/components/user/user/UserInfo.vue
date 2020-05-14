<template>
    <div class="userinfo">
        <el-row>
            <el-col :span="8" style="padding-right:5px;"> 
                <el-card class="box-card" shadow="hover" >
                    <div slot="header" class="clearfix">
                        <span>关于我</span>
                    </div>
                    <div>
                        <img style="width:150px;height:150px;" src="http://127.0.0.1:8888/uploads/avatar/1.png"></el-button>
                    </div>
                </el-card>
            </el-col>
            <el-col :span="16">
                <el-card class="box-card" shadow="hover">
                    <div>
                        <el-tabs v-model="activeName">
                            <el-tab-pane label="个人信息" name="first">
                                <el-form style="text-align:left;" ref="infoform" :model="infoform" size="mini" label-position="top">
                                    <el-form-item label="手机号：">
                                        <el-input style="width:300px;" size="mini" v-model="infoform.mobile"></el-input>
                                    </el-form-item>
                                    <el-form-item label="微信：">
                                        <el-input style="width:300px;"  size="mini" v-model="infoform.webcat"></el-input>
                                    </el-form-item>
                                    <el-form-item>
                                        <el-button size="mini" type="primary" @click="handleSumit('info')">Update</el-button>
                                    </el-form-item>
                                </el-form>
                            </el-tab-pane>
                            <el-tab-pane label="密码管理" name="second">密码管理</el-tab-pane>
                        </el-tabs>
                    </div>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>
import {getUserInfo,editUserInfo} from '@/api/user.js';
export default {
    name: 'userinfo',
    data() {
        var validatePass = (rule, value, callback) => {
            if (value === '') {
                callback(new Error('请再次输入密码'));
            } else if (value !== this.pwdform.new_pwd) {
                callback(new Error('两次输入密码不一致!'));
            } else {
                callback();
            }
        };
        return {
            activeName: 'first',
            infoform: {
                mobile: '',
                webcat: '',
            },
            pwdform: {
                old_pwd: '',
                new_pwd: '',
                check_pass: '',
            },
            rules: {
                // pass: [
                //     { validator: validatePass, trigger: 'blur' }
                // ],
                check_pass: [
                    { validator: validatePass, trigger: 'blur' }
                ],
                // age: [
                //     { validator: checkAge, trigger: 'blur' }
                // ]
            }
            
        }
    },
    methods: {
        handleSumit(type) {
            let req_data = {}
            if (type == 'info') {
                req_data.edit_type = 'info'
                req_data.edit_data = this.infoform
                this.editData(req_data)
            }
        },
        getData() {
            getUserInfo().then((response) => {
                this.infoform = response.data.results
            }).catch((error) => {
                console.log(error);
            })
        },
        editData(data) {
            editUserInfo(data).then((response) => {
                this.$message.success('修改成功!');
                this.getData()
            }).catch((error) => {
                console.log(error);
                this.$message.error('修改失败!');
            })
        }
    },
    mounted() {
        this.getData()
    },
}
</script>

<style>
.userinfo .clearfix{
    text-align: left;
}
</style>