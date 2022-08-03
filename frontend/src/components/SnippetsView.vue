<template>
  <div class="snippets-view">
    <table style="width: 100%;">
      <tr v-for="(snippet, index) in snippetSummaries"              
        v-bind:key="index"
        class="snippet-summary"
        @click="selectSummary(snippet.snippet)"
      >
      <td class="grip"><i class="bi-grip-vertical"></i></td>
      <td
      class="time-ago"
      v-show="!isMobile"
      >{{snippet.timeAgo}}</td>
      <td class="snippet-column"><span v-html="snippet.summary"/></td>
      <td class="tags-column" v-if="snippet.tags.length > 0">
          <p v-for="(tag, index) in snippet.tags" v-bind:key="index"
            @click="(ev) => tagClicked(ev, tag)"
            :class="['tag-p', filterTags.includes(tag) && 'filter-tag']"
          >
            {{ tag }}
          </p>
        </td>
      </tr>
    </table>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, watch, onMounted, onUnmounted, ref, PropType } from 'vue';
import { removeElement } from "../helpers/helpers";
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import utc from 'dayjs/plugin/utc'

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
    isMobile: {
      type: Boolean,
      default: false,
    },
  },

  emits: ['summarySelected', 'tagClicked'],

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
            summary: `<b>${title}</b> <span style="font-size:14px">${bodySingleLine}</span>`,
            snippet: i,
            tags: i.tags,
            timeAgo: dayjs.utc(i.updated).fromNow(),
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
            // summary: `<b>${title}</b> ${bodySingleLine}`,
            summary: `<b>${title}</b> <span style="font-size:14px">${bodySingleLine}</span>`,
            snippet: i,
            tags: i.tags,
            timeAgo: dayjs.utc(i.updated).fromNow(),
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

    const tagClicked = (ev, tag) => {
      ev.stopPropagation();
      emit('tagClicked', tag)
    }

    return {
      selectSummary,
      snippetSummaries,
      tagClicked,
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

  display: flex;


  padding-bottom: 4px;
  padding-top: 4px;
  box-shadow: inset 0 -1px 0 0 rgb(100 121 143 / 12%);
  color: #202124;
  margin-left: 6px;
  padding-left: 6px;
  margin-right: 6px;
}

.snippet-column {
  white-space: nowrap;
  text-overflow:ellipsis;
  overflow: hidden;
  width:100%
}

.snippet-summary:hover {
  box-shadow: inset 1px 0 0 #dadce0, inset -1px 0 0 #dadce0, 0 1px 2px 0 rgb(60 64 67 / 30%), 0 1px 3px 1px rgb(60 64 67 / 15%);
}

.bi-grip-vertical {
  cursor: grab;
}

.tag-p {
  background-color: var(--tag-color);
  color: white;
  margin: 5px;
  padding: 2.5px 10px 2.5px 10px;
  border-radius: 3px;
  font-size: 0.7em;
  height: fit-content;
  cursor: pointer;
}

.tags-column {
  display: flex;
  align-items: center

}

.time-ago {
  min-width: 7em; 
  font-size: small; 
  text-align: left;
  overflow: hidden;
  display: flex;
  align-items: center;
  font-style: italic;
  
}

.filter-tag {
  background: rgb(208, 86, 72);
}

.grip {
  display: flex;
  align-items: center;

}

.snippets-view {
  background: white;
}
</style>
