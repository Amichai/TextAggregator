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
import { defineComponent, ref } from 'vue';

export default defineComponent({
  components: {},

  props: {},

  emits: [],

  setup(props, { emit }) {
    // query the database for a list of notebooks, ids and names - visiblity
    const userId = 'amichai';

    const notebookList = ref([]);

    fetch(
      `https://8cem0l4r4j.execute-api.us-east-1.amazonaws.com/getNotebooks?userId=${userId}`
    )
      .then((response) => response.json())
      .then((asJson) => {
        console.log(asJson);
        notebookList.value = asJson;
      });

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
