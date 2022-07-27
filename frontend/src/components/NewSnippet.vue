<template>
  <div>
    <PageNavbar />
    <div class="new-snippet">
      Back to
      <a class="link-primary" :href="`/notebook/${notebookId}`">{{
        notebookName
      }}</a>
      <div>
        <EditableTitle v-model="title">
          <h3>
            {{title}}
          </h3>
        </EditableTitle>
      </div>
      <Editor
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
          toolbar: 'bold italic | \
            outdent indent',
        }"
      />
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
        Submit
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import Editor from '@tinymce/tinymce-vue';
import VueTagsInput from '@sipec/vue3-tags-input';
import { useRouter } from 'vue-router';
import PageNavbar from './PageNavbar.vue';
import EditableTitle from './EditableTitle.vue';
import {
  getNotebookInfo,
  newSnippet,
  getSnippet,
} from './../helpers/apiHelper';
import { useAuth0 } from '@auth0/auth0-vue';

export default defineComponent({
  components: {
    VueTagsInput,
    Editor,
    PageNavbar,
    EditableTitle,
  },

  props: {
    notebookId: {
      type: String,
      default: '',
    },
    snippetId: {
      type: String,
      default: '',
    },
  },

  emits: [],

  setup(props, { emit }) {
    console.log(`notebook id: ${props.notebookId}`);
    console.log(`snippet id: ${props.snippetId}`);
    const notebookName = ref('');

    const { user } = useAuth0();
    const userId = user.value.sub

    getNotebookInfo(props.notebookId).then((json) => {
      notebookName.value = json.name;
      console.log(json);
    });

    const body = ref('');
    const tag = ref('');
    const tags = ref([]);

    const router = useRouter();

    const title = ref('');
    getSnippet(props.notebookId, props.snippetId, userId).then((json) => {
      title.value = json.name;
      body.value = json.body;
      tags.value = json.tags.split(',').map((tagText) => ({
        text: tagText,
        tiClasses: ['ti-valid'],
      }));
    });

    const submitSnippet = async () => {
      newSnippet(
        title.value ?? '',
        body.value,
        tags.value.map((tag) => tag.text).join(),
        props.notebookId,
        userId,
        props.snippetId
      ).then((text) => {
        console.log('Success', text);

        router.push(`/notebook/${props.notebookId}`);
      });
    };

    return {
      body,
      tag,
      tags,
      title,
      submitSnippet,
      notebookName,
    };
  },
});
</script>

<style scoped>
.new-snippet {
  padding: 0 18% 0 18%;
}

.vue-tags-input {
  margin: 0.5em;
}

.submit-button {
  margin: 0.5em;
}
</style>
