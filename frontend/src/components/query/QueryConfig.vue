<template>
    <div class="queryconfig">
        <el-row>
          <div>
                <el-tabs v-model="activeName">
                    <el-tab-pane label="QueryLimit" name="first">
                        <QueryLimit></QueryLimit>
                    </el-tab-pane>
                    <el-tab-pane label="导出白名单" name="second">
                        <DumpWhiteList></DumpWhiteList>
                    </el-tab-pane>
                </el-tabs>
            </div>
        </el-row>
    </div>
</template>

<script>
import QueryLimit from './QueryLimit.vue';
import DumpWhiteList from './DumpWhiteList.vue';
export default {
    name: 'queryconfig',
    components: {
        QueryLimit,
        DumpWhiteList,
    },
    data() {
      return {
        activeName: 'first'
      };
    },
}
</script>

<style>

</style>