<template>
    <div class="dialog-container">
        <el-dialog
            :title="isUpdate?'修改用户信息':'添加用户'"
            :visible.sync="visible"
            @close="$emit('update:show', false)"
            :show="show"
            :before-close="handleClose">           
            <el-form :model="form" :rules="rules" ref="form"> 
                <el-form-item label="用户名 : " label-width="100px" prop="username">
                    <el-input style="width: 300px; float: left;" v-model="form.username" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item v-if="isUpdate" label="密码 : " label-width="100px" prop="password">
                    <el-input style="width: 300px; float: left;" v-model="form.password" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="姓 : " label-width="100px" prop="last_name">
                    <el-input style="width: 300px; float: left;" v-model="form.last_name" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="名 : " label-width="100px" prop="first_name">
                    <el-input style="width: 300px; float: left;" v-model="form.first_name" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="邮箱 : " label-width="100px" prop="email">
                    <el-input style="width: 300px; float: left;" v-model="form.email" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="手机 : " label-width="100px" prop="mobile">
                    <el-input style="width: 300px; float: left;" v-model="form.mobile" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="微信 : " label-width="100px" prop="webcat">
                    <el-input style="width: 300px; float: left;" v-model="form.webcat" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="备注 : " label-width="100px" prop="comment">
                    <el-input style="width: 300px; float: left;" v-model="form.comment" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="用户组 : " label-width="100px" prop="group">
                    <el-select style="width: 300px; float: left;" v-model="form.group" placeholder="请选择用户组">
                        <el-option label="开发组" value="dev"></el-option>
                        <el-option label="管理组" value="admin"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item>
                    <el-button v-if="!isUpdate" type="primary" @click="addDataFun">添加</el-button>
                    <el-button v-if="isUpdate" type="primary" @click="editDataFun">编辑</el-button>
                    <el-button @click="visible = false;resetForm('form')">取消</el-button>
                    <el-button @click="resetForm('form')">重置</el-button>
                </el-form-item>
            </el-form>
        </el-dialog>
    </div>
</template>

<script>
export default {
    data () {
        return {
            visible: this.show,
            isUpdate: false
        };
    },
    props: {
        show: {
            type: Boolean,
            default: false
        },

        apiurl: '',
        form: {
            type: Object,
        },
        rules: {
            type: Object,
        },
        addFun: {
            type: Function
        },
        editFun: {
            type: Function
        },
        editurl: '',
    },
    watch: {
        show () {
            this.visible = this.show;
        }
    },
    methods: {
        handleClose(done) {
            this.$confirm('确认关闭!')
                .then(_=> {
                    done();
                })
                .catch(_=>{})
        },
        resetForm(formName) {
            this.$refs[formName].resetFields();
        },
        // 添加数据按钮功能
        addDataFun() {  
            this.$refs['form'].validate((valid)=>{
                if(valid){
                    this.addFun(this.apiurl,this.form)
                    this.visible = false
                }
                else {
                    this.$message.error('数据不合法!');
                }
            })
                       
        },
        // 修改数据按钮功能
        editDataFun() {
            this.$refs['form'].validate((valid)=>{
                if(valid){
                    this.editFun(this.editurl,this.form)
                    this.visible = false
                }
                else {
                    this.$message.error('数据不合法!');
                }
            })    
        },
    },
};
</script>

<style>

</style>
