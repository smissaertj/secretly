<template>
  <div class="flex flex-col w-full border-opacity-50 my-auto mt-5">
    <div class="grid card bg-base-300 rounded-box place-items-center mb-2">
      <div class="stats shadow bg-base-300 mt-1">
        <div class="stat place-items-center">
          <div class="stat-title">Sent Messages</div>
          <div class="stat-value text-accent">{{ sentMessages }}</div>
        </div>

        <div class="stat place-items-center">
          <div class="stat-title">Read Messages</div>
          <div class="stat-value text-accent">{{ readMessages }}</div>
        </div>

        <div class="stat place-items-center">
          <div class="stat-title">Users</div>
          <div class="stat-value text-accent">{{ users }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from "pinia";
import { useStatStore } from "@/stores/statStore.js";
export default {
  name: "AppStats",
  computed: {
    ...mapActions(useStatStore, ["updateStats"]),
    ...mapState(useStatStore, {
      sentMessages: "sentMessages",
      readMessages: "readMessages",
      users: "users",
    }),
  },
  mounted() {
    this.updateStats;
  },
};
</script>

<style scoped></style>
