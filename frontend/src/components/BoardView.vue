<template>
  <div class="root">
    <PageNavbar />
    <div :class="['board-view', isMobile && 'full-width']">
      <div class="labels" v-show="!isMobile">
        <LabelsView
          :notebookId="notebookId"
          :snippets="snippets"
          :filterTags="filterTags"
          @tagClicked="tagClicked"
        />
        <!-- <button
            type="button"
            :class="[
              'btn', 'btn-default', 'bi-trash', 'trash-button',
              isMobile && 'mobile-button'
            ]"
            @click="trashLabel"
          >
            Trash
          </button> -->
      </div>
      <div class="snippets">
        <div class="snippets-header" v-if="!isSnippetSelected">
          <button
            type="button"
            :class="[
              'btn', 'btn-default', 'bi-pencil', 'new-button',
              isMobile && 'mobile-button'
            ]"
            @click="newPost"
          >
            New
          </button>
          <div class="updated-created-buttons">
            <span
              @click="sortCreatedClicked"
              :class="[
                'noselect',
                'sort-icon',
                selectedSortOption[0] === 'C' && 'icon-selected',
              ]"
            >
              <i v-if="selectedSortOption === 'CU'" class="bi bi-sort-up"></i>
              <i v-else class="bi bi-sort-down"></i>
              Created
            </span>
            <span
              @click="sortUpdatedClicked"
              :class="[
                'noselect',
                'sort-icon',
                selectedSortOption[0] === 'U' && 'icon-selected',
              ]"
            >
              <i v-if="selectedSortOption === 'UU'" class="bi bi-sort-up"></i>
              <i v-else class="bi bi-sort-down"></i>
              Updated
            </span>
          </div>
        </div>
        <NewSnippetArea
          v-if="isSnippetSelected"
          :notebookId="notebookId"
          :snippetId="selectedSnippetId"
          :userId="userId"
          @backClicked="backClicked"
          @snippetSubmitted="snippetSubmitted"
          @snippetUpdated="snippetUpdated"
        />
        <SnippetsView
          :isMobile="isMobile"
          v-show="!isSnippetSelected"
          :notebookId="notebookId"
          :snippets="snippets"
          :userId="userId"
          :filterTags="filterTags"
          @summarySelected="summarySelected"
          @tagClicked="tagClicked"
          @trashClicked="trashClicked"
        />
        <div 
          class="footer"
          v-if="!isSnippetSelected"
        >
          <button
              type="button"
              :class="[
                'btn', 'btn-default', 'more-button', 'bi-arrow-down-short',
                isMobile && 'mobile-button'
              ]"
              @click="loadMore"
            >
              Load More
            </button>

            <div class="snippets-loaded">
            {{snippetCount}} snippets
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import {
  defineComponent,
  computed,
  watch,
  onMounted,
  onUnmounted,
  ref,
} from 'vue';
import PageNavbar from './PageNavbar.vue';
import LabelsView from './LabelsView.vue';
import NewSnippetArea from './NewSnippetArea.vue';
import SnippetsView from './SnippetsView.vue';
import {
  getNotebook,
  newSnippet,
  getSnippet,
  updateSnippet,
} from './../helpers/apiHelper';
import { removeElement, parseTags } from './../helpers/helpers';
import { v4 as uuidv4 } from 'uuid';
import { useRouter } from 'vue-router';
import dayjs from 'dayjs';
import { useAuth0 } from '@auth0/auth0-vue';

