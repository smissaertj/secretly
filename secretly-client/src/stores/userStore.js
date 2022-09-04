import { defineStore } from "pinia";
import { useLocalStorage } from "@vueuse/core";
import axios from "axios";

export const useUserStore = defineStore("userStore", {
  state: () => {
    return {
      token: useLocalStorage("secretlyUserToken"),
      userEmail: useLocalStorage("secretlyUserEmail"),
      userFirstName: useLocalStorage("secretlyUserFirstName"),
      userLastName: useLocalStorage("secretlyUserLastName"),

      response_msg: undefined,
      severity: undefined,
      userLoggedIn: false,
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
        const response = await axios.post(
          import.meta.env.VITE_API_URL + "/api/login",
          {
            email: values.email,
            password: values.passwd,
          }
        );
        localStorage.setItem("secretlyUserToken", response.data.token);
        localStorage.setItem("secretlyUserEmail", response.data.email);
        localStorage.setItem("secretlyUserFirstName", response.data.first_name);
        localStorage.setItem("secretlyUserLastName", response.data.last_name);
        this.response_msg = response.data.response_msg;
        this.severity = response.data.severity;
        this.userLoggedIn = true;
        setTimeout(() => window.location.reload(), 1000);
      } catch (error) {
        this.userLoggedIn = false;
        this.response_msg = error.response.data.response_msg;
        this.severity = error.response.data.severity;
      }
    },
    async updateProfile(values) {
      console.log(values);
      const config = {
        headers: { Authorization: `Bearer ${this.token}` },
      };
      try {
        const response = await axios.post(
          import.meta.env.VITE_API_URL + "/api/user_profile",
          {
            email: values.email,
            first_name: values.firstName,
            last_name: values.lastName,
            password: values.passwd,
          },
          config
        );
        this.userEmail = values.email;
        this.userFirstName = values.firstName;
        this.lastName = values.lastName;
        this.response_msg = response.data.response_msg;
        this.severity = response.data.severity;
      } catch (error) {
        this.response_msg = error.response.data.response_msg;
        this.severity = error.response.data.severity;
      }
    },
  },
});
