<template>
  <vee-form
    class="form-control m-4 justify-center w-1/3"
    :validation-schema="sendMsgSchema"
    @submit="sendMsg"
    v-if="!response"
  >
    <vee-field
      name="destEmail"
      type="email"
      placeholder="Receiving Email Address"
      class="input input-bordered text-center m-2"
    />
    <ErrorMessage class="text-red-600" name="destEmail" />
    <vee-field
      name="messageTxt"
      type="txt"
      placeholder="Your message"
      class="input input-bordered text-center m-2"
    />
    <ErrorMessage class="text-red-600" name="messageTxt" />
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
      Send Message
    </button>
  </vee-form>

  <!--  On Success-->
  <template v-else-if="response.severity === 'success'">
    <div
      class="alert alert-success shadow-lg w-1/4 my-4 justify-center rounded"
    >
      <div class="flex flex-wrap justify-center">
        <div>
          <font-awesome-icon icon="fa-solid fa-check" class="mr-2 fa-2xl" />{{
            response.response_msg
          }}
        </div>
      </div>
    </div>
  </template>

  <!--  On Error-->
  <div
    class="alert alert-error shadow-lg w-1/2 my-4 justify-center rounded"
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
</template>

<script>
import axios from "axios";
import { mapState } from "pinia";
import { useUserStore } from "@/stores/userStore";
export default {
  name: "AppSendMessage",
  data() {
    return {
      sendMsgSchema: {
        destEmail: "required|email",
        messageTxt: "required",
        passwd: "required",
        confirmPasswd: "required|confirmed:@passwd",
      },
      response: "",
    };
  },
  computed: {
    ...mapState(useUserStore, { userToken: "token" }),
  },
  methods: {
    async sendMsg(values) {
      const token = this.userToken;
      const config = {
        headers: { Authorization: `Bearer ${token}` },
      };
      try {
        await axios
          .post(
            import.meta.env.VITE_API_URL + "/api/new_message",
            {
              message: values.messageTxt,
              to_email: values.destEmail,
              password: values.passwd,
            },
            config
          )
          .then((response) => {
            console.log(response.data);
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
