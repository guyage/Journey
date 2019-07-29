<template>
    <div id="permissionsgroupdialog" class="permissionsgroupdialog">
        <el-dialog
        :title="isEdit?'编辑权限组':'添加权限组'"
        :visible.sync="visible"
        @close="$emit('update:show', false)"
        :show="show"
        width="50%"
        :before-close="handleClose">
            <el-card class="box-card">
                <div style="padding-bottom: 4em;">
                    <div style="width: 15%;float: left;text-align: right;">
                        <label style="padding-right: 1em;">权限组：</label>
                    </div>
                    <div style="width: 85%;float: left;">
                        <el-input v-model="permissions_name" style="width: 495px;" size="small"></el-input>
                    </div>
                </div>
                <div style="padding-bottom: 4em;height: 15em;">
                    <div style="width: 15%;float: left;text-align: right;">
                        <label style="padding-right: 1em;">用户：</label>
                    </div>
                    <div style="width: 85%;float: left;">
                        <el-transfer
                        v-model="userselected"
                        :data="data"
                        :titles="['权限组外', '权限组内']">
                        </el-transfer>
                    </div>
                </div>
                <div style="padding-top: 4em;">
                    <div style="width: 15%;float: left;text-align: right;">
                        <label style="padding-right: 1em;">备注：</label>
                    </div>
                    <div style="width: 85%;float: left;">
                        <el-input v-model="comment" style="width: 495px;" size="small"></el-input>
                    </div>
                </div>
                <div style="padding-top: 4em;padding-left: 15%;">
                    <el-button v-if="!isEdit" @click="handleAddData" type="primary" size="small">添加</el-button>
                    <el-button v-if="isEdit" @click="handelEditData" type="primary" size="small">编辑</el-button>
                    <el-button @click="visible = false;" size="small">取消</el-button>
                </div>
            </el-card>
        </el-dialog>
    </div>
</template>

<script>
import { getUserList,addUserGroup,editUserGroup, getUserGroupList } from '@/api/api.js';
export default {
    name: 'permissionsgroupdialog',
    data () {
        //穿梭框生成数据
        const generateData = _ => {
            const data = [];
            getUserList().then((response) => {
                response.data.forEach((userinfo,i) => {
                    data.push({label: userinfo.last_name+userinfo.first_name, key: userinfo.id})
                })
            })
            return data;
        };
        return {
            //用户组相关变量
            permissions_name: '',
            comment: '',
            userlist: [],
            userselected: [],
            data: generateData(),
            permissionsgroup_edit_id: 0,
            //弹出框
            visible: this.show,
            isEdit: false,
        };
    },
    props: {
        show: {
            type: Boolean,
            default: false
        },
        usergroupdata: {
            type: Object,
        },
        saveData: {
            type: Function
        }
    },
    watch: {
        show () {
            this.visible = this.show;
        }
    },
    methods: {
        handelEditData() {
            let permissionsgourp_data = {};
            permissionsgourp_data.permissions_name = this.permissions_name
            permissionsgourp_data.comment = this.comment
            permissionsgourp_data.userselected = this.userselected
            permissionsgourp_data.id = this.permissionsgroup_edit_id
            this.saveData(this.isEdit,permissionsgourp_data)
        },
        handleAddData() {
            let permissionsgourp_data = {};
            permissionsgourp_data.permissions_name = this.permissions_name
            permissionsgourp_data.comment = this.comment
            permissionsgourp_data.userselected = this.userselected
            this.saveData(this.isEdit,permissionsgourp_data)
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
.permissionsgroupdialog{
    text-align: left;
}
</style>
