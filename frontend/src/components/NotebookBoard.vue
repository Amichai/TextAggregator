<template>
  <div>
    <PageNavbar />
    <div class="notebook-board">
      <EditableTitle 
      v-model="notebookName"
      @blur="nameUpdated"
      />
      <NewItemButton
        :clickEvent="() => router.push(`/${notebookId}/Snippet`)"
      />
      <div class="snippet-filters">
        <VueTagsInput
          class="vue-tags-input"
          placeholder="Tag filters"
          v-model="tag"
          :tags="tagsWrapped"
          @tags-changed="(newTags) => (tagsWrapped = newTags)"
        />
      </div>
      <NewSnippetArea 
        :notebookId="notebookId"
        @snippetSubmitted="snippetSubmitted"
      />
      <ul id="snippet-list">
        <li
          v-for="snippet in snippetsFiltered"
          :key="snippet['userId-snippetId']"
          class="snippet-item"
        >
          <SnippetItem
            :snippet="snippet"
            :notebookId="notebookId"
            :filterTags="tags"
            @tagClicked="tagClicked"
          />
        </li>
      </ul>
      <div v-if="snippetsFiltered.length === 0 && snippets.length > 0">
        <br />
        <br />
        <i>No results match selected tag filters</i>
      </div>
      <div v-if="snippets.length === 0">
        <br />
        <br />
        <i>No Snippets to show</i>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, defineComponent, ref, watch } from 'vue';
import VueTagsInput from '@sipec/vue3-tags-input';
import { useRoute, useRouter } from 'vue-router';
import PageNavbar from './PageNavbar.vue';
import NewItemButton from './NewItemButton.vue';
import EditableTitle from './EditableTitle.vue';
import SnippetItem from './SnippetItem.vue';
import NewSnippetArea from './NewSnippetArea.vue';
import { getNotebook, updateNotebook } from './../helpers/apiHelper'

export default defineComponent({
  components: {
    VueTagsInput,
    PageNavbar,
    NewItemButton,
    EditableTitle,
    SnippetItem,
    NewSnippetArea,
  },
  props: {
    notebookId: {
      type: String,
      default: '',
    },
  },

  setup(props) {
    console.log(`notebook id: ${props.notebookId}`);
    const snippets = ref([]);
    const notebookName = ref(' ');

    const loadNotebook = () => {
      getNotebook(props.notebookId).then(json => {
        notebookName.value = json.notebook.name;
        snippets.value = json.snippets;
        snippets.value.map(
          (snippet) => (snippet.tags = snippet.tags.split(','))
        );

        filterItems();
      })
    }

    loadNotebook();

    const route = useRoute();
    const router = useRouter();

    const tag = ref('');
    const tags = ref([]);

    const query = { ...route.query };

    const path = window.location.pathname;

    query.tags?.split(',').forEach((tagText) => tags.value.push(tagText));
    const snippetsFiltered = ref(snippets.value);

    const filterItems = () => {
      if (tags.value.length === 0) {
        snippetsFiltered.value = snippets.value;
        router.push({ path, query: {} });
        return;
      }

      const filterTags = tags.value;
      snippetsFiltered.value = snippets.value.filter((item) =>
        item.tags
          .map((tag) => tag)
          .some((tagText) => filterTags.includes(tagText))
      );

      const queryValue = filterTags.join();

      router.push({ path, query: { tags: queryValue } });
    };

    const snippetSubmitted = () => {
      loadNotebook();
    }

    const tagClicked = (tagText) => {
      const selectedTags = tags.value.map((tag) => tag);

      if (selectedTags.includes(tagText)) {
        tags.value = tags.value.filter((tag) => {
          return tag !== tagText;
        });
        filterItems();
        return;
      }

      tags.value.push(tagText);
      filterItems();
    };

    const tagsWrapped = computed({
      get: () =>
        tags.value.map((tagText) => ({
          text: tagText,
          tiClasses: ['ti-valid'],
        })),
      set: (newTags) => (tags.value = newTags.map((tag) => tag.text)),
    });

    watch(tags, (newVal, oldVal) => {
      filterItems();
    });

    const nameUpdated = () => {
      updateNotebook(props.notebookId, notebookName.value)
    }

    return {
      snippets,
      tag,
      tags,
      tagsWrapped,
      snippetsFiltered,
      tagClicked,
      snippetSubmitted,

      router,

      notebookName,

      nameUpdated,
    };
  },
});
</script>

<style scoped>
#snippet-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.snippet-filters {
  display: flex;
  justify-content: space-between;
  margin-top: 1em;
}

.vue-tags-input {
  flex: 1;
}

.snippet-item {
  margin-top: 0.7em;
}

.notebook-board {
  padding: 0 18% 0 18%;
}

.notebook-menu {
  display: flex;
}
</style>
