<template>
  <div class="notebook-list">
    <div v-for="notebook in notebookList" :key="notebook.id" class="notebook">
      <a :href="`/notebook/${notebook.id}`">
        {{ notebook.name }}
      </a>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  components: {},

  props: {},

  emits: [],

  setup(props, { emit }) {
    // query the database for a list of notebooks, ids and names - visiblity
    const notebookList = [
      {
        name: 'Notebook 13',
        id: 123,
      },
      {
        name: 'Notebook 2',
        id: 124,
      },
      {
        name: 'Notebook 3',
        id: 125,
      },
      {
        name: 'Notebook 4',
        id: 128,
      },
    ];

    return {
      notebookList,
    };
  },
});
</script>

<style scoped>
.notebook {
  margin: 1em;
  padding: 1.5em;
  background-color: lightgray;
}

.notebook-list {
  display: flex;
}
</style>
