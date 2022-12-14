<template>
  <main>
    <div class="card">
      <h1 class="card__title" v-if="mode === 'login'">Login</h1>
      <h1 class="card__title" v-else>Registration</h1>
      <p class="card__subtitle" v-if="mode === 'login'">
        Not account yet ?
        <span class="card__action" @click="switchToRegister()"
          >Create account</span
        >
      </p>
      <p class="card__subtitle" v-else>
        Already registered ?
        <span class="card__action" @click="switchToLogin()">Log In</span>
      </p>
      <div class="form-row">
        <input
          v-model="username"
          class="form-row__input"
          type="text"
          placeholder="Username"
        />
      </div>
      <div class="form-row" v-if="mode === 'register'">
        <input
          v-model="email"
          class="form-row__input"
          type="text"
          placeholder="Email"
        />
      </div>
      <div class="form-row">
        <input
          v-model="password"
          class="form-row__input"
          type="password"
          placeholder="Password"
        />
      </div>
      <div class="form-row" v-if="mode === 'register'">
        <input
          v-model="password_confirm"
          class="form-row__input"
          type="password"
          placeholder="Confirm password"
        />
      </div>
      <div class="form-row" v-if="mode === 'login'">
        <button
          @click="login"
          @keyup.enter="login"
          class="button"
          :class="{ 'button--disable': !validatedForm }"
          :disabled="!validatedForm"
        >
          <span v-if="status === 'loading'">Log In...</span>
          <span v-else>Log In</span>
        </button>
      </div>
      <div class="form-row" v-else>
        <button
          @click="register"
          @keyup.enter="register"
          class="button"
          :class="{ 'button--disable': !validatedForm }"
          :disabled="!validatedForm"
        >
          <span v-if="status === 'loading'">Creation in progress...</span>
          <span v-else>Create account</span>
        </button>
      </div>
    </div>
  </main>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "LoginView",
  data: function () {
    return {
      mode: "login",
      email: "",
      username: "",
      password: "",
      password_confirm: "",
    };
  },
  mounted: function () {
    if (this.$store.state.user.id !== -1) {
      this.$router.push("/home");
    }
  },
  computed: {
    validatedForm: function () {
      if (this.mode === "register") {
        if (
          this.email.match(
            /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
          ) &&
          this.username !== "" &&
          this.password.match(
            /((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$/
          ) &&
          this.password === this.password_confirm
        ) {
          return true;
        } else {
          return false;
        }
      } else {
        const response = this.username !== "" && this.password !== "";
        return response;
      }
    },
    ...mapState(["status"]),
  },
  methods: {
    switchToRegister: function () {
      this.mode = "register";
    },
    switchToLogin: function () {
      this.mode = "login";
    },
    login: function () {
      const self = this;
      this.$store
        .dispatch("login", {
          username: this.username,
          password: this.password,
        })
        .then(
          function () {
            self.$router.push("home");
          },
          function (error) {
            console.log(error);
          }
        );
    },
    register: function () {
      const self = this;
      this.$store
        .dispatch("register", {
          username: this.username,
          email: this.email,
          password: this.password,
          password2: this.password_confirm,
        })
        .then(
          function () {
            self.login();
          },
          function (error) {
            console.log(error);
          }
        );
    },
  },
};
</script>

<style lang="scss" scoped>
@import "@/styles/_variables.scss";

main {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px;
}

.card {
  max-width: 100%;
  width: 540px;
  padding: 32px;
  background-color: white;
  border-radius: 16px;

  &__title {
    text-align: center;
    font-weight: 800;
  }

  &__subtitle {
    text-align: center;
    font-weight: 500;
    color: #666;
  }

  &__action {
    color: $tertiary-color;
    text-decoration: underline;

    &:hover {
      cursor: pointer;
    }
  }
}

.button {
  width: 100%;
}

.form-row {
  display: flex;
  margin: 16px 0;
  gap: 16px;
  flex-wrap: wrap;

  &__input {
    padding: 8px;
    border: none;
    border-radius: 8px;
    background: #f2f2f2;
    font-weight: 500;
    font-size: 16px;
    min-width: 90%;
    color: black;
    flex: 1;

    &::placeholder {
      color: #aaaaaa;
    }
  }
}
</style>
