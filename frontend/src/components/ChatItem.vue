<template>
<div class="chat-item" @click="onClick">
  <div class="left-side">
    <span class="chat-item-title">
    <div>{{dayjs.utc(snippet.updated).fromNow()}}</div>
      <ChatItemSnippet :title="snippet.title" :body="snippet.body" />
    </span>
    <!-- <span>
      <b>{{snippet.updated}}</b>
    </span> -->

      <div class="chat-item-tags" v-if="snippet.tags.length > 0">
      <p
        v-for="(tag, index) in snippet.tags"
        v-bind:key="index"
        @click="(ev) => tagClicked(ev, tag)"
        :class="['tag-p', filterTags.includes(tag) && 'filter-tag']"
      >
        {{ tag }}
      </p>
    </div>
  </div>
</div>
</template>

<script lang="ts">
import { 
  defineComponent,
  PropType,
} from 'vue';
import dayjs from 'dayjs';
import ChatItemSnippet from './ChatItemTitleAndSnippet.vue';

export default defineComponent({
  components: {
    ChatItemSnippet,
  },

  props: {
    snippet: {
      type: Object,
      required: true,
    },
    filterTags: {
      type: Array as PropType<any>,
      required: true,
    },
  },

  emits: ['clicked'],

  setup(props, { emit }) {
    const onClick = () => {
      emit('clicked', props.snippet)
    }

    return {
      dayjs,
      onClick,
    };
  },
});
</script>

<style>
.chat-item {
  /* border-radius: 0.4rem; */
  background-color: white;
  /* height: 5rem; */
  display: grid;
  /* box-shadow: 0px 4px 10px 0px gray; */
  border: 1px solid black;
  
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

.left-side {
  display: flex;
  justify-content: space-between;
  flex-direction: column;
}

.right-side {
  display: flex;
  flex-direction: column;
  text-overflow: ellipsis;
}

.filter-tag {
  background: rgb(208, 86, 72);
}

.chat-item-tags {
  display: flex;
}

.chat-item-title {
  /* background-color: blue; */
  margin: 0.5rem 0rem 0 0.5rem
}
</style>
