<template>
  <vee-form
    class="form-control m-4"
    :validation-schema="retrieveMsgSchema"
    @submit="retrieveMsg"
    v-if="!response"
  >
    <vee-field
      name="uuid"
      type="text"
      placeholder="Unique Identifier"
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
    <button class="btn btn-wide m-2" type="submit">Get Message</button>
  </vee-form>

  <!--  On Success-->
  <template v-else-if="response.severity === 'success'">
    <div
      class="alert alert-success shadow-lg w-1/4 mb-8 justify-center rounded"
    >
      <div class="flex flex-wrap justify-center">
        <div>Message decrypted successfully!</div>
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
    class="alert alert-error shadow-lg w-1/2 mb-8 justify-center rounded"
    v-else-if="response.severity === 'error'"
  >
    <div>
      <span>Error! {{ response.response_msg }}</span>
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
    };
  },
  methods: {
    async retrieveMsg(values) {
      try {
        await axios
          .post("http://localhost:8080/api/read_message", {
            uuid: values.uuid,
            password: values.passwd,
          })
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
