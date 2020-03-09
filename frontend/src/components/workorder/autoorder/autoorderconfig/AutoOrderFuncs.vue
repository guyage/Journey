<template>
    <div class="autoorderfuncs" >
        <el-row >
            <el-input autosize v-model="ordertypefuncs" type="textarea"></el-input>
            <el-button @click="getJson">JSON</el-button>
        </el-row>
    </div>
</template>

<script>
export default {
    name: 'autoorderfuncs',
    data() {
        return {
            remotefuncs: ''
        }
    },
    props: {
        ordertypeid: {
            type: Number,
        },
        ordertypefuncs: {
            type: String,
        },
    },
    methods: {
        getJson() {
            console.log(JSON.stringify(this.ordertypefuncs));
        }
    }
}
</script>

<style>

</style>