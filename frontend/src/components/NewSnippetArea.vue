<template>
  <div class="new-snippet-area">
    <div class="header-area" @click="toggleExpandCollapse">
      <h4>New Post</h4>
      <div v-if="!isEditingExistingSnippet">
        <i class="bi bi-arrows-collapse" v-if="!isCollapsed"></i>
        <i class="bi bi-arrows-expand" v-if="isCollapsed"></i>
      </div>
    </div>
    <div v-if="!isCollapsed">
      <input
        class="form-control"
        type="text"
        placeholder="Title"
        v-model="title"
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
        {{ isEditingExistingSnippet ? 'Save' : 'Post' }}
      </button>
      <button
        type="button"
        class="btn btn-primary submit-button cancel-button"
        @click="cancelChanges"
      >
        Cancel
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

    isEditingExistingSnippet: {
      type: Boolean,
      default: false,
    },

    parentSnippet: {
      type: Object,
      required: false,
    },
  },

  emits: ['snippetSubmitted', 'cancelChanges'],

  setup(props, { emit }) {
    const isCollapsed = ref(!props.isEditingExistingSnippet);
    const body = ref(props.parentSnippet?.body ?? '');
    const tag = ref('');
    const tags = ref(
      (props.parentSnippet?.tags ?? []).map((i) => ({ text: i }))
    );
    const title = ref(props.parentSnippet?.title ?? '');

    const toggleExpandCollapse = () => {
      isCollapsed.value = !isCollapsed.value;
    };

    const cancelChanges = () => {
      emit('cancelChanges', props.parentSnippet);
    };

    const submitSnippet = async () => {
      const snippetId = uuidv4().replaceAll('-', '');
      newSnippet(
        title.value ?? '',
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
      title.value = '';
    };

    return {
      isCollapsed,
      body,
      tag,
      tags,
      title,
      submitSnippet,
      toggleExpandCollapse,

      snippetPostSuccessCallback,
      cancelChanges,
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

.cancel-button {
  margin-left: 1em;
}
</style>