export default defineComponent({
  components: {
    PageNavbar,
    LabelsView,
    SnippetsView,
    NewSnippetArea,
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
    const snippetCount = ref(0)

    const sortOptions = ref(['CU', 'CD', 'UU', 'UD']);

    const selectedSortOption = ref(sortOptions.value[0]);

    const selectedSnippetId = ref(null);

    const router = useRouter();

    let socket = new WebSocket(
      'wss://nj87v6wtpf.execute-api.us-east-1.amazonaws.com/production'
    );

    socket.onmessage = (event) => {
      const updatedSnippet = JSON.parse(event.data);
      console.log(event);

      const matchedSnippet = snippets.value.filter(
        (snippet) => snippet.snippetId == updatedSnippet.snippetId
      )[0];

      if (!matchedSnippet) {
        loadNotebook();
      } else {
        matchedSnippet.body = updatedSnippet.body;
        matchedSnippet.title = updatedSnippet.title;
        matchedSnippet.isStarred = updatedSnippet.isStarred ?? false
        matchedSnippet.tags = updatedSnippet.tags
          ? parseTags(updatedSnippet.tags)
          : [];
      }
    };

    onMounted(() => {
      window.addEventListener('resize', onResize);
    });

    onUnmounted(() => {
      window.removeEventListener('resize', onResize);
    });

    const snippetSubmitted = (snippetId) => {
      getSnippet(props.notebookId, snippetId, userId).then((updatedSnippet) => {
        snippetUpdated(updatedSnippet);
      });
    };

    const snippetUpdated = (updatedSnippet) => {
      updatedSnippet.tags = parseTags(updatedSnippet.tags);
      const snippetId = updatedSnippet.snippetId;
      selectedSnippetId.value = snippetId;

      const matchedSnippet = snippets.value.filter(
        (i) => i.snippetId === snippetId
      )[0];
      matchedSnippet.title = updatedSnippet.title;
      matchedSnippet.body = updatedSnippet.body;
      matchedSnippet.tags = updatedSnippet.tags;
      matchedSnippet.isStarred = updatedSnippet.isStarred ?? false
    };

    const loadNotebook = (startIdx, takeCount, tags) => {
      if(!startIdx || !takeCount) {
        resetPagination()
      }

      getNotebook(props.notebookId, startIdx, takeCount, 'created-desc', tags).then((json) => {
        notebookName.value = json.notebook.name;
        snippets.value = [...snippets.value, ...json.snippets];

        snippets.value.forEach((snippet) => {
          if (!snippet.tags) {
            snippet.tags = [];
            return;
          }

          if (typeof snippet.tags == 'string') {
            snippet.tags = parseTags(snippet.tags);
          }
        });

        const parts = window.location.href.split('#');
        if (parts.length > 1) {
          const snippetId = parts[1];
          console.log(snippetId);
          selectedSnippetId.value = snippetId;
        }

        snippetCount.value = snippets.value.length
        sortSnippets();
      });
    };

    let startIdx = 0
    let takeCount = 30
    const resetPagination = () => {
      startIdx = 0
      takeCount = 30
      snippets.value = []
    }

    loadNotebook(startIdx, takeCount);

    const loadMore = () => {
      startIdx += takeCount
      loadNotebook(startIdx, takeCount);
    }

    const tagClicked = (tag) => {
      if (filterTags.value.includes(tag)) {
        filterTags.value = removeElement(filterTags.value, tag);
      } else {
        filterTags.value = filterTags.value.concat([tag]);
      }
      const path = window.location.pathname;
      if (filterTags.value.length > 0) {
        router.push({
          path,
          query: { categories: filterTags.value.join(',') },
        });
      } else {
        router.push({ path, query: {} });
      }

      resetPagination();
      loadNotebook(startIdx, takeCount, filterTags.value.join())
    };

    const summarySelected = (snippet) => {
      if (selectedSnippetId.value === snippet.snippetId) {
        selectedSnippetId.value = undefined;
        return;
      }

      selectedSnippetId.value = snippet.snippetId;
    };

    const backClicked = () => {
      selectedSnippetId.value = undefined;
      loadNotebook();
    };

    const isSnippetSelected = computed(() => !!selectedSnippetId.value);

    const { user } = useAuth0();
    const userId = user.value.sub;

    const newPost = () => {
      const uuid = uuidv4().replaceAll('-', '');
      // filterTags.value = []

      newSnippet('', '', '', props.notebookId, userId, uuid).then((text) => {
        loadNotebook();

        router.push(`/notebook/${props.notebookId}#${uuid}`);
      });
    };

    const MOBILE_WIDTH = 760;

    const isMobile = ref(visualViewport.width <= MOBILE_WIDTH);
    const onResize = () => {
      isMobile.value = visualViewport.width <= MOBILE_WIDTH;
    };

    const trashClicked = () => {
      loadNotebook();
    };

    const sortSnippets = () => {
      const sortOption = selectedSortOption.value;
      if (sortOption === 'CD') {
        snippets.value.sort((a, b) => {
          return +dayjs.utc(a.created) - +dayjs.utc(b.created);
        });
      }
      if (sortOption === 'CU') {
        snippets.value.sort((a, b) => {
          return +dayjs.utc(b.created) - +dayjs.utc(a.created);
        });
      }
      if (sortOption === 'UU') {
        snippets.value.sort((a, b) => {
          return +dayjs.utc(b.updated) - +dayjs.utc(a.updated);
        });
      }
      if (sortOption === 'UD') {
        snippets.value.sort((a, b) => {
          return +dayjs.utc(a.updated) - +dayjs.utc(b.updated);
        });
      }
    };

    const sortCreatedClicked = () => {
      if (selectedSortOption.value === 'CU') {
        selectedSortOption.value = 'CD';
      } else {
        selectedSortOption.value = 'CU';
      }

      sortSnippets();
    };

    const sortUpdatedClicked = () => {
      if (selectedSortOption.value === 'UU') {
        selectedSortOption.value = 'UD';
      } else {
        selectedSortOption.value = 'UU';
      }

      sortSnippets();
    };

    return {
      snippets,
      tagClicked,
      filterTags,
      summarySelected,
      selectedSnippetId,
      backClicked,
      isSnippetSelected,
      newPost,
      snippetSubmitted,
      isMobile,
      userId,
      trashClicked,
      snippetUpdated,
      sortOptions,
      selectedSortOption,
      loadMore,

      sortCreatedClicked,
      sortUpdatedClicked,

      snippetCount,
    };
  },
});
</script>

