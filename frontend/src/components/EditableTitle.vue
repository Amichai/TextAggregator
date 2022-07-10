<template>
  <div class="project-name">
    <h2
      v-if="!isEditingTitle"
      class="project-name-header"
      @click="isEditingTitle = true"
    >
      {{ modelValueModified }}
    </h2>
    <div class="edit-title-wrapper" v-if="isEditingTitle">
      <input
        class="edit-title-input form-control"
        type="text"
        v-model="modelValueModified"
        placeholder="Title"
        @blur="setIsEditingTitle(false)"
        @keyup.enter="setIsEditingTitle(false)"
        v-focus
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';

export default defineComponent({
  components: {},

  props: {
    modelValue: {
      type: String,
      default: '',
    },
  },

  emits: ['update:modelValue'],

  setup(props, { emit }) {
    const modelValueModified = computed({
      get: () => props.modelValue,
      set: (value) => {
        emit('update:modelValue', value);
      },
    });

    const isEditingTitle = ref(!modelValueModified.value);

    const setIsEditingTitle = (isEditing) => {
      if (!isEditing && !modelValueModified.value) {
        return;
      }
      isEditingTitle.value = isEditing;
    };

    return {
      isEditingTitle,
      setIsEditingTitle,
      modelValueModified,
    };
  },
});
</script>

<style>
.project-name {
  display: flex;
  height: 3em;
}

.project-name-header {
  padding: 0.5px 0.2em 0.5px 0.2em;
}

.project-name-header:hover {
  border-style: solid;
  border-width: 0.5px;
}

.edit-title-wrapper {
  display: flex;
  width: 100%;
}

.edit-title-input {
  margin: 3px;
  font-size: 1.5rem !important;
}
</style>
