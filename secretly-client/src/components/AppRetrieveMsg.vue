<template>
  <vee-form
    class="form-control m-4 justify-center w-1/3"
    :validation-schema="retrieveMsgSchema"
    @submit="retrieveMsg"
    v-if="!response && !retrieveMsgAction"
  >
    <vee-field
      name="uuid"
      type="text"
      placeholder="Message Unique Identifier"
      class="input input-bordered text-center m-2"
    />
    <ErrorMessage class="text-red-600" name="uuid" />
    <vee-field
      name="passwd"
      type="password"
      placeholder="Password"
      class="input input-bordered text-center m-2"
    />
    <ErrorMessage class="text-red-600" name="passwd" />
    <button class="btn btn-accent btn-wide m-2 mx-auto" type="submit">
      Get Message
    </button>
  </vee-form>

  <!--  On retrieveMsgAction-->
  <div
    class="alert alert-info shadow-lg w-1/3 my-4 justify-center rounded"
    v-else-if="retrieveMsgAction"
  >
    <div>
      <span
        ><font-awesome-icon icon="fa-solid fa-spinner" class="mr-2 fa-2xl" />
        Fetching Message...</span
      >
    </div>
  </div>

  <!--  On Success-->
  <template v-else-if="response.severity === 'success'">
    <div
      class="alert alert-success shadow-lg w-1/3 my-4 justify-center rounded"
    >
      <div class="flex flex-wrap justify-center">
        <div>
          <font-awesome-icon
            icon="fa-solid fa-check"
            class="mr-2 fa-2xl"
          />Message decrypted!
        </div>
      </div>
    </div>
    <div class="card w-1/2 bg-base-200 shadow-xl text-center mb-8">
      <div class="card-body">
        <p class="text-lg">{{ response.response_msg }}</p>
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

export default {
  name: "AppRetrieveMsg",
  data() {
    return {
      retrieveMsgSchema: {
        uuid: "required",
        passwd: "required",
      },
      response: "",
      retrieveMsgAction: false,
    };
  },
  methods: {
    async retrieveMsg(values) {
      try {
        this.retrieveMsgAction = true;
        await axios
          .post(import.meta.env.VITE_API_URL + "/api/read_message", {
            uuid: values.uuid,
            password: values.passwd,
          })
          .then((response) => {
            // console.log(response.data);
            this.retrieveMsgAction = false;
            this.response = response.data;
          });
      } catch (error) {
        this.retrieveMsgAction = false;
        this.response = error.response.data;
        setTimeout(() => window.location.reload(), 3000);
      }
    },
  },
};
</script>
