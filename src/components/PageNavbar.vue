<template>
  <header class="p-3 mb-3 border-bottom header">
    <div class="container">
      <div
        class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start"
      >
        <a class="navbar-brand" href="/Projects">
          <img src="../assets/logo.png" width="40" />
        </a>
        <a
          href="/Projects"
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
      </div>
    </div>
  </header>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  setup() {
    return {};
  },
});
</script>

<style scoped>
.header {
  background-color: lightgray;
}
</style>
