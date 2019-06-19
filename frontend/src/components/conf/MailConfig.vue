<template>
    <div id="mailconfig" class="mailconfig">
        <el-collapse v-model="activeNames">
            <el-collapse-item title="Eamil配置" name="1">
                <el-form :model="mailform" :rules="mailrules" ref="mailform" label-width="150px" size="small">
                    <el-form-item label="邮件服务器：" prop="mail_host">
                        <el-input style="width: 300px; float: left;" v-model="mailform.mail_host"></el-input>
                    </el-form-item>
                    <el-form-item label="邮件服务器端口：" prop="mail_port">
                        <el-input style="width: 300px; float: left;" v-model="mailform.mail_port"></el-input>
                    </el-form-item>
                    <el-form-item label="邮件用户：" prop="mail_user">
                        <el-input style="width: 300px; float: left;" v-model="mailform.mail_user"></el-input>
                    </el-form-item>
                    <el-form-item label="邮件用户密码：" prop="mail_pass">
                        <el-input style="width: 300px; float: left;" type="password" v-model="mailform.mail_pass"></el-input>
                    </el-form-item>
                    <el-form-item label="备注：" prop="comment">
                        <el-input style="width: 300px; float: left;" v-model="mailform.comment"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button style="float: left;" size="small" type="primary" @click="handleSaveData('mailform')">保存</el-button>                        
                        <el-button style="float: left;" size="small" @click="handlresetForm('mailform')">重置</el-button>
                    </el-form-item>
                </el-form>
            </el-collapse-item>
            <el-collapse-item title="邮件测试" name="2">
                <el-form :model="testmailform" :rules="testmailrules" ref="testmailform" label-width="150px" size="small">
                    <el-form-item label="测试邮箱：" prop="mail_host">
                        <el-input style="width: 300px; float: left;" v-model="testmailform.testmail"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button style="float: left;" size="small" type="primary" @click="handleTestMail('testmailform')">发送测试邮件</el-button>
                    </el-form-item>
                </el-form>
            </el-collapse-item>
        </el-collapse>
    </div>
</template>

<script>
import { getMailConfig, setMailConfig, execMailTest } from '@/api/api.js';
export default {
    name: 'mailconfig',
    data () {
        return {
            testmailform: {
                testmail: ''
            },
            testmailrules: {
                testmail: [
                    { required: true, message: '测试接收邮箱', trigger: 'blur' },
                ]
            },
            isid: false,
            activeNames: ['1','2'],
            mailform: {
                mail_host: '',
                mail_port: '',
                mail_user: '',
                mail_pass: '',
                comment: ''
            },
            mailrules: {
                mail_host: [
                    { required: true, message: '邮件服务器', trigger: 'blur' },
                ],
                mail_port: [
                    { required: true, message: '邮件服务器端口', trigger: 'blur' },
                ],
                mail_user: [
                    { required: true, message: '邮件用户', trigger: 'blur' },
                ],
                mail_pass: [
                    { required: true, message: '邮件用户密码', trigger: 'blur' },
                ],
            }
        }
    },
    methods: {
        handlresetForm(formName) {
            this.$refs[formName].resetFields();
        },
        handleSaveData(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    if (this.isid) {
                        this.mailform.id = 1
                        setMailConfig(this.mailform).then((response) => {
                            this.$message.success('保存成功!');
                        }).catch((error) => {
                            this.$message.success('保存失败，请联系管理员!');
                            console.log(error);
                        })
                    }
                    else {
                        setMailConfig(this.mailform).then((response) => {
                            this.$message.success('保存成功!');
                            this.isid = true
                        }).catch((error) => {
                            this.$message.success('保存失败，请联系管理员!');
                            console.log(error);
                        })
                    } 
                }
                else {
                    console.log('error save!!');
                    return false;
                }
            })
        },
        handleTestMail(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    execMailTest(this.testmailform).then((response) => {
                        var testinfo = ''
                        if (response.data.status == 'sucess') {
                            testinfo = '邮件测试 '+'<strong style="color:green">'+response.data.status+' !<strong>'
                        }
                        else {
                            testinfo = '邮件测试 '+'<strong style="color:red">'+response.data.status+' !<strong>'
                        }
                        this.$alert(testinfo,{dangerouslyUseHTMLString: true})
                    }).catch((error) => {
                        console.log(error);
                    })
                }
                else {
                    console.log('error test!!');
                    return false;
                }

            })
        },
        getMailConfig() {
            getMailConfig().then((response) => {
                if (response.data.length > 0) {
                    this.mailform = response.data[0]
                    this.isid = true
                }
                else {
                   this.isid = false 
                }
            })
        }
    },
    mounted() {
        this.getMailConfig()
    },
}
</script>

<style>
.mailconfig .el-collapse-item__header.is-active,.mailconfig .el-collapse-item__header{
    font-size: 16px;
    font-weight: bold;
    padding-left: 0.5em;
}
</style>
