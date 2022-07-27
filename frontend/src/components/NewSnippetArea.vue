<template>
  <div
    :class="[
      'new-snippet-area',
      isEditingExistingSnippet && 'new-snippet-area-editing',
    ]"
    v-click-outside="cancelChanges"
  >
    <div
      class="header-area"
      @click="toggleExpandCollapse"
      v-if="!isEditingExistingSnippet"
    >
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
import { useAuth0 } from '@auth0/auth0-vue';


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

    snippet: {
      type: Object,
      required: false,
    },
  },

  emits: ['snippetSubmitted', 'cancelChanges'],

  setup(props, { emit }) {
    const isCollapsed = ref(!props.isEditingExistingSnippet);
    const body = ref(props.snippet?.body ?? '');
    const tag = ref('');
    const tags = ref(
      (props.snippet?.tags ?? []).filter((i) => i).map((i) => ({ text: i }))
    );
    const title = ref(props.snippet?.title ?? '');

    const toggleExpandCollapse = () => {
      isCollapsed.value = !isCollapsed.value;
    };

    const { user } = useAuth0();
    const userId = user.value.sub

    const cancelChanges = () => {
      isCollapsed.value = true
      emit('cancelChanges', props.snippet);
    };

    const submitSnippet = async () => {
      isCollapsed.value = true
      const snippetId =
        props.snippet?.snippetId ?? uuidv4().replaceAll('-', '');
      newSnippet(
        title.value ?? '',
        body.value,
        tags.value.map((tag) => tag.text).join(),
        props.notebookId,
        userId,
        snippetId
      ).then((text) => {
        console.log('Success', text);

        emit('snippetSubmitted');

        body.value = '';
        tag.value = '';
        tags.value = [];
        title.value = '';
      });
    };

    return {
      isCollapsed,
      body,
      tag,
      tags,
      title,
      submitSnippet,
      toggleExpandCollapse,

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
  width: 55%;
}

.new-snippet-area-editing {
  width: 100%;
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
