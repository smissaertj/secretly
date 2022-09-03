<template>
  <p class="text mt-2">Edit Profile</p>
  <vee-form
    class="form-control mb-4 justify-center w-1/3"
    :validation-schema="editProfileSchema"
    @submit="editProfile"
    v-if="response.severity === 'success'"
  >
    <vee-field
      name="email"
      type="email"
      v-model="response.email"
      class="input input-bordered text-center m-2"
    />
    <ErrorMessage class="text-red-600" name="email" />
    <vee-field
      name="firstName"
      type="text"
      placeholder="First Name"
      v-model="response.first_name"
      class="input input-bordered text-center m-2"
    />
    <ErrorMessage class="text-red-600" name="firstName" />
    <vee-field
      name="lastName"
      type="text"
      placeholder="Last Name"
      v-model="response.last_name"
      class="input input-bordered text-center m-2"
    />
    <ErrorMessage class="text-red-600" name="lastName" />
    <vee-field
      name="passwd"
      type="password"
      placeholder="New Password (optional)"
      class="input input-bordered text-center m-2"
    />
    <ErrorMessage class="text-red-600" name="passwd" />
    <vee-field
      name="confirmPasswd"
      type="password"
      placeholder="Confirm New Password (optional)"
      class="input input-bordered text-center m-2"
    />
    <ErrorMessage class="text-red-600" name="confirmPasswd" />
    <button class="btn btn-accent btn-wide m-2 mx-auto" type="submit">
      Submit Changes
    </button>
  </vee-form>

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
        {{ response.response_msg }}</span
      >
    </div>
  </div>
  <div
    class="alert alert-info shadow-lg w-1/2 mb-8 justify-center rounded"
    v-else
  >
    <div>
      <span
        ><font-awesome-icon icon="fa-solid fa-spinner" class="mr-2 fa-2xl" />
        Loading Data...</span
      >
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapState } from "pinia";
import { useUserStore } from "@/stores/userStore";

export default {
  name: "AppProfile.vue",
  data() {
    return {
      editProfileSchema: {
        email: "required|email",
        firstName: "required",
        lastName: "required",
        confirmPasswd: "confirmed:@passwd",
      },
      response: "",
    };
  },
  computed: {
    ...mapState(useUserStore, { userToken: "token" }),
  },
  created: function () {
    const token = this.userToken;
    const config = {
      headers: { Authorization: `Bearer ${token}` },
    };
    try {
      axios
        .get(import.meta.env.VITE_API_URL + "/api/user_profile", config)
        .then((response) => {
          // console.log(response.data);
          this.response = response.data;
        });
    } catch (error) {
      console.log(error);
    }
  },
  methods: {
    async editProfile(values) {
      const token = this.userToken;
      const config = {
        headers: { Authorization: `Bearer ${token}` },
      };
      try {
        await axios
          .post(
            import.meta.env.VITE_API_URL + "/api/user_profile",
            {
              email: values.email,
              first_name: values.firstName,
              last_name: values.lastName,
              password: values.passwd,
            },
            config
          )
          .then((response) => {
            // console.log(response.data);
            this.response = response.data;
          });
      } catch (error) {
        this.response = error.response.data;
      }
    },
  },
};
</script>

<style scoped></style>
