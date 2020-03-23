<template>
    <div id="dashboard" class="dashboard">
        <el-alert
        title="首次登陆无权限访问任何菜单，请联系管理员配置!"
        type="success"
        effect="dark">
        </el-alert>
        <el-row>
            <!-- <ShowCharts></ShowCharts> -->
        </el-row>
    </div>
</template>

<script>
import ShowCharts from './charts/ShowCharts.vue';
export default {
    name: 'dashboard',
    components: {
        ShowCharts
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
