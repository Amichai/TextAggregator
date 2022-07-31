<template>
  <div>
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
</template>

<script lang="ts">
import { defineComponent, computed, watch, onMounted, onUnmounted, ref, PropType } from 'vue';
import BoardViewMobile from './BoardViewMobile.vue'
import BoardViewDesktop from './BoardViewDesktop.vue'
import PageNavbar from './PageNavbar.vue';

export default defineComponent({
  components: {
    BoardViewMobile,
    BoardViewDesktop,
    PageNavbar,
  },

  props: {
    snippets: {
      type: Array as PropType<any>,
      default: [],
    },
  },

  emits: [],

  setup(props, { emit }) {
    const snippetSummaries = ref([])
    snippetSummaries.value = props.snippets.map(i => {
      const title = i.title.trim()
      const body = i.body.trim()
      return `<b>${title}</b> ${body}`
    })

    const selectedSnippets = ref([])
    const selectedSnippetIndices = ref([])

    const removeElement = (arr, element) => {
      for(var i = 0; i < arr.length; i++) {
        if(arr[i] === element) {
          arr.splice(i, 1)
          break
        }
      }

      return arr
    }

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
      selectedSnippets,
    };
  },
});
</script>

<style>
</style>
