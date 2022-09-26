<template>
  <div class="new-snippet-area new-snippet-area-editing" v-if="isSnippetLoaded">
    <div class="header">
      <div class="header-button">
        <i class="bi-arrow-left" @click="backClicked"></i>
      </div>

      <div class="header-button" @click="trashClicked">
        <i class="bi-trash"></i>
      </div>
      <!-- <div class="header-button" @click="highlightClicked">
        <i class="bi-magic"></i>
      </div> -->
    </div>
    <div>
      <div style="border-style: solid; border-width: 1px; border-color: gray">
        <div style="overflow: auto; background-color: white; height: 70vh">
          <input
            @keydown.enter="submitSnippet"
            class="form-control snippet-title"
            type="text"
            placeholder="Title"
            v-model="title"
            @blur="submitSnippet"
          />
          <contenteditable
            class="form-control text-area"
            v-model="body"
            tag="div"
            :contenteditable="true"
            @blur="submitSnippet"
          >
          </contenteditable>
        </div>
      </div>
      <div class="footer">
        <VueTagsInput
          class="vue-tags-input"
          placeholder="Tags"
          v-model="tag"
          :tags="tags"
          @tags-changed="(newTags) => (tags = newTags)"
          @blur="submitSnippet"
        />
        <div class="time-ago">
          {{ timeAgo }}
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import {
  computed,
  defineComponent,
  onMounted,
  ref,
  watch,
  watchEffect,
  onBeforeUnmount,
} from 'vue';
import VueTagsInput from '@sipec/vue3-tags-input';
import {
  updateSnippet,
  getSnippet,
  updateNotebook,
} from './../helpers/apiHelper';
import { useAuth0 } from '@auth0/auth0-vue';
import { useMagicKeys } from '@vueuse/core';
import { useRouter } from 'vue-router';
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';
import utc from 'dayjs/plugin/utc';
import { removeElement, parseTags } from './../helpers/helpers';
import contenteditable from 'vue-contenteditable';

export default defineComponent({
  components: {
    VueTagsInput,
    contenteditable,
  },

  props: {
    notebookId: {
      type: String,
      default: '',
    },
    snippetId: {
      type: String,
      required: false,
    },
    userId: {
      type: String,
      required: true,
    },
  },

  emits: [
    'tagClicked',
    'snippetSubmitted',
    'cancelChanges',
    'backClicked',
    'snippetUpdated',
  ],

  setup(props, { emit }) {
    const { meta, enter } = useMagicKeys();

    const initialSnippet = ref(null);
    const isSnippetLoaded = ref(false);
    const body = ref(null);
    const tag = ref('');

    const tags = ref(null);

    const title = ref(null);

    getSnippet(props.notebookId, props.snippetId, props.userId).then(
      (snippet) => {
        initialSnippet.value = snippet;
        initialSnippet.value.tags = parseTags(snippet.tags);
        body.value = snippet.body;
        title.value = snippet.title;
        tags.value = snippet.tags
          .filter((i) => i !== '')
          .map((i) => ({ text: i }));
        isSnippetLoaded.value = true;
      }
    );

    watchEffect(() => {
      if (meta.value && enter.value) {
        submitSnippet();
      }
    });

    const router = useRouter();

    router.push(`/notebook/${props.notebookId}#${props.snippetId}`);

    const cancelChanges = () => {
      emit('cancelChanges', initialSnippet);
    };

    const submitSnippet = async () => {
      if (!body.value && !title.value) {
        return;
      }

      if (!isSnippetModified(initialSnippet.value)) {
        return;
      }

      const snippetId = props.snippetId;

      updateSnippet(
        title.value ?? '',
        body.value,
        tags.value.map((tag) => tag.text).join(),
        props.notebookId,
        props.userId,
        snippetId
      ).then((text) => {
        console.log('Success', text);
        emit('snippetSubmitted', snippetId);

        initialSnippet.value.title = title.value;
        initialSnippet.value.body = body.value;
        initialSnippet.value.tags = tags.value.map((i) => i.text);
      });
    };

    var isSavedPoll, querySnippetPoll;

    const timeAgo = ref('');
    const isChangeUnsaved = ref(false);

    const isSnippetModified = (snippet) => {
      var isModified = false;
      isModified = snippet?.title !== title.value || snippet.body !== body.value;

      if (isModified) {
        console.log('is modified');
        return true;
      }

      const snippetTags = snippet.tags.filter((i) => i !== '');

      if (snippetTags.length != tags.value.length) {
        console.log('tag length changed');
        return true;
      }

      const tagTexts = tags.value.map((i) => i.text);

      if (
        !snippetTags.every((element) => {
          return tagTexts.includes(element);
        })
      ) {
        console.log('tag contents are different');
        return true;
      }

      return false;
    };

    onMounted(() => {
      isSavedPoll = setInterval(() => {
        timeAgo.value = dayjs.utc(initialSnippet.updated).fromNow();

        isChangeUnsaved.value = isSnippetModified(initialSnippet.value);

        if (isChangeUnsaved.value) {
          timeAgo.value = '*' + timeAgo.value;
        }
      }, 400);

      querySnippetPoll = setInterval(() => {
        if (isChangeUnsaved.value) {
          return;
        }
        console.log('get snippet', dayjs().format());
        getSnippet(props.notebookId, props.snippetId, props.userId).then(
          (updatedSnippet) => {
            emit('snippetUpdated', updatedSnippet);

            title.value = updatedSnippet.title;
            body.value = updatedSnippet.body;
            tags.value = updatedSnippet.tags
              .filter((i) => i !== '')
              .map((i) => ({ text: i }));

            initialSnippet.value.title = title.value;
            initialSnippet.value.body = body.value;
            initialSnippet.value.tags = tags.value.map((i) => i.text);
          }
        );
      }, 10000);
    });

    onBeforeUnmount(() => {
      clearInterval(isSavedPoll);
      clearInterval(querySnippetPoll);
    });

    const tagClicked = (evt, tagText) => {
      evt.stopPropagation();
      emit('tagClicked', tagText);
    };

    const backClicked = () => {
      router.push(`/notebook/${props.notebookId}`);
      emit('backClicked');
    };

    const trashClicked = () => {
      const snippetId = props.snippetId;

      updateSnippet(
        title.value ?? '',
        body.value,
        tags.value.map((tag) => tag.text).join() + ',trash',
        props.notebookId,
        props.userId,
        snippetId
      ).then((text) => {
        console.log('Success', text);
        backClicked();
      });
    };

    return {
      body,
      tag,
      tags,
      title,
      submitSnippet,

      cancelChanges,
      tagClicked,
      backClicked,
      trashClicked,
      timeAgo,
      isSnippetLoaded,
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

  /* height: 60vh;
  max-height: 60vh;
  min-height: 60vh; */

  border-radius: 0;

  border: none;
  overflow: auto;
}

* :focus {
  box-shadow: none !important;
}

.vue-tags-input {
  width: 100%;
}

.snippet-title {
  font-weight: bold;
  border-radius: 0;
  box-shadow: none;
  border: none;
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

.time-ago {
  margin-right: 1em;
  font-size: small;
  font-style: italic;
}

.header {
  display: flex;
}

.footer {
  display: flex;
  justify-content: space-between;
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
</style>
