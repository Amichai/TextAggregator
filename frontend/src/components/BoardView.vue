<template>
<div class="root">
  <PageNavbar />
  <div 
    :class="['board-view',
    isMobile && 'full-width']"
  >
    <div class="labels" v-show="!isMobile">
      <LabelsView 
        :notebookId="notebookId"
        :snippets="snippets"
        :filterTags="filterTags"
        @tagClicked="tagClicked"
      />
    </div>
    <div 
      class="snippets">
      <button type="button" class="btn btn-default bi-pencil new-button"
        v-if="!isSnippetSelected"
        @click="newPost"
      > New</button>
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
        :filterTags="filterTags"
        :userId="userId"
        @summarySelected="summarySelected"
        @tagClicked="tagClicked"
        @trashClicked="trashClicked"
      />
    </div>
  </div>
</div>
</template>

<script lang="ts">
import { defineComponent, computed, watch, onMounted, onUnmounted, ref } from 'vue';
import PageNavbar from './PageNavbar.vue';
import LabelsView from './LabelsView.vue';
import NewSnippetArea from './NewSnippetArea.vue';
import SnippetsView from './SnippetsView.vue';
import { getNotebook, newSnippet, getSnippet, updateSnippet } from './../helpers/apiHelper';
import { removeElement, parseTags } from "./../helpers/helpers";
import { v4 as uuidv4 } from 'uuid';
import { useRouter } from 'vue-router';
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

    const selectedSnippetId = ref(null)

    const router = useRouter()

    let socket = new WebSocket("wss://nj87v6wtpf.execute-api.us-east-1.amazonaws.com/production");

    socket.onmessage = (event) => {
      const updatedSnippet = JSON.parse(event.data)
      console.log(event)

      const matchedSnippet = snippets.value.filter(snippet => snippet.snippetId == updatedSnippet.snippetId)[0]

      if(!matchedSnippet) {
        loadNotebook()
      } else {
        matchedSnippet.body = updatedSnippet.body
        matchedSnippet.title = updatedSnippet.title
        matchedSnippet.tags = updatedSnippet.tags ? parseTags(updatedSnippet.tags) : []
      }
    }

    onMounted(() => {
      window.addEventListener("resize", onResize);
    })

    onUnmounted(() => {
      window.removeEventListener("resize", onResize);
    })

    const snippetSubmitted = (snippetId) => {
      getSnippet(props.notebookId, snippetId, userId).then((updatedSnippet) => {
        snippetUpdated(updatedSnippet)
      })
    }

    const snippetUpdated = (updatedSnippet) => {
      updatedSnippet.tags = parseTags(updatedSnippet.tags)
      const snippetId = updatedSnippet.snippetId
      selectedSnippetId.value = snippetId

      const matchedSnippet = snippets.value.filter(i => i.snippetId === snippetId)[0]
      matchedSnippet.title = updatedSnippet.title
      matchedSnippet.body = updatedSnippet.body
      matchedSnippet.tags = updatedSnippet.tags
    }

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

            snippet.tags = parseTags(snippet.tags)
          }
        );

        const parts = window.location.href.split('#')
        if (parts.length > 1) {
          const snippetId = parts[1]
          console.log(snippetId)
          selectedSnippetId.value = snippetId
        }
      });
    };

    loadNotebook();

    const tagClicked = (tag) => {
      if(filterTags.value.includes(tag)) {
        filterTags.value = removeElement(filterTags.value, tag)
      } else {
        filterTags.value = filterTags.value.concat([tag])

      }
        const path = window.location.pathname;
        if(filterTags.value.length > 0) {
          router.push({path, query: { categories: filterTags.value.join(",") }})
        } else {
          router.push({path, query: {}})
        }
    }

    const summarySelected = (snippet) => {
      if(selectedSnippetId.value === snippet.snippetId) {
        selectedSnippetId.value = undefined;
        return
      }

      selectedSnippetId.value = snippet.snippetId
    }

    const backClicked = () => {
      selectedSnippetId.value = undefined
      loadNotebook();
    }

    const isSnippetSelected = computed(() => !!selectedSnippetId.value)

    const { user } = useAuth0();
    const userId = user.value.sub

    const newPost = () => {
      const uuid = uuidv4().replaceAll('-', '');
      // filterTags.value = []

      newSnippet(
        '',
        '',
        '',
        props.notebookId,
        userId,
        uuid
      ).then((text) => {
        loadNotebook();

        router.push(`/notebook/${props.notebookId}#${uuid}`)
      });
    }

    const MOBILE_WIDTH = 760

    const isMobile = ref(visualViewport.width <= MOBILE_WIDTH)
    const onResize = () => {
      isMobile.value = visualViewport.width <= MOBILE_WIDTH;
    }

    const trashClicked = () => {
      loadNotebook()
    }


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
  margin: 0 5% 0 5%;
  padding: 10px;
  width: 10em;
  background-color: var(--theme-color2);
  margin-bottom: 1em;
  /* color:black; */
  /* border:none; */
}

.snippets {
}
</style>
