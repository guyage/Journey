<template>
    <div class="newworkorder">
        <el-row>
            <div>
                <el-tabs v-model="activeName">
                    <el-tab-pane label="SQL工单" name="second">
                        <NewSqlOrder></NewSqlOrder>
                    </el-tab-pane>
                    <el-tab-pane label="自助工单" name="third">
                        <NewAutoOrder></NewAutoOrder>
                    </el-tab-pane>
                </el-tabs>
            </div>
        </el-row>
    </div>
</template>

<script>
import NewSqlOrder from './sqlorder/NewSqlOrder.vue';
import NewAutoOrder from './autoorder/NewAutoOrder.vue';
export default {
    name: 'newworkorder',
    components: {
        NewSqlOrder,
        NewAutoOrder,
    },
    data() {
      return {
        activeName: 'second'
      };
    },
    methods: {

    }
}
</script>

<style>

</style>