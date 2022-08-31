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
          <p class="text-2xl m-4">Login To Send a Message</p>
          <button @click="login" class="btn btn-accent m-4">Log in</button>
        </div>
      </div>
      <AppFooter />
    </div>
  </div>
</template>
<script>
// import { RouterLink, RouterView } from "vue-router";
// import HelloWorld from "./components/HelloWorld.vue";
import AppNavBar from "./components/AppNavBar.vue";
import AppRetrieveMsg from "./components/AppRetrieveMsg.vue";
import AppFooter from "./components/AppFooter.vue";
import { useAuth0 } from "@auth0/auth0-vue";

export default {
  name: "App",
  components: {
    AppNavBar,
    AppRetrieveMsg,
    AppFooter,
  },
  setup() {
    const { loginWithRedirect } = useAuth0();

    return {
      login: () => {
        try {
          loginWithRedirect();
        } catch (error) {
          console.log(error);
        }
      },
    };
  },
};
</script>
