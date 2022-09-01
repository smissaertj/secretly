<template>
  <footer
    class="footer items-center p-4 bg-neutral text-neutral-content mt-5 rounded-b-lg"
  >
    <div class="items-center grid-flow-col">
      <a href="https://joerismissaert.dev" target="_blank">
        <p>© 2022 - Joeri JM Smissaert</p>
      </a>
    </div>
    <div class="grid-flow-col gap-4 md:place-self-center md:justify-self-end">
      <a href="https://github.com/smissaertj/secretly" target="_blank">
        <font-awesome-icon icon="fa-brands fa-square-github" class="fa-2xl" />
      </a>
    </div>
  </footer>
</template>

<script>
export default {
  name: "AppFooter",
};
</script>
