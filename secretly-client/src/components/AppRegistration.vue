<template>
  <p class="text mt-2">Create Account</p>
  <vee-form
    class="form-control mb-4 justify-center w-1/3"
    :validation-schema="registerSchema"
    @submit="register"
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
export default {
  name: "AppRegistration",
  data() {
    return {
      registerSchema: {
        email: "required|email",
        passwd: "required",
        confirmPasswd: "required",
      },
    };
  },
  methods: {
    register(values) {
      console.log(values);
    },
  },
};
</script>
