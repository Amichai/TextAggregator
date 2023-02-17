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

        <form class="col-12 col-lg-auto mb-3 mb-lg-0 me-lg-3" role="search">
          <input type="search" class="form-control" placeholder="Search..." aria-label="Search">
        </form>

        <div class="dropdown">
          <a class="btn btn-secondary dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            {{ selectedSortOption }}
          </a>

          <ul class="dropdown-menu">
            <li>
              <a class="dropdown-item" href="#"
                @click="() => setSortOption('CU')"
              >
                Created</a></li>
            <li><a class="dropdown-item" href="#"
              @click="() => setSortOption('UU')">
              Updated</a></li>
            <li><a class="dropdown-item" href="#"
            @click="() => setSortOption('SU')">
              Size</a></li>
          </ul>
        </div>

        <div class="dropdown text-end">
          <a
              @click="logout"
              class="dropdown-item" href="#">Sign out</a>
        </div>
      </div>
    </div>
  </header>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useAuth0 } from '@auth0/auth0-vue';
import { useRouter, useRoute } from 'vue-router';

export default defineComponent({
  components: {
  },

  props: {
  },

  emits: ['newPost', 'sortChanged'],

  setup(props, { emit }) {
    const { logout, user } = useAuth0();
    console.log(user.value.sub);

    const router = useRouter();
    const route = useRoute();
    
    const selectedSortOption = ref('Sort');
    

    const newPost = () => {
      emit('newPost')
    }

    const sortOptionMapper = {
      'CU': '↑ Created',
      'CD': '↓ Created',
      'UU': '↑ Updated',
      'UD': '↓ Updated',
      'SU': '↑ Size',
      'SD': '↓ Size',
    }

    const setSortOption = (sortOption) => {
      const path = route.path;
      if (route.query['sort'] && route.query['sort'][1] == "U") {
        sortOption = sortOption[0] + "D"
      }

      router.push({ path, query: { ...route.query, sort: sortOption } });

      selectedSortOption.value = sortOptionMapper[sortOption];

      emit('sortChanged')
    }

    /// HOME, LOGOUT, SEARCH, SORT, NEW
    return {
      logout,

      selectedSortOption,

      setSortOption,

      newPost,
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
