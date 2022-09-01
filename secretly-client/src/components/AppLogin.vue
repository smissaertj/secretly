<template>
  <p class="text-2xl m-4">Login To Send a Message</p>
  <vee-form
    class="form-control m-4 justify-center"
    :validation-schema="loginSchema"
    @submit="login"
    v-if="!response"
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
    <button class="btn btn-accent btn-wide m-2" type="submit">Login</button>
  </vee-form>

  <!--  On Success-->
  <div
    class="alert alert-success shadow-lg w-1/3 mb-8 justify-center rounded"
    v-else-if="response.severity === 'success'"
  >
    <div>
      <span
        ><font-awesome-icon icon="fa-solid fa-check" class="mr-2 fa-2xl" />
        {{ response.response_msg }}</span
      >
    </div>
  </div>

  <!--  On Error-->
  <div
    class="alert alert-error shadow-lg w-1/2 mb-8 justify-center rounded"
    v-else-if="response.severity === 'error'"
  >
    <div>
      <span
        ><font-awesome-icon
          icon="fa-solid fa-circle-exclamation"
          class="mr-2 fa-2xl"
        />
        Error! {{ response.response_msg }}</span
      >
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AppLogin",
  data() {
    return {
      loginSchema: {
        email: "required|email",
        passwd: "required",
      },
      response: "",
    };
  },
  methods: {
    async login(values) {
      console.log(values);
      try {
        const response = await axios.post(
          import.meta.env.VITE_API_URL + "/api/login",
          {
            email: values.email,
            password: values.passwd,
          }
        );
        const token = response.data["token"];
        this.response = response.data;
        localStorage.setItem("secretlyUser", token);
        setTimeout(function () {
          location.reload();
        }, 1000);
      } catch (error) {
        console.log(error);
        this.response = error.response.data;
      }
    },
  },
};
</script>
