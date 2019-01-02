<template>
      <svg class="svg-icon" aria-hidden="true">
          <use :xlink:href="iconName"></use>
      </svg>
</template>

<script>
export default {
  props: {
    iconClass: {
      type: String,
      required: true
    }
  },
  computed: {
    iconName() {
      return `#${this.iconClass}`
    }
  }
}
</script>

<style>
.svg-icon {
  width: 20px;
  height: 15px;
  vertical-align: -0.2em;
  fill: currentColor;
  overflow: hidden;
}
</style>