<template>
  <!--  <RouterView />-->
  <div class="flex h-screen">
    <div class="container m-auto px-10">
      <AppNavBar />
      <div class="flex flex-col w-full border-opacity-50 my-auto mt-5">
        <div class="grid card bg-base-300 place-items-center">
          <p class="text-2xl m-4">Retrieve a Message</p>
          <AppRetrieveMsg />
        </div>
        <div class="divider">OR</div>
        <div class="grid card bg-base-300 rounded-box place-items-center">
          <app-login v-if="!userToken" />
          <!--          TODO - Else: show AppSendMsg-->
        </div>
      </div>
      <AppFooter />
    </div>
  </div>
</template>
<script>
// import { RouterLink, RouterView } from "vue-router";
// import HelloWorld from "./components/HelloWorld.vue";

import AppNavBar from "@/components/AppNavBar.vue";
import AppRetrieveMsg from "@/components/AppRetrieveMsg.vue";
import AppFooter from "@/components/AppFooter.vue";
import AppLogin from "@/components/AppLogin.vue";
import { useUserStore } from "@/stores/userStore";

export default {
  name: "App",
  components: {
    AppNavBar,
    AppRetrieveMsg,
    AppLogin,
    AppFooter,
  },
  data() {
    return {
      userToken: "",
    };
  },
  mounted() {
    const userStore = useUserStore();
    this.userToken = userStore.token != "undefined" ? userStore.token : false;
  },
};
</script>
