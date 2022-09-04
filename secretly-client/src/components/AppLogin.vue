<template>
  <p class="text mt-2">Login To Send a Message</p>
  <vee-form
    class="form-control mb-4 justify-center w-1/3"
    :validation-schema="loginSchema"
    @submit="login"
    v-if="!loginAction && !userLoggedIn"
  >
    <vee-field
      name="email"
      type="email"
      placeholder="Email Address"
      class="input input-bordered text-center m-2"
    />
    <ErrorMessage class="text-red-600" name="email" />
    <vee-field
      name="passwd"
      type="password"
      placeholder="Password"
      class="input input-bordered text-center m-2"
    />
    <ErrorMessage class="text-red-600" name="passwd" />
    <button class="btn btn-accent btn-wide m-2 mx-auto" type="submit">
      Login
    </button>
  </vee-form>

  <!--  On LoginAction-->
  <div
    class="alert alert-info shadow-lg w-1/3 mb-8 justify-center rounded"
    v-else-if="loginAction"
  >
    <div>
      <span
        ><font-awesome-icon icon="fa-solid fa-spinner" class="mr-2 fa-2xl" />
        Logging in...</span
      >
    </div>
  </div>
  <!--  On Success-->
  <div
    class="alert alert-success shadow-lg w-1/3 mb-8 justify-center rounded"
    v-if="severity === 'success' && !loginAction"
  >
    <div>
      <span
        ><font-awesome-icon icon="fa-solid fa-check" class="mr-2 fa-2xl" />
        {{ response_msg }}</span
      >
    </div>
  </div>

  <!--  On Error-->
  <div
    class="alert alert-error shadow-lg w-1/2 mb-8 justify-center rounded"
    v-else-if="severity === 'error' && !loginAction"
  >
    <div>
      <span
        ><font-awesome-icon
          icon="fa-solid fa-circle-exclamation"
          class="mr-2 fa-2xl"
        />
        {{ response_msg }}</span
      >
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapState, mapActions } from "pinia/dist/pinia";
import { useUserStore } from "@/stores/userStore";

export default {
  name: "AppLogin",
  data() {
    return {
      loginSchema: {
        email: "required|email",
        passwd: "required",
      },
      response: "",
      loginAction: false,
    };
  },
  computed: {
    ...mapState(useUserStore, {
      userLoggedIn: "userLoggedIn",
      response_msg: "response_msg",
      severity: "severity",
    }),
  },
  methods: {
    ...mapActions(useUserStore, ["authenticate"]),

    async login(values) {
      this.loginAction = true;
      await this.authenticate(values);
      this.loginAction = false;
    },
  },
};
</script>
