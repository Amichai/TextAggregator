<template>
  <div>
    <PageNavbar />
    <div class="notebook-board">
      <EditableTitle v-model="notebookName" />
      <NewSnippetButton
        :clickEvent="() => router.push(`/${notebookId}/NewSnippet`)"
      />
      <div class="snippet-filters">
        <VueTagsInput
          class="vue-tags-input"
          placeholder="Tag filters"
          v-model="tag"
          :tags="tags"
          @tags-changed="(newTags) => (tags = newTags)"
        />
      </div>

      <ul id="snippet-list">
        <li
          v-for="snippet in snippetsFiltered"
          :key="snippet['userId-snippetId']"
          class="snippet-item"
        >
          <SnippetItem :snippet="snippet" />
        </li>
      </ul>
      <div v-if="snippetsFiltered.length === 0 && snippets.length > 0">
        <br />
        <br />
        <i>No results match selected tag filters</i>
      </div>
      <div v-if="snippets.length === 0">
        <br />
        <br />
        <i>No Snippets to show</i>
      </div>
    </div>
  </div>
</template>

<script>
// This view is similar to keep
// A rich editor at the top to create a note
// a list of snippets + tags
// search, tag filtering
// collaborators
// When clicked, display the content in a scrollable modal?
import { defineComponent, ref } from 'vue';
import VueTagsInput from '@sipec/vue3-tags-input';
import { useRoute, useRouter } from 'vue-router';
import PageNavbar from './PageNavbar.vue';
import NewSnippetButton from './NewSnippetButton.vue';
import EditableTitle from './EditableTitle.vue';
import SnippetItem from './SnippetItem.vue';

export default defineComponent({
  components: {
    VueTagsInput,
    PageNavbar,
    NewSnippetButton,
    EditableTitle,
    SnippetItem,
  },
  props: {
    notebookId: {
      type: String,
      default: '',
    },
  },

  setup(props) {
    console.log(`notebook id4: ${props.notebookId}`);
    console.log(`notebook id4: ${props.notebookId}`);
    const snippets = ref([]);

    fetch(
      `https://8cem0l4r4j.execute-api.us-east-1.amazonaws.com/getNotebook?notebookId=${props.notebookId}`
    )
      .then((response) => response.json())
      .then((asJson) => {
        console.log(asJson);
        snippets.value = asJson;

        console.log('GG');
        filterItems();
      });

    // Query the notebook by id to get the notebok name and the list of snippets and users

    const route = useRoute();
    const router = useRouter();

    const tag = ref('');
    const tags = ref([]);

    const notebookName = ref('Notebook Name');

    const query = { ...route.query };

    const path = window.location.pathname;

    query.tags
      ?.split(',')
      .forEach((tagText) =>
        tags.value.push({ text: tagText, tiClasses: ['ti-valid'] })
      );
    const snippetsFiltered = ref(snippets.value);

    const filterItems = () => {
      if (tags.value.length === 0) {
        snippetsFiltered.value = snippets.value;
        router.push({ path, query: {} });
        console.log('---');
        console.log(snippets.value);
        console.log(snippetsFiltered.value);
        return;
      }

      const filterTags = tags.value.map((tag) => tag.text);
      snippetsFiltered.value = snippets.value.filter((item) =>
        item.tags
          .map((tag) => tag.text)
          .some((tagText) => filterTags.includes(tagText))
      );

      const queryValue = filterTags.join();

      router.push({ path, query: { tags: queryValue } });
    };

    const tagClicked = (tagText) => {
      console.log(tags.value);

      const selectedTags = tags.value.map((tag) => tag.text);
      if (selectedTags.includes(tagText)) {
        tags.value = tags.value.filter((tag) => tag.text !== tagText);
        filterItems();
        return;
      }

      tags.value.push({ text: tagText, tiClasses: ['ti-valid'] });
      filterItems();
    };

    return {
      snippets,
      tag,
      tags,
      snippetsFiltered,
      tagClicked,

      router,

      notebookName,
    };
  },
});
</script>

<style scoped>
#snippet-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.snippet-filters {
  display: flex;
  justify-content: space-between;
  margin-top: 1em;
}

.vue-tags-input {
  flex: 1;
}

.snippet-item {
  margin-top: 0.7em;
}

.notebook-board {
  padding: 0 18% 0 18%;
}
</style>
