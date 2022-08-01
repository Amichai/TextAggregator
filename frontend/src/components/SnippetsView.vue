<template>
  <div>
    <table>
      <tr>
        <div v-for="(snippet, index) in snippetSummaries" v-bind:key="index"
          :class="[
            'snippet-summary',
          ]"
          
          @click="selectSummary(snippet.snippet)"
          >
          <!-- <i class="bi-grip-vertical" @click="deleteClicked"></i> -->
          <span v-html="snippet.summary">
          </span>
        </div>
      </tr>
    </table>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, watch, onMounted, onUnmounted, ref, PropType } from 'vue';
import { removeElement } from "../helpers/helpers";

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

  emits: ['summarySelected'],

  setup(props, { emit }) {
    const snippetSummaries = ref([])

    const loadSnippets = () => {
      if(props.filterTags.length == 0) {
        snippetSummaries.value = props.snippets
        .filter(i => !i.tags.includes('trash'))
        .map(i => {
          const title = i.title.trim()
          const body = i.body.trim()
          const bodySingleLine = body.replaceAll('\n', ' ')
          return {
            summary: `<b>${title}</b> ${bodySingleLine}`,
            snippet: i,
          }
        })
      } else {
        snippetSummaries.value = props.snippets.filter(
        (item) =>
          item.tags
            .map((tag) => tag)
            .some((tagText) => props.filterTags.includes(tagText))
        ).map(i => {
          const title = i.title.trim()
          const body = i.body.trim()
          const bodySingleLine = body.replaceAll('\n', ' ')
          return {
            summary: `<b>${title}</b> ${bodySingleLine}`,
            snippet: i,
          }
        })
      }
    }
    
    watch(() => props.snippets, (newVal, oldVal) => {
      loadSnippets()
    })
    
    watch(() => props.filterTags, (newVal, oldVal) => {
      loadSnippets()
    }, {deep: true})

    const selectSummary = (snippet) => {  
      emit('summarySelected', snippet)
    }

    return {
      selectSummary,
      snippetSummaries,
    };
  },
});
</script>

<style scoped>

table {
  table-layout:fixed;
  width:100%
}

.snippet-summary {
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
  cursor: pointer;

  height: 2em;


  padding-bottom: 4px;
  padding-top: 4px;
  box-shadow: inset 0 -1px 0 0 rgb(100 121 143 / 12%);
  color: #202124;
  margin-left: 6px;
  padding-left: 6px;
  margin-right: 6px;
}

.snippet-summary:hover {
  box-shadow: inset 1px 0 0 #dadce0, inset -1px 0 0 #dadce0, 0 1px 2px 0 rgb(60 64 67 / 30%), 0 1px 3px 1px rgb(60 64 67 / 15%);
}

.bi-grip-vertical {
  cursor: grab;
}
</style>
