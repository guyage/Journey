<template>
    <div class="error500">
        500
    </div>
</template>

<script>
export default {
    methods: {
        backPage () {
            this.$router.go(-1);
        },
        goHome () {
            this.$router.push({
                name: 'home'
            });
        }
    }
};
</script>