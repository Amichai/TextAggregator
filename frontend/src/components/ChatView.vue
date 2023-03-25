<template>
<div class="chatView">
  <!-- Header -->
  <div class="chats">
    <ChatList :snippets="snippets" @clicked="clicked" />
  </div>
  <!-- <div class="openChat">
    <NewSnippetArea
      v-if="isSnippetSelected"
      :notebookId="notebookId"
      :snippetId="selectedSnippetId"
      :userId="userId"
      @backClicked="() => {}"
      @snippetSubmitted="() => {}"
      @snippetUpdated="() => {}"
    /> -->
  <!-- </div> -->
    <!-- <TextEditor :body="" /> -->
    <SnippetEditor :snippet="selectedSnippet" />
</div>
</template>

<script lang="ts">
import { 
  defineComponent,
  ref,
  onMounted,
  onUnmounted,
  computed,
} from 'vue';
import {
  getNotebook,
  newSnippet,
  getSnippet,
  updateSnippet,
} from './../helpers/apiHelper';
import { removeElement, parseTags } from './../helpers/helpers';
import dayjs from 'dayjs';
import ChatList from '../components/ChatList.vue';
import NewSnippetArea from '../components/NewSnippetArea.vue';
import TextEditor from '../components/TextEditor.vue';
import SnippetEditor from '../components/SnippetEditor.vue';
import { useAuth0 } from '@auth0/auth0-vue';

export default defineComponent({
  components: {
    ChatList,
    NewSnippetArea,
    TextEditor,
    SnippetEditor,
  },

  props: {
    notebookId: {
      type: String,
      default: '',
    },
  },

  emits: [],

  setup(props, { emit }) {
    const snippets = ref([]);
    const notebookName = ref(' ');
    const selectedSnippetId = ref(null);
    const snippetCount = ref(0)

    const sortOptions = ref(['CU', 'CD', 'UU', 'UD']);

    const selectedSortOption = ref(sortOptions.value[0]);

    const MOBILE_WIDTH = 760;

    const isSnippetSelected = computed(() => !!selectedSnippetId.value);

    const isMobile = ref(visualViewport.width <= MOBILE_WIDTH);
    const onResize = () => {
      isMobile.value = visualViewport.width <= MOBILE_WIDTH;
    };

    onMounted(() => {
      loadNotebook(0, 5, [])
      window.addEventListener('resize', onResize);
    });

    onUnmounted(() => {
      window.removeEventListener('resize', onResize);
    });

    let startIdx = 0
    let takeCount = 30
    const resetPagination = () => {
      startIdx = 0
      takeCount = 30
      snippets.value = []
    }

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
      if (sortOption === 'SU') {
        snippets.value.sort((a, b) => {
          return b.body.length - a.body.length;
        });
      }
      if (sortOption === 'SD') {
        snippets.value.sort((a, b) => {
          return a.body.length - b.body.length;
        });
      }
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

        console.log(snippets.value)
      });
    };

    const selectedSnippet = computed(() => {
      return snippets.value.find((snippet) => snippet.snippetId === selectedSnippetId.value)
    })

    const clicked = (snippet) => {
      selectedSnippetId.value = snippet.snippetId
      // debugger
    }

    const { user } = useAuth0();
    const userId = user.value.sub;

    return {
      snippets,
      clicked,
      selectedSnippetId,
      isSnippetSelected,
      userId,
      selectedSnippet,
    };
  },
});
</script>

<style>
.chatView {
  display: grid;
  grid-template-columns: 32vw 58vw;
  gap: 10px;
  background-color: lightgreen;
}

.chats {
  /* grid-column: 1; */
  background-color: red;
  /* max-width: 50%; */

}

.openChat {
  /* grid-column: 2; */
  background-color: yellow;
}


</style>
