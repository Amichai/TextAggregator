<template>
<div>
  <PageNavbar />
  <div class="board-view">
    <div class="labels">
      <LabelsView 
        :notebookId="notebookId"
        :snippets="snippets"
        :filterTags="filterTags"
        @tagClicked="tagClicked"
      />
    </div>
    <div class="snippets">
      <SnippetsView 
        :notebookId="notebookId"
        :snippets="snippets"
        :filterTags="filterTags"
      />
    </div>
  </div>
</div>
</template>

<script lang="ts">
import { defineComponent, computed, watch, onMounted, onUnmounted, ref } from 'vue';
import PageNavbar from './PageNavbar.vue';
import LabelsView from './LabelsView.vue';
import SnippetsView from './SnippetsView.vue';
import { getNotebook } from './../helpers/apiHelper';
import { removeElement } from "./../helpers/helpers";

export default defineComponent({
  components: {
    PageNavbar,
    LabelsView,
    SnippetsView,
  },

  props: {
    notebookId: {
      type: String,
      default: '',
    },
  },

  emits: [],

  setup(props, { emit }) {
    console.log(`notebook id: ${props.notebookId}`);
    const notebookName = ref(' ');
    const snippets = ref([]);

    const filterTags = ref([]);

    const loadNotebook = () => {
      getNotebook(props.notebookId).then((json) => {
        notebookName.value = json.notebook.name;
        snippets.value = json.snippets;
        snippets.value.forEach(
          (snippet) => {
            if(!snippet.tags) {
              snippet.tags = [];
              return 
            }

            snippet.tags = snippet.tags.split(',');
          }
        );
      });
    };

    loadNotebook();

    const tagClicked = (tag) => {
      if(filterTags.value.includes(tag)) {
        removeElement(filterTags.value, tag)
        return
      }

      filterTags.value.push(tag);

    }

    return {
      snippets,
      tagClicked,
      filterTags,
    };
  },
});
</script>

<style scoped>
.board-view {
  display: grid;
  grid-template-columns: 20vw 80vw;
}

.labels {
}

.snippets {
}
</style>
