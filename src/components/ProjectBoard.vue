<template>
  <div>
    <PageNavbar />
  </div>
  <div class="root">
    <div class="feed-filters">
      <VueTagsInput
        class="vue-tags-input"
        placeholder="Tag filters"
        v-model="tag"
        :tags="tags"
        @tags-changed="(newTags) => (tags = newTags)"
      />
    </div>

    <NewPostButton :clickEvent="() => isEditorVisible = true" />

    <Editor
      v-if="isEditorVisible"
      api-key="87di36sy23q93vwyyaopux8zr5pi3l3zqim8wr2029pg314f"
      type="body"
      name="body"
      id="body"
      v-model="body"
      :init="{
        menubar: false,
        statusbar: false,
        paste_block_drop: true,
        plugins: [],
        toolbar:
          'image | undo redo | link | bold italic | \
            alignleft aligncenter alignright alignjustify | \
            outdent indent',
      }"
    />
    <ul id="feed-list"></ul>
    <div v-if="notesFiltered.length === 0 && notes.length > 0">
      <br />
      <br />
      <i>No results match selected tag filters</i>
    </div>
    <div v-if="notes.length === 0">
      <br />
      <br />
      <i>No posts to show</i>
    </div>
  </div>
</template>

<script>
// This view is similar to keep
// A rich editor at the top to create a note
// a list of notes + tags
// search, tag filtering
// collaborators
// When clicked, display the content in a scrollable modal?
import { defineComponent, ref, watch } from 'vue';
import VueTagsInput from '@sipec/vue3-tags-input';
import { useRoute, useRouter } from 'vue-router';
import Editor from '@tinymce/tinymce-vue';
import PageNavbar from './PageNavbar.vue';
import NewPostButton from './NewPostButton.vue';

export default defineComponent({
  components: {
    VueTagsInput,
    Editor,
    PageNavbar,
    NewPostButton,
  },
  props: {
    projectId: {
      type: String,
      default: '',
    },
  },

  setup(props) {
    console.log(`Project id: ${props.projectId}`);

    const isEditorVisible = ref(false);

    const route = useRoute();
    const router = useRouter();

    const notes = ref([]);

    const tag = ref('');
    const tags = ref([]);

    const body = ref('');

    const query = { ...route.query };

    const path = window.location.pathname;
    
    query.tags
      ?.split(',')
      .forEach((tagText) => tags.value.push({ text: tagText, tiClasses: ['ti-valid'] }));
    const notesFiltered = ref(notes.value);

    const filterItems = () => {
      if (tags.value.length === 0) {
        notesFiltered.value = notes;
        router.push({ path, query: {} });
        return;
      }

      const filterTags = tags.value.map((tag) => tag.text);
      notesFiltered.value = notes.value.filter((item) => item.tags
        .map((tag) => tag.text)
        .some((tagText) => filterTags.includes(tagText)));

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
      notes,
      tag,
      tags,
      body,
      notesFiltered,
      tagClicked,

      isEditorVisible,
    };
  },
});
</script>

<style scoped>
#feed-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.feed-filters {
  display: flex;
  justify-content: space-between;
}

.vue-tags-input {
  flex: 1;
}

.feed-item {
  margin-top: 0.7em;
}

.root {
  padding: 0 18% 0 18%;
}
</style>
