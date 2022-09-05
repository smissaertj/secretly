import { defineStore } from "pinia";
import axios from "axios";

export const useStatStore = defineStore("statStore", {
  state: () => {
    return {
      sentMessages: 0,
      readMessages: 0,
      users: 0,
    };
  },
  actions: {
    async updateStats() {
      try {
        const response = await axios.get(
          import.meta.env.VITE_API_URL + "/api/update_stats"
        );
        console.log(response.data);
        this.sentMessages = response.data.sentMessages;
        this.readMessages = response.data.readMessages;
        this.users = response.data.users;
      } catch (error) {
        console.log(error);
      }
    },
  },
});
