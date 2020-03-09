<template>
    <div id="userdialog" class="userdialog">
        <el-dialog
            :title="isEdit?'编辑用户':'添加用户'"
            :visible.sync="visible"
            @close="$emit('update:show', false)"
            :show="show"
            :before-close="handleClose"
            width="50%">
            <el-card class="box-card">          
                <el-form :model="form" :rules="rules" ref="form"> 
                    <el-form-item label="用户名 : " label-width="100px" prop="username">
                        <el-input style="width: 300px; float: left;" v-model="form.username" auto-complete="off"></el-input>
                    </el-form-item>
                    <el-form-item v-if="isEdit" label="密码 : " label-width="100px" prop="password">
                        <el-input style="width: 300px; float: left;" show-password v-model="form.password" auto-complete="off"></el-input>
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
                    <el-form-item label-width="100px">
                        <el-button v-if="!isEdit" type="primary" @click="handleAddData">添加</el-button>
                        <el-button v-if="isEdit" type="primary" @click="handelEditData">编辑</el-button>
                        <el-button @click="visible = false;resetForm('form')">取消</el-button>
                        <el-button @click="resetForm('form')">重置</el-button>
                    </el-form-item>
                </el-form>
            </el-card>
        </el-dialog>
    </div>
</template>

<script>
import { getUserGroup } from '@/api/user.js';
export default {
    name: 'userdialog',
    data () {
        return {
            visible: this.show,
            isEdit: false,
            user_edit_id: 0,
            usergrouplist: []
        };
    },
    props: {
        show: {
            type: Boolean,
            default: false
        },
        form: {
            type: Object,
        },
        rules: {
            type: Object,
        },
        saveData: {
            type: Function
        },
    },
    watch: {
        show () {
            this.visible = this.show;
        }
    },
    methods: {
        resetForm(formName) {
            this.$refs[formName].resetFields();
        },
        handelEditData() {
            this.$refs['form'].validate((valid)=>{
                if(valid){
                    console.log(this.form);
                    this.saveData(this.isEdit,this.form)
                }
                else {
                    this.$message.error('数据不合法!');
                }
            })
        },
        handleAddData() {
            this.$refs['form'].validate((valid)=>{
                if(valid){
                    console.log(this.form);
                    this.saveData(this.isEdit,this.form)
                }
                else {
                    this.$message.error('数据不合法!');
                }
            })
        },
        handleClose(done) {
            this.$confirm('确认关闭!')
            .then(_=> {
                done();
            })
            .catch(_=>{})
        },
    },
}
</script>

<style>
.userdialog{
    text-align: left;
}
</style>