<style scoped>
.root {
  background-color: var(--background-color);
}

.board-view {
  display: grid;
  grid-template-columns: 10vw 88vw;
}

.full-width {
  display: grid;
  grid-template-columns: 100vw;
}

.labels {
  display: flex;
  flex-direction: column;
}

.new-button {
  margin: 0 5px 0 5px;
  padding: 8px;
  width: 10em;
  background-color: var(--theme-color2);
  margin-bottom: 1em;
}

.more-button {
  margin: 0 5px 0 5px;
  padding: 3px;
  width: 7em;
  background-color: var(--theme-color3);
  color: white;
  margin-bottom: 1em;
}

.footer {
  display: flex;
  margin: 1 0px;
}

.snippets-header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.snippets-loaded {
  font-size: small;
  margin-left: 20px;
  font-style: italic;
}

.snippets {
}

.sort-icon {
  padding: 9px 15px 9px 15px;
  margin: 0 8px 0 8px;
  border-radius: 1.1em;
  color: gray;
  border-color: lightgray;
  border-style: solid;
}

.trash-button {
  width: 6em;
  background-color: var(--theme-color1);
  margin-left: 5px;
}

.icon-selected {
  color: black;
}

.sort-icon:hover {
  background-color: lightgray;
  cursor: pointer;
}

.mobile-button {
  width: 7em;
}

.updated-created-buttons {
  display: flex;
  align-items: baseline;
}

.noselect {
  -webkit-touch-callout: none; /* iOS Safari */
  -webkit-user-select: none; /* Safari */
  -khtml-user-select: none; /* Konqueror HTML */
  -moz-user-select: none; /* Old versions of Firefox */
  -ms-user-select: none; /* Internet Explorer/Edge */
  user-select: none; /* Non-prefixed version, currently
                                  supported by Chrome, Edge, Opera and Firefox */
}
</style>
