import { createStore } from "vuex";

import axios from "axios";

const BASE_URL = "http://localhost:8000";

const instance = axios.create({
  baseURL: BASE_URL,
});

let user = localStorage.getItem("user");
if (!user) {
  user = {
    id: -1,
    username: "",
    email: "",
    token: "",
  };
} else {
  try {
    user = JSON.parse(user);
    instance.defaults.headers.common["Authorization"] = `Bearer ${user.token}`;
  } catch (ex) {
    user = {
      id: -1,
      username: "",
      email: "",
      token: "",
    };
  }
}

export default createStore({
  state: {
    status: "",
    user: user,
    files: [],
    displayFiles: [],
  },
  getters: {},
  mutations: {
    setStatus: function (state, status) {
      state.status = status;
    },
    logUser: function (state, access_token) {
      let user = {
        id: -1,
        username: "",
        email: "",
        token: access_token,
      };

      instance.defaults.headers.common[
        "Authorization"
      ] = `Bearer ${user.token}`;

      instance.get("/api/users/me").then(function (response) {
        user.id = response.data.id;
        user.username = response.data.username;
        user.email = response.data.email;
        state.user = user;
        localStorage.setItem("user", JSON.stringify(state.user));
      });

      state.user = user;
    },
    logout: function (state) {
      state.user = {
        id: -1,
        username: "",
        email: "",
        token: "",
      };
      localStorage.removeItem("user");
    },
    setCurrentFiles: function (state) {
      instance.get("/api/files/").then(function (response) {
        state.files = response.data;
        state.displayFiles = response.data.reverse();
      });
    },
    sortByAdded: function (state) {
      state.displayFiles = state.displayFiles.sort((a, b) => {
        return b.since_added.localeCompare(a.since_added);
      });
    },
    reverseSortByAdded: function (state) {
      state.displayFiles = state.displayFiles.sort((a, b) => {
        return a.since_added.localeCompare(b.since_added);
      });
    },
  },
  actions: {
    login({ commit }, userInfos) {
      commit("setStatus", "loading");
      return new Promise((resolve, reject) => {
        instance
          .post(`${BASE_URL}/api/login/`, userInfos)
          .then(function (response) {
            commit("setStatus", "logged");
            commit("logUser", response.data.access);
            resolve(response);
          })
          .catch(function (error) {
            commit("setStatus", "error_login");
            reject(error);
          });
      });
    },
    register({ commit }, userInfos) {
      commit("setStatus", "loading");
      return new Promise((resolve, reject) => {
        axios
          .post(`${BASE_URL}/api/register/`, userInfos)
          .then(function (response) {
            commit("setStatus", "created");
            resolve(response);
          })
          .catch(function (error) {
            commit("setStatus", "error_create");
            reject(error);
          });
      });
    },
    submitFile({ commit }, formData) {
      commit("setStatus", "file_uploaded");
      return new Promise((resolve, reject) => {
        instance
          .post("/api/files/", formData, {
            headers: {
              "Content-Type": "multipart/data-form",
            },
          })
          .then(function (response) {
            commit("setCurrentFiles");
            resolve(response);
          })
          .catch(function (error) {
            commit("setStatus", "error_upload");
            reject(error);
          });
      });
    },
    getFiles() {
      return new Promise((resolve, reject) => {
        instance
          .get("/api/files/")
          .then(function (response) {
            resolve(response);
          })
          .catch(function (error) {
            reject(error);
          });
      });
    },
  },
  modules: {},
});
