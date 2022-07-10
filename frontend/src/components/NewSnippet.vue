<template>
  <div>
    <PageNavbar />
    <div class="new-snippet">
      <a class="link-primary" :href="`/notebook/${notebookId}`"
        >Back to Notebook</a
      >
      <div>
        <EditableTitle v-model="snippetName" />
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
          toolbar:
            'image | undo redo | link | bold italic | \
            alignleft aligncenter alignright alignjustify | \
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
      <button type="button" class="btn btn-primary" @click="submitSnippet">
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
  },

  emits: [],

  setup(props, { emit }) {
    console.log(`notebook id: ${props.notebookId}`);
    const body = ref('');
    const tag = ref('');
    const tags = ref([]);

    const router = useRouter();

    const snippetName = ref('');

    const submitSnippet = async () => {
      const post = {
        title: snippetName.value,
        body: body.value,
        tags: tags.value.map((tag) => tag.text).join(),
        notebookId: props.notebookId,
        userId: 'amichai',
      };

      const raw = JSON.stringify(post);

      const requestOptions = {
        method: 'POST',
        body: raw,
      };

      try {
        const response = await fetch(
          'https://8cem0l4r4j.execute-api.us-east-1.amazonaws.com/newSnippet',
          requestOptions
        );
        const data = await response.text();
        console.log('Success', data);

        router.push(`/notebook/${props.notebookId}`);
        return true;
      } catch (error) {
        console.log('error', error);
        return null;
      }
    };

    return {
      body,
      tag,
      tags,
      snippetName,
      submitSnippet,
    };
  },
});
</script>

<style scoped>
.new-snippet {
  padding: 0 18% 0 18%;
}

.link-primary {
  cursor: pointer;
}
</style>
