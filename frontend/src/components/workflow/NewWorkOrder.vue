<template>
    <div class="newworkorder">
        <el-collapse v-model="activeNames">
            <el-collapse-item title="新建工单" name="1">
                <div class="user-operation" style="padding: 0.8em 0em 1em;">
                    <el-select size="small" style="float: left;padding-left: 1px;" v-model="ordertype" @change="handleChange($event)" placeholder="请选择工单类型">
                        <el-option v-for="(val,index) in ordertypelist" :key="index" :label="val" :value="val" ></el-option>
                    </el-select>
                </div>
                <br>
                <GitWorkOrder v-if="ordertype == 'git'"></GitWorkOrder>       
            </el-collapse-item>
        </el-collapse>
    </div>
</template>

<script>
import store from '@/store/store.js';
import GitWorkOrder from './GitWorkOrder.vue';
export default {
    name: 'newworkorder',
    components: {
        GitWorkOrder,
    },
    data () {
        return {
            activeNames: ['1'],
            ordertypelist: ['git','email'],
            ordertype: '',
            
        }
    },
    methods: {
        handleChange(val) {
            if (val == 'git') {
                this.ordertype = val
            }
        },
    }
}
</script>

<style>
.newworkorder .el-collapse-item__header.is-active,.newworkorder .el-collapse-item__header{
    font-size: 16px;
    font-weight: bold;
    padding-left: 0.5em;
    border-bottom: 1px solid #dcdfe6;
}

</style>
