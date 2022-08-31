<template>
  <vee-form
    class="form-control m-4"
    :validation-schema="retrieveMsgSchema"
    @submit="retrieveMsg"
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
</template>

<script>
export default {
  name: "AppRetrieveMsg",
  data() {
    return {
      retrieveMsgSchema: {
        uuid: "required",
        passwd: "required",
      },
    };
  },
  methods: {
    async retrieveMsg(values) {
      console.log(values);
    },
  },
};
</script>

<style scoped></style>
