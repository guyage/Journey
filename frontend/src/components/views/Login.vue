<template>
    <div id="login" class="login">
        <vueCanvasNest :config="backgroundcolor"></vueCanvasNest>
        <div class="login-title">
            <img src="../../assets/logo.png">
            <h3 class="logintitletext">Welcome to Journey DB平台</h3>
        </div>
        <div class="login-form">
            <el-tabs v-model="activeName" type="card">
                <el-tab-pane label="LDAP登录" name="1">
                    <el-form ref="ldaploginform" :model="ldaploginform" :rules="ldaploginrules" class="loginform">
                        <el-form-item lable="用户名" prop="username">
                            <el-input v-model="ldaploginform.username" placeholder="username">
                                <icon-svg iconClass="icon-user" slot="prepend"></icon-svg>
                            </el-input>
                        </el-form-item>
                        <el-form-item lable="密码" prop="password">
                            <el-input type="password" v-model="ldaploginform.password" placeholder="password" @keyup.enter.native="handleldapLogin">
                                <icon-svg iconClass="icon-lock" slot="prepend"></icon-svg>
                            </el-input>
                        </el-form-item>
                        <el-button :loading="loading" class="loginbutton" type="primary" @click="handleldapLogin">Login</el-button>
                    </el-form>
                </el-tab-pane>
                <el-tab-pane  label="普通登录" name="2">
                    <el-form ref="normalloginform" :model="normalloginform" :rules="normalloginrules" class="loginform">
                        <el-form-item lable="用户名" prop="username">
                            <el-input v-model="normalloginform.username" placeholder="username">
                                <icon-svg iconClass="icon-user" slot="prepend"></icon-svg>
                            </el-input>
                        </el-form-item>
                        <el-form-item lable="密码" prop="password">
                            <el-input type="password" v-model="normalloginform.password" placeholder="password" @keyup.enter.native="handlenormalLogin">
                                <icon-svg iconClass="icon-lock" slot="prepend"></icon-svg>
                            </el-input>
                        </el-form-item>
                        <el-button :loading="loading" class="loginbutton" type="primary" @click="handlenormalLogin">Login</el-button>
                    </el-form>
                </el-tab-pane>
            </el-tabs>
        </div>
    </div>
</template>

<script>
import store from '@/store/store.js'
import vueCanvasNest from 'vue-canvas-nest';
export default {
    components: {
        vueCanvasNest
    },
    data () {
        return {
            backgroundcolor: {
                color: '0,0,0',
                count: 199,
                opacity: 0.7,
            },
            activeName: '1',
            api: '/login',
            loading: false,
            normalloginform: {
                username: '',
                password: ''
            },
            normalloginrules: {
                username: [
                    { required: true, message: '请输入用户名', trigger: 'red' },
                ],
                password: [
                    { required: true, message: '请输入密码', trigger: 'red' },
                ]
            },
            ldaploginform: {
                username: '',
                password: ''
            },
            ldaploginrules: {
                username: [
                    { required: true, message: '请输入用户名', trigger: 'red' },
                ],
                password: [
                    { required: true, message: '请输入密码', trigger: 'red' },
                ]
            },
        }
    },
    methods: {
        handlenormalLogin() {
            this.$refs['normalloginform'].validate((valid)=>{
                if(valid){
                    this.loading = true
                    this.$store.dispatch('NormalLogin',this.normalloginform).then((response) => {
                        this.$message.success('登陆成功，跳转中...');
                        this.loading = false
                        this.$router.push({ path: '/index'})                     
                    }).catch((error) => {
                        this.loading = false
                        console.log(error);
                    })
                }
                else {
                    this.loading = false
                    this.$message.error('请输入合法用户名和密码!');
                }
            });
        },
        handleldapLogin() {
            this.$refs['ldaploginform'].validate((valid)=>{
                if(valid){
                    this.loading = true
                    this.$store.dispatch('LdapLoginIn',this.ldaploginform).then(() => {
                        this.$message.success('登陆成功，跳转中...');
                        this.loading = false
                            this.$router.replace({ path: '/index'})
                    }).catch((error)=>{
                        // this.$message.error('登陆失败，请输入正确用户名及密码，如有疑问，请联系管理员!');
                        console.log(error);
                        this.loading = false
                    })
                }
                else {
                    this.loading = false
                    this.$message.error('请输入合法用户名和密码!');
                }
            });
        },
    }
}
</script>

<style>
.login {
    height: 100%;
    width: 100%;
    position: fixed;
}
.login .login-title {
    margin: 0 auto;
    text-align: center;
    margin-top: 7%;
}
.login .login-form {
    margin: 120px auto;
    max-width: 100%;
    padding: 10px 35px 15px;
    right: 0;
    width: 400px;
    margin-top: 0.1em;
}
.login .loginbutton {
    width: 400px;
}
.login .el-button--primary {
    background-color:#1ab394;
    border-color: #1ab394
}
.login .el-button--primary:focus, .el-button--primary:hover{
    background-color:#56c0a5;
    border-color: #56c0a5;
}
.login .logintitletext {
    font-size: 20px;
    font-weight: 100;
    margin-top: 10px;
    color: inherit
}
.login .el-tabs--card>.el-tabs__header .el-tabs__nav{
    width: 100%;
}
.login .el-tabs--card>.el-tabs__header .el-tabs__item:first-child{
    width: 50%;
}
.login .el-tabs--card>.el-tabs__header .el-tabs__item:last-child{
    width: 50%;
}
</style>