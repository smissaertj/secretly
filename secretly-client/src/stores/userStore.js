import { defineStore } from "pinia";
import { useLocalStorage } from "@vueuse/core";
import axios from "axios";

export const useUserStore = defineStore("userStore", {
  state: () => {
    return {
      token: useLocalStorage("secretlyUser"),
      userLoggedIn: false,
      userData: undefined,
      response_msg: undefined,
      severity: undefined,
    };
    // getters: {
    //   getUser(state) {
    //     return state;
    //   },
  },
  actions: {
    async authenticate(values) {
      console.log(values);
      try {
        const login_response = await axios.post(
          import.meta.env.VITE_API_URL + "/api/login",
          {
            email: values.email,
            password: values.passwd,
          }
        );
        this.userData = login_response.data.user_data;
        localStorage.setItem("secretlyUser", login_response.data.token);
        this.response_msg = login_response.data.response_msg;
        this.severity = login_response.data.severity;
        this.userLoggedIn = true;
        setTimeout(() => window.location.reload(), 1000);
      } catch (error) {
        this.userLoggedIn = false;
        this.response_msg = error.response.data.response_msg;
        this.severity = error.response.data.severity;
      }
    },
  },
});
