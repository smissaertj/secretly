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
  <div
    class="alert alert-success shadow-lg w-1/2 mb-8 justify-center rounded"
    v-else-if="response.severity === 'success'"
  >
    <div>
      <span>{{ response.response_msg }}</span>
    </div>
  </div>
  <!--  On Error-->
  <div
    class="alert alert-error shadow-lg w-1/2 mb-8 justify-center rounded"
    v-else-if="response.severity === 'error'"
  >
    <div class="">
      <span>{{ response.response_msg }}</span>
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
      console.log(values);
      try {
        await axios
          .post("http://localhost:8080/api/read_message", {
            uuid: values.uuid,
            password: values.passwd,
          })
          .then((response) => {
            this.response = response.data;
          });
      } catch (error) {
        this.response = error.response.data;
      }
    },
  },
};
</script>

<!--TODO - Disable Form & display message when data is being retrieved-->
<!--TODO - Display error or message-->

<style scoped></style>
