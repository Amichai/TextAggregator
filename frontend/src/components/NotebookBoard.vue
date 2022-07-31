<template>
  <div>
    <PageNavbar />

    <div class="notebook-board">
      <div class="column-left column">
        <div v-for="(summary, index) in snippetSummaries" v-bind:key="index"
          :class="[
          'snippet-summary', 
          selectedSnippetIndices.includes(index) && 'selected-snippet-summary'
          ]"
          v-html="summary"
          @click="selectSummary(index)"
          >
        </div>
      </div>
      <div class="column-center column">
        <div v-for="snippet in visibleSnippets" :key="snippet.snippetId">
          <NewSnippetArea 
            :notebookId="notebookId"
            :snippet="snippet"
            :filterTags="filterTags"
          />
        </div>
        <!-- filtered, editable snippets
        add new snippet form -->
      </div>
      <div class="column-right column">
        <!-- SEARCH BAR -->
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
import { removeElement } from "../helpers/helpers";

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

    const snippetSummaries = ref([])
    
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

        snippetSummaries.value = snippets.value.map(i => {
          const title = i.title.trim()
          const body = i.body.trim()
          return `<b>${title}</b> ${body}`
        })

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
        filterTags.value = []
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

    watch(() => tags, (newVal, oldVal) => {
      filterItems();
    });

    const nameUpdated = () => {
      updateNotebook(props.notebookId, notebookName.value);
    };

    const cancelChanges = () => {
      editingSnippet.value = undefined;
    };
    
    const cancelNewSnippet = () => {
    }

    const selectedSnippets = ref([])
    const selectedSnippetIndices = ref([])

    const selectSummary = (index) => {
      if(selectedSnippetIndices.value.includes(index)) {
        selectedSnippetIndices.value = removeElement(selectedSnippetIndices.value, index)
        selectedSnippets.value = removeElement(selectedSnippets.value, snippets.value[index])
      } else {
        selectedSnippetIndices.value.push(index)
        selectedSnippets.value.push(snippets.value[index])
      }

      console.log(selectedSnippets.value)
    }

    const visibleSnippets = computed(() => selectedSnippets.value.length === 0 ? snippets.value : selectedSnippets.value)


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
      cancelNewSnippet,
      snippetSummaries,
      selectSummary,
      selectedSnippetIndices,
      visibleSnippets,
    };
  },
});
</script>

<style scoped>
.notebook-board {
  display: flex;
}

.column {
  margin: 0.5em;
}


.column-left {
  flex:1;
  width: 30%;
}

.column-center {
  flex:2.5;
}

.column-right {
  flex:1;
}

.snippet-summary {
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
  cursor: pointer;
}

.snippet-summary:hover {
  background-color: lightgray;
}

.selected-snippet-summary {
  background-color: gray;
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
