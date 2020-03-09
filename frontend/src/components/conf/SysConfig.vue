<template>
    <div class="sysconfig">
        <el-row>
          <div>
                <el-tabs v-model="activeName">
                    <el-tab-pane label="邮件配置" name="first">
                        <MailConfig></MailConfig>
                    </el-tab-pane>
                </el-tabs>
            </div>
        </el-row>
    </div>
</template>

<script>
import MailConfig from './MailConfig.vue';
export default {
    name: 'sysconfig',
    components: {
        MailConfig
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