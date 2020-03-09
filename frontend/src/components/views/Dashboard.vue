<template>
    <div id="dashboard" class="dashboard">
        <el-alert
        title="首次登陆无权限访问任何菜单，请联系管理员配置!"
        type="success"
        effect="dark">
        </el-alert>
        <el-row>
            <!-- <OrderCharts></OrderCharts> -->
        </el-row>
    </div>
</template>

<script>
import OrderCharts from './charts/OrderCharts.vue';
export default {
    name: 'dashboard',
    components: {
        OrderCharts
    },
    data () {
        return {
            msg: '仪表盘'
        }
    },
}
</script>

<style>

</style>
