<template>
  <div class="project-list">
    <div v-for="project in projectList" :key="project.id" class="project">
      <a :href="`/project/${project.id}`">
        {{ project.name }}
      </a>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  components: {},

  props: {},

  emits: [],

  setup(props, { emit }) {
    const projectList = [
      {
        name: 'project 1',
        id: 123,
      },
      {
        name: 'project 2',
        id: 124,
      },
      {
        name: 'project 3',
        id: 125,
      },
      {
        name: 'project 4',
        id: 126,
      },
    ];

    return {
      projectList,
    };
  },
});
</script>

<style scoped>
.project {
  margin: 1em;
  padding: 1.5em;
  background-color: lightgray;
}

.project-list {
  display: flex;
}
</style>
