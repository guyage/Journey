<template>
    <div id="dashboard" class="dashboard">
        <el-alert
        title="首次登陆无权限访问任何菜单，请联系管理员配置!"
        type="success"
        effect="dark">
        </el-alert>
    </div>
</template>

<script>
export default {
    name: 'dashboard',
    data () {
        return {
            msg: '仪表盘'
        }
    },
}
</script>

<style>

</style>
