<template>
<header class="p-3 mb-3 border-bottom fixed-top board-header">
    <div class="container">
      <div class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start">
        <a href="/" class="d-flex align-items-center mb-2 mb-lg-0 text-dark text-decoration-none">
          <svg class="bi me-2" width="40" height="32" role="img" aria-label="Bootstrap"><use xlink:href="#bootstrap"></use></svg>
        </a>

        <ul class="nav col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0">
          <li>
            <button
              type="button"
              :class="[
                'btn', 'btn-default', 'bi-pencil', 'new-button',
              ]"
              @click="newPost"
            >
            New
          </button>

          </li>
          
        </ul>

        <div class="updated-created-buttons">
            <span
              @click="sortCreatedClicked"
              :class="[
                'noselect',
                'sort-icon',
                selectedSortOption[0] === 'C' && 'icon-selected',
              ]"
            >
              <i v-if="selectedSortOption === 'CU'" class="bi bi-sort-up"></i>
              <i v-else class="bi bi-sort-down"></i>
              Created
            </span>
            <span
              @click="sortUpdatedClicked"
              :class="[
                'noselect',
                'sort-icon',
                selectedSortOption[0] === 'U' && 'icon-selected',
              ]"
            >
              <i v-if="selectedSortOption === 'UU'" class="bi bi-sort-up"></i>
              <i v-else class="bi bi-sort-down"></i>
              Updated
            </span>
            <span
              @click="sortUpdatedClicked"
              :class="[
                'noselect',
                'sort-icon',
                selectedSortOption[0] === 'U' && 'icon-selected',
              ]"
            >
              <i v-if="selectedSortOption === 'UU'" class="bi bi-sort-up"></i>
              <i v-else class="bi bi-sort-down"></i>
              Size
            </span>
        </div>

        <form class="col-12 col-lg-auto mb-3 mb-lg-0 me-lg-3" role="search">
          <input type="search" class="form-control" placeholder="Search..." aria-label="Search">
        </form>

        <div class="dropdown text-end">
          <a href="#" class="d-block link-dark text-decoration-none dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
            <img src="https://github.com/mdo.png" alt="mdo" width="32" height="32" class="rounded-circle">
          </a>
          <ul class="dropdown-menu text-small">
            <li><a
              @click="logout"
              class="dropdown-item" href="#">Sign out</a></li>
          </ul>
        </div>
      </div>
    </div>
  </header>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useAuth0 } from '@auth0/auth0-vue';

export default defineComponent({
  components: {
  },

  props: {
  },

  emits: [],

  setup(props, { emit }) {
    const { logout, user } = useAuth0();
    console.log(user.value.sub);

    const sortOptions = ref(['CU', 'CD', 'UU', 'UD']);

    const selectedSortOption = ref(sortOptions.value[0]);

    

    /// HOME, LOGOUT, SEARCH, SORT, NEW
    return {
      logout,

      sortOptions,
      selectedSortOption,
    };
  },
});
</script>

<style>
.board-header {
  background-color: var(--theme-color2);
}

.new-button {
  width: 8em;
  background-color: var(--theme-color3) !important;
}

.updated-created-buttons {
  display: flex;
  align-items: baseline;
}

.icon-selected {
  color: black;
}

.sort-icon:hover {
  background-color: lightgray;
  cursor: pointer;
}

.sort-icon {
  padding: 9px 15px 9px 15px;
  margin: 0 8px 0 8px;
  border-radius: 1.1em;
  color: white;
  border-color: lightgray;
  border-style: solid;
  background-color: var(--theme-color4);
}
</style>
