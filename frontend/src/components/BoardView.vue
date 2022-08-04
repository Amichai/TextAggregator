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
        :snippet="selectedSnippet"
        @backClicked="backClicked"
        @snippetSubmitted="snippetSubmitted"
      />
      <SnippetsView 
        :isMobile="isMobile"
        v-show="!isSnippetSelected"
        :notebookId="notebookId"
        :snippets="snippets"
        :filterTags="filterTags"
        @summarySelected="summarySelected"
        @tagClicked="tagClicked"
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
import { removeElement } from "./../helpers/helpers";
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

    const selectedSnippet = ref(null)

    const router = useRouter()

    onMounted(() => {
      window.addEventListener("resize", onResize);
    })

    onUnmounted(() => {
      window.removeEventListener("resize", onResize);
    })

    const snippetSubmitted = (snippetId) => {
      getSnippet(props.notebookId, snippetId, userId).then((updatedSnippet) => {
        updatedSnippet.tags = updatedSnippet.tags.split(',').map(i => i.toLowerCase())
        selectedSnippet.value = updatedSnippet

        const matchedSnippet = snippets.value.filter(i => i.snippetId === snippetId)[0]
        matchedSnippet.title = updatedSnippet.title
        matchedSnippet.body = updatedSnippet.body
        matchedSnippet.tags = updatedSnippet.tags
      })
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

            snippet.tags = snippet.tags.split(',').map(i => i.toLowerCase());
          }
        );


        const parts = window.location.href.split('#')
        if (parts.length > 1) {
          const snippetId = parts[1]
          console.log(snippetId)
          const matched = snippets.value.find(snip => snip.snippetId == snippetId)
          selectedSnippet.value = matched
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
      if(selectedSnippet.value === snippet) {
        selectedSnippet.value = undefined;
        return
      }

      selectedSnippet.value = snippet
    }

    const backClicked = () => {
      selectedSnippet.value = undefined
      loadNotebook();
    }

    const isSnippetSelected = computed(() => !!selectedSnippet.value)

    const { user } = useAuth0();
    const userId = user.value.sub

    const newPost = () => {
      const uuid = uuidv4().replaceAll('-', '');

      newSnippet(
        '',
        '',
        '',
        props.notebookId,
        userId,
        uuid
      ).then((text) => {
        loadNotebook();

        const query = filterTags.value.length > 0 ? { categories: filterTags.value.join(",") } : {}
        router.push({path: `/notebook/${props.notebookId}#${uuid}`, query})
      });
    }

    const MOBILE_WIDTH = 760

    const isMobile = ref(visualViewport.width <= MOBILE_WIDTH)
    const onResize = () => {
      isMobile.value = visualViewport.width <= MOBILE_WIDTH;
    }


    return {
      snippets,
      tagClicked,
      filterTags,
      summarySelected,
      selectedSnippet,
      backClicked,
      isSnippetSelected,
      newPost,
      snippetSubmitted,
      isMobile,
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
