<template>
  <div
    class="new-snippet-area new-snippet-area-editing"
  >
    <div class="header">
      
      <div class="header-button">
        <i class="bi-arrow-left" @click="backClicked"></i>
      </div>
      

      <div class="header-button" @click="trashClicked">
        <i class="bi-trash"></i>
      </div>
    </div>
    <div>
      <input
        @keydown.enter="submitSnippet"
        class="form-control snippet-title"
        type="text"
        placeholder="Title"
        v-model="title"
        @blur="submitSnippet"
      />
      <textarea
        ref="textAreaRef"
        class="form-control text-area"
        placeholder="New post here!"
        v-model="body"
        @input="textAreaChange"
        @blur="submitSnippet"
      ></textarea>
      <VueTagsInput
        class="vue-tags-input"
        placeholder="Tags"
        v-model="tag"
        :tags="tags"
        @tags-changed="(newTags) => (tags = newTags)"
        @blur="submitSnippet"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, onMounted, ref, watch, watchEffect } from 'vue';
import VueTagsInput from '@sipec/vue3-tags-input';
import { newSnippet } from './../helpers/apiHelper';
import { v4 as uuidv4 } from 'uuid';
import { useAuth0 } from '@auth0/auth0-vue';
import { useMagicKeys } from '@vueuse/core'
import { useRouter } from "vue-router";


export default defineComponent({
  components: {
    VueTagsInput,
  },

  props: {
    notebookId: {
      type: String,
      default: '',
    },
    snippet: {
      type: Object,
      required: false,
    },
  },

  emits: ['tagClicked', 'snippetSubmitted', 'cancelChanges', 'backClicked'],

  setup(props, { emit }) {
    const { meta, enter } = useMagicKeys()

    watchEffect(() => {
      if (meta.value && enter.value)
        submitSnippet()
    })

    const body = ref(props.snippet?.body ?? '')
    const router = useRouter()
    
    router.push(`/notebook/${props.notebookId}#${props.snippet.snippetId}`)

    const tag = ref('');
    const tags = ref(
      (props.snippet?.tags ?? []).filter((i) => i).map((i) => ({ text: i }))
    );

    const title = ref(props.snippet?.title ?? '');

    const { user } = useAuth0();
    const userId = user.value.sub

    const cancelChanges = () => {
      emit('cancelChanges', props.snippet);
    };

    const submitSnippet = async () => {
      if(!body.value && !title.value) {
        return
      }

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
      });
    };

    const textAreaRef = ref(null)

    onMounted(() => {
      textAreaRef.value.style.height = "";
      textAreaRef.value.style.height = textAreaRef.value.scrollHeight + "px"
    })

    const textAreaChange = () => {
      textAreaRef.value.style.height = "";
      textAreaRef.value.style.height = textAreaRef.value.scrollHeight + "px"
    }

    const tagClicked = (evt, tagText) => {
      evt.stopPropagation();
      emit('tagClicked', tagText);
    };

    const parsedTags = ref(props.snippet.tags.filter((t) => t !== ''));

    const backClicked = () => {
      router.push(`/notebook/${props.notebookId}`)
      emit('backClicked')
    }

    const trashClicked = () => {
      const snippetId =
        props.snippet?.snippetId

      newSnippet(
        title.value ?? '',
        body.value,
        tags.value.map((tag) => tag.text).join() + ',trash',
        props.notebookId,
        userId,
        snippetId
      ).then((text) => {
        console.log('Success', text);

        backClicked()
      });

    }

    return {
      body,
      tag,
      tags,
      title,
      submitSnippet,

      cancelChanges,
      textAreaRef,
      textAreaChange,
      tagClicked,
      parsedTags,
      backClicked,
      trashClicked,
    };
  },
});
</script>

<style scoped>
.new-snippet-area {
  background-color: lightgray;
  /* padding: 0.5em; */
  border-radius: 0.5em;
  margin-bottom: 1em;
  /* width: 55%; */
}

.new-snippet-area-editing {
  width: 90%;
}

.header-area {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.text-area {
  /* height: 10em; */
  min-height: 10em;
  overflow-y: hidden;
}

.vue-tags-input {
  width: 100%;
}

.footer {
  display: flex;
  align-items: center;
}
.tags-container {
  display: flex;
  flex-wrap: wrap;
  flex: 1;
}
.tag-p {
  background-color: var(--tag-color);
  color: white;
  margin: 5px;
  padding: 2.5px 10px 2.5px 10px;
  border-radius: 3px;
  font-size: 0.7em;
  height: fit-content;
  cursor: pointer;
}

.filter-tag {
  background: rgb(208, 86, 72);
}

a {
  margin-right: 1em;
}

.snippet-title {
  font-weight: bold;
}

.header-button {
  width: 3em;
  height: 2.5em;
  border-radius: 10em;
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.header-button :hover {
  background-color: white;
  width: 2.5em;
  height: 2.5em;
  border-radius: 10em;
  display: flex;
  justify-content: space-around;
  align-items: center;
  cursor: pointer;
}

.header {
  display: flex;
}
</style>
