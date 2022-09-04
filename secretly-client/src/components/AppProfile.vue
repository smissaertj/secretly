<template>
  <p class="text mt-2">Edit Profile</p>
  <vee-form
    class="form-control mb-4 justify-center w-1/3"
    :validation-schema="editProfileSchema"
    @submit="editProfile"
    v-if="!updateProfileAction"
  >
    <vee-field
      name="email"
      type="email"
      v-model="email"
      class="input input-bordered text-center m-2"
    />
    <ErrorMessage class="text-red-600" name="email" />
    <vee-field
      name="firstName"
      type="text"
      placeholder="First Name"
      v-model="firstName"
      class="input input-bordered text-center m-2"
    />
    <ErrorMessage class="text-red-600" name="firstName" />
    <vee-field
      name="lastName"
      type="text"
      placeholder="Last Name"
      v-model="lastName"
      class="input input-bordered text-center m-2"
    />
    <ErrorMessage class="text-red-600" name="lastName" />
    <button class="btn btn-accent btn-wide m-2 mx-auto" type="submit">
      Submit Changes
    </button>
  </vee-form>

  <!--  On Success-->
  <div
    class="alert alert-success shadow-lg w-1/2 mb-8 justify-center rounded"
    v-if="severity === 'success'"
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
    v-if="severity === 'error'"
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
  <div
    class="alert alert-info shadow-lg w-1/3 mb-8 justify-center rounded"
    v-if="updateProfileAction"
  >
    <div>
      <span
        ><font-awesome-icon icon="fa-solid fa-spinner" class="mr-2 fa-2xl" />
        Updating Profile...</span
      >
    </div>
  </div>
  <div class="overflow-x-auto my-4" v-if="userMessages.length > 0">
    <table class="table table-compact w-full">
      <thead>
        <tr>
          <th>UUID</th>
          <th>Destination</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(message, index) in userMessages">
          <td>{{ message.uuid }}</td>
          <td>{{ message.to_email }}</td>
          <td>{{ message.is_read ? "Read" : "Unread" }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";
import { mapState, mapWritableState, mapActions } from "pinia";
import { useUserStore } from "@/stores/userStore";

export default {
  name: "AppProfile.vue",
  data() {
    return {
      editProfileSchema: {
        email: "required|email",
        firstName: "required",
        lastName: "required",
      },
      updateProfileAction: false,
      userMessages: [],
    };
  },
  computed: {
    ...mapState(useUserStore, {
      userToken: "token",
      email: "userEmail",
      firstName: "userFirstName",
      lastName: "userLastName",
      response_msg: "response_msg",
      severity: "severity",
    }),
    ...mapWritableState(useUserStore, {
      email: "userEmail",
      firstName: "userFirstName",
      lastName: "userLastName",
      severity: "severity",
    }),
  },
  methods: {
    ...mapActions(useUserStore, ["updateProfile"]),
    async editProfile(values) {
      this.updateProfileAction = true;
      await this.updateProfile(values);
      this.updateProfileAction = false;
    },
  },
  mounted: function () {
    this.severity = "";
    const config = {
      headers: { Authorization: `Bearer ${this.userToken}` },
    };
    try {
      const response = axios
        .get(
          import.meta.env.VITE_API_URL + "/api/user_profile/messages",
          config
        )
        .then((response) => {
          console.log(response);
          this.userMessages = response.data.user_messages;
          console.log(this.userMessages);
        });
    } catch (error) {
      console.log(error);
    }
  },
};
</script>

<style scoped></style>
