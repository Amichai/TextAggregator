<template>
  <div class="snippet-item">
    <h4>
      {{ snippet.title }}
    </h4>
    <br />
    <div v-html="snippet.body" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  components: {},

  props: {
    snippet: {
      type: Object,
      required: true,
    },
  },

  emits: [],

  setup(props, { emit }) {
    return {};
  },
});
</script>

<style scoped>
.snippet-item {
  background-color: rgb(241, 241, 241);
  padding: 1em;
  border-radius: 1em;
  border-color: black;
  border-style: solid;
  border-width: 0.08em;
}


</style>
