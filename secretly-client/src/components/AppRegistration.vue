<template>
  <p class="text mt-2">Create Account</p>
  <vee-form
    class="form-control mb-4 justify-center w-1/3"
    :validation-schema="registerSchema"
    @submit="register"
    v-if="!response && !registerAction"
  >
    <vee-field
      name="email"
      type="email"
      placeholder="Email Address"
      class="input input-bordered text-center m-2"
    />
    <ErrorMessage class="text-red-600" name="email" />
    <vee-field
      name="firstName"
      type="text"
      placeholder="First Name"
      class="input input-bordered text-center m-2"
    />
    <ErrorMessage class="text-red-600" name="firstName" />
    <vee-field
      name="lastName"
      type="text"
      placeholder="Last Name"
      class="input input-bordered text-center m-2"
    />
    <vee-field
      name="passwd"
      type="password"
      placeholder="Password"
      class="input input-bordered text-center m-2"
    />
    <ErrorMessage class="text-red-600" name="passwd" />
    <vee-field
      name="confirmPasswd"
      type="password"
      placeholder="Confirm Password"
      class="input input-bordered text-center m-2"
    />
    <ErrorMessage class="text-red-600" name="confirmPasswd" />
    <button class="btn btn-accent btn-wide m-2 mx-auto" type="submit">
      Register
    </button>
  </vee-form>

  <!--  On registerAction-->
  <div
    class="alert alert-info shadow-lg w-1/3 mb-8 justify-center rounded"
    v-else-if="registerAction"
  >
    <div>
      <span
        ><font-awesome-icon icon="fa-solid fa-spinner" class="mr-2 fa-2xl" />
        Creating Account...</span
      >
    </div>
  </div>

  <!--  On Success-->
  <div
    class="alert alert-success shadow-lg w-1/2 mb-8 justify-center rounded"
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
  name: "AppRegistration",
  data() {
    return {
      registerSchema: {
        email: "required|email",
        firstName: "required",
        lastName: "required",
        passwd: "required",
        confirmPasswd: "required|confirmed:@passwd",
      },
      response: "",
      registerAction: false,
    };
  },
  methods: {
    async register(values) {
      // console.log(values);

      try {
        this.registerAction = true;
        const response = await axios.post(
          import.meta.env.VITE_API_URL + "/api/signup",
          {
            email: values.email,
            first_name: values.firstName,
            last_name: values.lastName,
            password: values.passwd,
          }
        );
        this.registerAction = false;
        this.response = response.data;
        setTimeout(() => window.location.reload(), 3000);
      } catch (error) {
        // console.log(error);
        this.registerAction = false;
        this.response = error.response.data;
      }
    },
  },
};
</script>

// yzuzPywSuqcJhYD2 // // dPxXg8RndDv3b0kJ
