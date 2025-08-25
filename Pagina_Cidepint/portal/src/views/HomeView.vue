<template>
  <body>
    <AppHeader />
    <HomeContent />
    <AppFooter />
  </body>
</template>

<script>
  import AppHeader from "@/components/AppHeader.vue";
  import AppFooter from "@/components/AppFooter.vue";
  import HomeContent from "@/components/HomeContent.vue";

  export default {
    name: "HomeView",
    components: {
      AppHeader,
      AppFooter,
      HomeContent,
    },
  };
</script>

<style scoped>

</style>