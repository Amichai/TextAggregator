<template>
<!-- <div> -->
  <!-- <p v-for="(row, index) in rows" :key="index"
    :value="row"
    class="text-row"
  >
    <input type="text" :value="row" class="text-row-input"/>
  </p> -->
    <!-- class="form-control text-area" -->
<!-- </div> -->
  <contenteditable
    class="form-control text-area"
    tag="div"
    :contenteditable="true"
    v-model="body"
  />
    <!-- v-model="body" -->
    <!-- @blur="submitSnippet" -->
</template>

<script>

import contenteditable from 'vue-contenteditable';
import { defineComponent, ref } from 'vue';

export default defineComponent({
  components: {
    contenteditable
  },

  props: {
    body: {
      type: String,
      default: '',
    },
  },

  setup(props, { emit }) {

    const rows = ref([])

    rows.value = props.body.split('\n')


    return {
      rows,
    }
  },
})
</script>

<style scoped>

.text-row-input:nth-child(even) {
  background-color: lightgray
}


.text-area {
  /* height: 10em; */
  /* min-height: 10em; */

  /* height: 60vh;
  max-height: 60vh;
  min-height: 60vh; */

  border-radius: 0;

  border: none;
  overflow: auto;
}

.text-row {
  margin: 0;
  /* padding: 0.2rem; */
  min-height: 1.5rem;
}

.text-row-input {
width: 100%;
}
</style>