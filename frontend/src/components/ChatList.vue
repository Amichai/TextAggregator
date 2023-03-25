<template>
<div>
  <div v-for="(snippet, index) in snippets" :key="index">
    <!-- {{snippets.map(i => i.title)}} -->
    <ChatItem 
      :snippet="snippet"
      :filterTags="[]"
      @clicked="() => clicked(snippet)"
    />
  </div>
</div>
</template>

<script lang="ts">
import { defineComponent, watch } from 'vue';
import ChatItem from '../components/ChatItem.vue';

export default defineComponent({
  components: {
    ChatItem,
  },

  props: {
    snippets: {
      type: Array,
      default: [],
    },
  },

  emits: ['clicked'],

  setup(props, { emit }) {
    const clicked = (snippet) => {
      emit('clicked', snippet)
    }
    
    return {
      clicked,
    };
  },
});
</script>

<style>
</style>
