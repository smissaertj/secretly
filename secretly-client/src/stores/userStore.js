import { defineStore } from "pinia";
import { useLocalStorage } from "@vueuse/core";

export const useUserStore = defineStore("userStore", {
  state: () => {
    return {
      token: useLocalStorage("secretlyUser"),
    };
  },
});
