<template>
  <TextEditor :body="snippet?.body ?? ''" />
  <!-- <div>{{snippet.body}}</div> -->
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import TextEditor from '../components/TextEditor.vue';

export default defineComponent({
  components: {
    TextEditor
  },

  props: {
    snippet: {
      type: Object,
      default: null,
    }
  },

  emits: [],

  setup(props, { emit }) {
    return {
    };
  },
});
</script>

<style>
</style>
