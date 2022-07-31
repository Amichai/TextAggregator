<template>
<div>
  <PageNavbar />
  <div v-if="!isMobile">
    <BoardViewDesktop />
  </div>
  <div v-else>
    <BoardViewMobile />
  </div>
</div>
</template>

<script lang="ts">
import { defineComponent, computed, watch, onMounted, onUnmounted, ref } from 'vue';
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
    notebookId: {
      type: String,
      default: '',
    },
  },

  emits: [],

  setup(props, { emit }) {
    const MOBILE_WIDTH = 760

    const isMobile = ref(visualViewport.width <= MOBILE_WIDTH)
    const onResize = () => {
      isMobile.value = visualViewport.width <= MOBILE_WIDTH;
    }

    onMounted(() => {
      window.addEventListener("resize", onResize);
    })

    onUnmounted(() => {
      window.removeEventListener("resize", onResize);
    })

    return {
      isMobile,
    };
  },
});
</script>

<style>
</style>
