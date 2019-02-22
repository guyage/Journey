<template>
    <div id="tabs">
        <el-tabs v-model="ediTabsValue" type="card" editable @edit="handleTabsEdit">
            <el-tab-pane 
            v-for="(item,index) in edittabs"
            :key="index"
            :label="item.title"
            :name="item.name">
            <el-input type="textarea">
            </el-input>
            </el-tab-pane>           
        </el-tabs>
    </div>
</template>

<script>
export default {
    data () {
        return {
           ediTabsValue: '1',
           edittabs: [
               { title: 'SQL标签1', name: '1'},
           ],
           tabIndex: 1
        }
    },
    methods: {
        handleTabsEdit(targetName, action) {
            if(action === 'add') {
                let newTabName = ++this.tabIndex + ''
                let newTitle = 'SQL标签' + newTabName
                this.edittabs.push({title:newTitle,name:newTabName})
                
            }
        }
    }
}
</script>

<style>

</style>
