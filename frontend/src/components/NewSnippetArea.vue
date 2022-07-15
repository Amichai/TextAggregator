<template>
  <div class="new-snippet-area">
    <div class="header-area" @click="toggleExpandCollapse">
      <h4>New Post</h4>
      <div>
        <i class="bi bi-arrows-collapse" v-if="!isCollapsed"></i>
        <i class="bi bi-arrows-expand" v-if="isCollapsed"></i>
      </div>
    </div>
    <div v-if="!isCollapsed">
      <input
        class="form-control"
        type="text"
        placeholder="Title"
        v-model="snippetName"
      />
      <textarea
        class="form-control text-area"
        placeholder="New post here!"
        v-model="body"
      ></textarea>
      <VueTagsInput
        class="vue-tags-input"
        placeholder="Tags"
        v-model="tag"
        :tags="tags"
        @tags-changed="(newTags) => (tags = newTags)"
      />
      <button
        type="button"
        class="btn btn-primary submit-button"
        @click="submitSnippet"
      >
        Post
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import VueTagsInput from '@sipec/vue3-tags-input';
import { newSnippet } from './../helpers/apiHelper';
import { v4 as uuidv4 } from 'uuid';

export default defineComponent({
  components: {
    VueTagsInput,
  },

  props: {
    notebookId: {
      type: String,
      default: '',
    },
  },

  emits: ['snippetSubmitted'],

  setup(props, { emit }) {
    const isCollapsed = ref(true);
    const body = ref('');
    const tag = ref('');
    const tags = ref([]);
    const snippetName = ref('');

    const toggleExpandCollapse = () => {
      isCollapsed.value = !isCollapsed.value;
    };

    const submitSnippet = async () => {
      const snippetId = uuidv4().replaceAll('-', '');
      newSnippet(
        snippetName.value ?? '',
        body.value,
        tags.value.map((tag) => tag.text).join(),
        props.notebookId,
        'amichai',
        snippetId
      ).then((text) => {
        console.log('Success', text);

        emit('snippetSubmitted');
      });
    };

    const snippetPostSuccessCallback = () => {
      body.value = '';
      tag.value = '';
      tags.value = [];
      snippetName.value = '';
    };

    return {
      isCollapsed,
      body,
      tag,
      tags,
      snippetName,
      submitSnippet,
      toggleExpandCollapse,

      snippetPostSuccessCallback,
    };
  },
});
</script>

<style scoped>
.new-snippet-area {
  background-color: lightgray;
  padding: 1em;
  border-radius: 0.5em;
}

.header-area {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.text-area {
  height: 10em;
  min-height: 10em;
  margin-top: 0.6em;
}

.vue-tags-input {
  margin: 0.5em;
  width: 100%;
}
</style>
