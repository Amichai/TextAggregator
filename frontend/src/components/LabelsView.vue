<template>
<div>
  <div class="tags-container">
    <p
      v-for="tag in allTags"
      :key="tag"
      @click="tagClicked(tag)"
      :class="['tag-p', filterTags.includes(tag) && 'filter-tag']"
    >
      {{ tag }}
    </p>
  </div>
</div>
</template>

<script lang="ts">
import { defineComponent, computed, watch, onMounted, onUnmounted, ref, PropType } from 'vue';

export default defineComponent({
  components: {
  },

  props: {
    notebookId: {
      type: String,
      default: '',
    },
    snippets: {
      type: Array as PropType<any>,
      required: true,
    },
    filterTags: {
      type: Array as PropType<any>,
      required: true,
    },
  },

  emits: ['tagClicked'],

  setup(props, { emit }) {
    console.log(`notebook id: ${props.notebookId}`);
    const allTags = ref([]);

    watch(() => props.snippets, (newVal, oldVal) => {
      const allTagsWithDuplicates = props.snippets
      .filter(snippet => !snippet.tags.includes('trash'))
      .reduce(
        (previous, current) => {
          return [...previous, ...current.tags];
        },
        ['trash']
      );

      allTags.value = [...new Set(allTagsWithDuplicates.map(i => i.toLowerCase()))].filter((t) => t);
      allTags.value = allTags.value.sort();

      console.log(allTags.value)
    })
    

    const tagClicked = (tagText) => {
      emit('tagClicked', tagText)
    }

    return {
      allTags,
      tagClicked,
    };
  },
});
</script>

<style scoped>
.tag-p {
  background: #5c6bc0;
  color: white;
  margin: 5px;
  padding: 2.5px 10px 2.5px 10px;
  border-radius: 3px;
  font-size: 0.7em;
  height: fit-content;
  cursor: pointer;
}

.filter-tag {
  background: rgb(208, 86, 72);
}
</style>
