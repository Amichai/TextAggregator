<template>
  <header class="p-3 mb-3 border-bottom header">
    <div class="container">
      <div
        class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start"
      >
        <a class="navbar-brand" href="/">
          <img src="../assets/logo.png" width="40" />
        </a>
        <a
          href="/Notebooks"
          class="d-flex align-items-center mb-2 mb-lg-0 text-dark text-decoration-none"
        >
          <svg
            class="bi me-2"
            width="40"
            height="32"
            role="img"
            aria-label="Bootstrap"
          >
            <use xlink:href="#bootstrap"></use>
          </svg>
        </a>

        <a @click="logout" class="link-primary">
          Log Out
        </a>
      </div>
    </div>
  </header>
</template>

<script>
import { defineComponent } from 'vue';
import { useAuth0 } from '@auth0/auth0-vue';

export default defineComponent({
  setup() {
    const { loginWithRedirect, logout, user } = useAuth0();

    console.log(user.value.sub)

    return {
      login: () => {
       loginWithRedirect();
      },
      logout,
    };
  },
});
</script>

<style scoped>
.header {
  background-color: var(--theme-color2);
}

</style>
