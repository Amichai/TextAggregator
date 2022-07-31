<template>
  <div>
    <table>
      <tr>
        <div v-for="(summary, index) in snippetSummaries" v-bind:key="index"
          :class="[
            'snippet-summary',
            selectedSnippetIndices.includes(index) && 'selected-snippet-summary'
          ]"
          
          @click="selectSummary(index)"
          >
          <i class="bi-grip-vertical" @click="deleteClicked"></i>
          <span v-html="summary">
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

  emits: [],

  setup(props, { emit }) {
    const snippetSummaries = ref([])
    
    watch(() => props.snippets, (newVal, oldVal) => {
      snippetSummaries.value = props.snippets.map(i => {
          const title = i.title.trim()
          const body = i.body.trim()
          const bodySingleLine = body.replaceAll('\n', ' ')
          return `<b>${title}</b> ${bodySingleLine}`
        })
    })

    const selectedSnippets = ref([])
    const selectedSnippetIndices = ref([])

    const selectSummary = (index) => {
      if(selectedSnippetIndices.value.includes(index)) {
        selectedSnippetIndices.value = removeElement(selectedSnippetIndices.value, index)
        selectedSnippets.value = removeElement(selectedSnippets.value, props.snippets[index])
      } else {
        selectedSnippetIndices.value.push(index)
        selectedSnippets.value.push(props.snippets[index])
      }

      console.log(selectedSnippets.value)
    }

    return {
      selectSummary,
      snippetSummaries,
      selectedSnippetIndices,
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

.selected-snippet-summary {
  background-color: gray;
}


.bi-grip-vertical {
  cursor: grab;
}
</style>
