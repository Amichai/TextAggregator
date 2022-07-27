<template>
  <div>
    <PageNavbar />
    <div class="notebook-board">
      <EditableTitle v-model="notebookName" @blur="nameUpdated">
        <h2>
          {{notebookName}}
        </h2>
      </EditableTitle>
      <div class="snippet-filters">
        <div class="tags-container" v-if="allTags != undefined">
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
            v-if="snippet.snippetId !== editingSnippet?.snippetId"
            :snippet="snippet"
            :notebookId="notebookId"
            :userId="userId"
            :filterTags="tags"
            @tagClicked="tagClicked"
            @editClicked="(s) => (editingSnippet = s)"
            @deleteClicked="loadNotebook"
          />
          <NewSnippetArea
            v-if="snippet.snippetId === editingSnippet?.snippetId"
            :notebookId="notebookId"
            @snippetSubmitted="snippetSubmitted"
            @cancelChanges="cancelChanges"
            :isEditingExistingSnippet="true"
            :snippet="snippet"
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
import { computed, defineComponent, ref, watch, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import PageNavbar from './PageNavbar.vue';
import NewItemButton from './NewItemButton.vue';
import EditableTitle from './EditableTitle.vue';
import SnippetItem from './SnippetItem.vue';
import NewSnippetArea from './NewSnippetArea.vue';
import { getNotebook, updateNotebook } from './../helpers/apiHelper';
import { useAuth0 } from '@auth0/auth0-vue';

export default defineComponent({
  components: {
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
    const allTags = ref([]);
    const editingSnippet = ref(null);
    
    const { user } = useAuth0();
    const userId = user.value.sub

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

        const allTagsWithDuplicates = snippets.value.reduce(
          (previous, current) => {
            return [...previous, ...current.tags];
          },
          []
        );

        allTags.value = [...new Set(allTagsWithDuplicates)].filter((t) => t);
        allTags.value.sort();

        console.log('All tags!!');
        console.log(allTags);

        filterItems();
      });
    };

    loadNotebook();

    const route = useRoute();
    const router = useRouter();

    const tag = ref('');
    const tags = ref([]);
    const filterTags = ref([]);

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

      filterTags.value = tags.value;
      snippetsFiltered.value = snippets.value.filter((item) =>
        item.tags
          .map((tag) => tag)
          .some((tagText) => filterTags.value.includes(tagText))
      );

      const queryValue = filterTags.value.join();

      router.push({ path, query: { tags: queryValue } });
    };

    const snippetSubmitted = () => {
      loadNotebook();

      editingSnippet.value = undefined;
    };

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
      updateNotebook(props.notebookId, notebookName.value);
    };

    const cancelChanges = () => {
      editingSnippet.value = undefined;
    };

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
      allTags,
      filterTags,
      editingSnippet,
      cancelChanges,
      loadNotebook,
      userId,
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
  padding-bottom: 4em;
}

.notebook-menu {
  display: flex;
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
</style>
