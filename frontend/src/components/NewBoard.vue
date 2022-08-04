<template>
<div>testing testing</div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { v4 as uuidv4 } from 'uuid';
import { useRouter } from 'vue-router';
import { useAuth0 } from '@auth0/auth0-vue';
import { newSnippet } from './../helpers/apiHelper';

export default defineComponent({
  components: {
  },

  props: {
    notebookId: {
      type: String,
      default: '',
    },
  },

  emits: [],

  setup(props, { emit }) {

    const uuid = uuidv4().replaceAll('-', '');
    const { user } = useAuth0();
    const userId = user.value.sub
    const router = useRouter()

    newSnippet(
      '',
      '',
      '',
      props.notebookId,
      userId,
      uuid
    ).then((text) => {
      router.push(`/notebook/${props.notebookId}#${uuid}`)
    });

    return {
    };
  },
});
</script>

<style>
</style>
