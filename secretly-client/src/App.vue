<template>
  <div class="flex h-screen">
    <div class="container m-auto px-10">
      <!--  Navbar-->
      <div class="navbar bg-neutral text-neutral-content mt-4 rounded-t-lg">
        <div class="navbar-start">
          <a class="btn btn-ghost normal-case text-xl" href="/">Secretly</a>
        </div>
        <div class="navbar-center hidden lg:flex">
          Password Protected Messages
        </div>
        <div class="navbar-end">
          <a class="btn btn-link normal-case" v-show="userToken">Profile</a>
          <a
            class="btn btn-link normal-case"
            v-show="userToken"
            @click.prevent="logout"
            >Logout</a
          >
          <a class="btn btn-secondary">Instructions</a>
        </div>
      </div>

      <!--  <RouterView />-->
      <!--      Main Content-->
      <div class="flex flex-col w-full border-opacity-50 my-auto mt-5">
        <div class="grid card bg-base-300 rounded-box place-items-center mb-2">
          <div class="stats shadow bg-base-300 mt-1">
            <div class="stat place-items-center">
              <div class="stat-title">Sent Messages</div>
              <div class="stat-value text-accent">31K</div>
            </div>

            <div class="stat place-items-center">
              <div class="stat-title">Read Messages</div>
              <div class="stat-value text-accent">4,200</div>
            </div>

            <div class="stat place-items-center">
              <div class="stat-title">Users</div>
              <div class="stat-value text-accent">1,200</div>
            </div>
          </div>
        </div>
      </div>
      <div class="grid card bg-base-300 place-items-center mt-2">
        <div class="tabs mt-2">
          <a
            class="tab tab-bordered"
            @click.prevent="tab = 'readMsg'"
            :class="{ 'tab-active': tab == 'readMsg' }"
            >Retrieve Message</a
          >
          <a
            class="tab tab-bordered"
            @click.prevent="tab = 'sendMsg'"
            :class="{ 'tab-active': tab == 'sendMsg' }"
            >Send Message</a
          >
          <a
            class="tab tab-bordered"
            v-if="!userToken"
            @click.prevent="tab = 'register'"
            :class="{ 'tab-active': tab === 'register' }"
            >Register</a
          >
        </div>
        <AppRetrieveMsg v-if="tab === 'readMsg'" />
        <AppLogin v-if="!userToken && tab == 'sendMsg'" />
        <AppSendMessage v-if="userToken && tab == 'sendMsg'" />
        <AppRegistration v-if="tab == 'register'" />
      </div>
      <footer
        class="footer items-center p-4 bg-neutral text-neutral-content mt-5 rounded-b-lg"
      >
        <div class="items-center grid-flow-col">
          <a href="https://joerismissaert.dev" target="_blank">
            <p>© 2022 - Joeri JM Smissaert</p>
          </a>
        </div>
        <div
          class="grid-flow-col gap-4 md:place-self-center md:justify-self-end"
        >
          <a href="https://github.com/smissaertj/secretly" target="_blank">
            <font-awesome-icon
              icon="fa-brands fa-square-github"
              class="fa-2xl"
            />
          </a>
        </div>
      </footer>
    </div>
  </div>
</template>
<script>
// import { RouterLink, RouterView } from "vue-router";
// import HelloWorld from "./components/HelloWorld.vue";

import AppRetrieveMsg from "@/components/AppRetrieveMsg.vue";
import AppLogin from "@/components/AppLogin.vue";
import AppRegistration from "@/components/AppRegistration.vue";
import AppSendMessage from "@/components/AppSendMessage.vue";
import { mapWritableState } from "pinia";
import { useUserStore } from "@/stores/userStore";

export default {
  name: "App",
  components: {
    AppRetrieveMsg,
    AppLogin,
    AppRegistration,
    AppSendMessage,
  },
  data() {
    return {
      tab: "readMsg",
    };
  },
  mounted() {
    const userStore = useUserStore();
    this.userToken =
      userStore.token !== "undefined" ? userStore.token : undefined;
  },
  computed: {
    ...mapWritableState(useUserStore, { userToken: "token" }),
  },
  methods: {
    logout() {
      this.userToken = undefined;
    },
  },
};
</script>
