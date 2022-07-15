<template>
  <div class="snippet-item">
    <h4 v-if="snippet.title">
      {{ snippet.title }}
    </h4>
    <div v-html="snippet.body" />

    <div class="footer">
      <div class="tags-container" v-if="tags != undefined">
        <p
          v-for="tag in tags"
          :key="tag"
          :class="['tag-p', filterTags.includes(tag) && 'filter-tag']"
          @click="tagClicked(tag)"
        >
          {{ tag }}
        </p>
      </div>
    </div>
    <div class="edit-delete-snippet">
      <a class="link-primary"> Delete </a>
      <a
        class="link-primary"
        :href="`/${notebookId}/Snippet/${snippet.snippetId}`"
        >Edit</a
      >
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  components: {},

  props: {
    snippet: {
      type: Object,
      required: true,
    },
    filterTags: {
      type: Array,
      required: true,
    },
    notebookId: {
      type: String,
      required: true,
    },
  },

  emits: ['tagClicked'],

  setup(props, { emit }) {
    const parsedTags = props.snippet.tags.filter((t) => t !== '');
    const tags = ref(parsedTags);

    console.log(props.snippet);

    const tagClicked = (tagText) => {
      emit('tagClicked', tagText);
    };

    return {
      tags,
      tagClicked,
    };
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

.footer {
  display: flex;
  align-items: center;
}
.tags-container {
  display: flex;
  flex-wrap: wrap;
}
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

.edit-delete-snippet {
  display: flex;
  flex-direction: row-reverse;
}

a {
  margin-right: 1em;
}
</style>
