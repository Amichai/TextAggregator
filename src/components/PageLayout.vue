<template>
  <div>
    navbar
  </div>
  <div class="root">
    header:
    <slot name="header"></slot>
    body:
    <slot name="body"></slot>
    test3
  </div>
</template>

<script lang="ts">
  import { defineComponent } from "vue"

  export default defineComponent({
    components: {
    },

    props: {
    },

    emits: [],

    setup(props, { emit }) {
      return {
      }
    },
  })
</script>

<style>
.root {
  padding: 0 18% 0 18%;
}
</style>