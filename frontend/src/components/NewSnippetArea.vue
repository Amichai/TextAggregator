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
      <div style="border-style: solid; border-width: 1px; border-color: gray">
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
            class="form-control text-area"
            placeholder="New post here!"
            v-model="body"
            @blur="submitSnippet"
          ></textarea>
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
          {{timeAgo}}
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, onMounted, ref, watch, watchEffect, onBeforeUnmount } from 'vue';
import VueTagsInput from '@sipec/vue3-tags-input';
import { updateSnippet, getSnippet } from './../helpers/apiHelper';
import { useAuth0 } from '@auth0/auth0-vue';
import { useMagicKeys } from '@vueuse/core'
import { useRouter } from "vue-router";
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import utc from 'dayjs/plugin/utc'

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
      if (meta.value && enter.value) {
        submitSnippet()
      }
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

      if(!isSnippetModified(props.snippet)) {
        return
      }

      const snippetId =
        props.snippet?.snippetId;

      updateSnippet(
        title.value ?? '',
        body.value,
        tags.value.map((tag) => tag.text).join(),
        props.notebookId,
        userId,
        snippetId,
      ).then((text) => {
        console.log('Success', text);
        emit('snippetSubmitted', snippetId);
      });
    };

    var polling;

    const timeAgo = ref('')
    const isChangeUnsaved = ref(false)

    const isSnippetModified = (snippet) => {
      var isModified = false
      isModified = snippet.title !== title.value 
          || snippet.body !== body.value

      if(isModified) {
        return true
      }

      const snippetTags = snippet.tags

      if(snippetTags.length != tags.value.length) {
        console.log("tag length changed")
        return true
      }

      const tagTexts = tags.value.map(i => i.text)

      if(!snippetTags.every((element) => {
        return tagTexts.includes(element)
      })) {
        console.log("tag contents are different")
        return true
      }

      return false
    }

    onMounted(() => {
      polling = setInterval(() => {
        timeAgo.value = dayjs.utc(props.snippet.updated).fromNow()

        isChangeUnsaved.value = isSnippetModified(props.snippet)

        if (isChangeUnsaved.value) {
          timeAgo.value = "*" + timeAgo.value
        }
        
		}, 500)
    })

    onBeforeUnmount(() => {
      clearInterval(polling)
    })

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

      updateSnippet(
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
      tagClicked,
      parsedTags,
      backClicked,
      trashClicked,
      timeAgo,
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

  height: 60vh;
  max-height: 60vh;
  min-height: 60vh;

  border-radius: 0;
  
  border:none
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
  border:none
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
  justify-content: space-between
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
