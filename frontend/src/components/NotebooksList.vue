<template>
  <div>
    <PageNavbar />
    <div class="notebook-list">
      <div v-for="notebook in notebookList" :key="notebook.id" class="notebook">
        <a :href="`/notebook/${notebook.id}`">
          {{ notebook.name }}
        </a>
      </div>
      <NewItemButton 
      class="new-notebook"
        :clickEvent="invokeNewNotebook"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import NewItemButton from './NewItemButton.vue';
import PageNavbar from './PageNavbar.vue';
import { getNotebooks, newNotebook } from './../helpers/apiHelper'
import { useRouter } from 'vue-router';
import { v4 as uuidv4 } from 'uuid';


export default defineComponent({
  components: {
    NewItemButton,
    PageNavbar,
  },

  props: {},

  emits: [],

  setup(props, { emit }) {
    // query the database for a list of notebooks, ids and names - visiblity
    const userId = 'amichai';

    const router = useRouter();

    const notebookList = ref([]);

    getNotebooks(userId).then(json => notebookList.value = json)

    const invokeNewNotebook = () => {
      const uuid = uuidv4().replaceAll('-', '');
      newNotebook('New Notebook!', uuid, userId)
      router.push(`/notebook/${uuid}`)
    }

    return {
      notebookList,
      invokeNewNotebook,
    };
  },
});
</script>

<style scoped>
.notebook {
  margin: 1.5em 0 1.5em 1.5em;
  background-color: lightgray;

  padding: 1em;
  border-radius: 0.3em;
  border-color: black;
  border-style: solid;
  border-width: 0.08em;
}

.notebook-list {
  display: flex;
  align-items: center;
  padding: 0 8% 0 8%;

}

.new-notebook {
  margin-left: 1em;
}
</style>
