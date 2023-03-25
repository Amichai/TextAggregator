<template>
<span class="chat-item-snippet">
  <span class="title"><b>{{title}} </b></span>
  ...
  <span v-for="(word, index) in taken" :key="index">
    <span class="word">{{word}}</span>
  </span>
</span>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';

export default defineComponent({
  components: {
  },

  props: {
    title: {
      type: String,
      required: true,
    },
    body: {
      type: String,
      required: true,
    },
  },

  emits: [],

  setup(props, { emit }) {
    const taken = ref([])

    onMounted(() => {
      const parts = props.body.split(' ').join('\n').split('\n')
      
      parts.reverse()
      let totalLength = 0
      for(var i = 0; i < parts.length; i += 1) {
        const inspection = parts[i]
        if (inspection === null || inspection.trim() === ''){
          continue
        }
        

        if(totalLength + inspection.length + 1 > (80 - props.title.length)) {
          break
        }
        
        totalLength += inspection.length + 1

        taken.value.push(inspection)
      }

      taken.value.reverse()
    })

    return {

      taken,
    };
  },
});
</script>

<style>
.chat-item-snippet {
  display: flex;
  flex-wrap: wrap;
}

.word {
  text-overflow: ellipsis;
  margin-right: 3px;
}

.title {
  margin-right: 0.3rem;
}
</style>
