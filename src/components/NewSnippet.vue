<template>
  <PageNavbar />
  <div class="new-snippet">
    <a class="link-primary" :href="`/project/${projectId}`">Project</a>
    <h2>New Snippet</h2>
    <div>
      <input type="text" class="form-control" placeholder="Title" />
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
    <button type="button" class="btn btn-primary" @click="clickEvent">
      Submit
    </button>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import Editor from '@tinymce/tinymce-vue';
import VueTagsInput from '@sipec/vue3-tags-input';
import PageNavbar from './PageNavbar.vue';

export default defineComponent({
  components: {
    VueTagsInput,
    Editor,
    PageNavbar,
  },

  props: {
    projectId: {
      type: String,
      default: '',
    },
  },

  emits: [],

  setup(props, { emit }) {
    console.log(`Project id: ${props.projectId}`);
    const body = ref('');
    const tag = ref('');
    const tags = ref([]);

    return {
      body,
      tag,
      tags,
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
