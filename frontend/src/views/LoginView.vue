<template>
  <div class="card">
    <h1 class="card__title" v-if="mode === 'login'">Connexion</h1>
    <h1 class="card__title" v-else>Inscription</h1>
    <p class="card__subtitle" v-if="mode === 'login'">
      Pas encore de compte ?
      <span class="card__action" @click="switchToRegister()"
        >Créer un compte</span
      >
    </p>
    <p class="card__subtitle" v-else>
      Dejà inscrit ?
      <span class="card__action" @click="switchToLogin()">Se connecter</span>
    </p>
    <div class="form-row">
      <input
        v-model="username"
        class="form-row__input"
        type="text"
        placeholder="Nom d'utilisateur"
      />
    </div>
    <div class="form-row" v-if="mode === 'register'">
      <input
        v-model="email"
        class="form-row__input"
        type="text"
        placeholder="Adresse mail"
      />
    </div>
    <div class="form-row">
      <input
        v-model="password"
        class="form-row__input"
        type="password"
        placeholder="Mot de passe"
      />
    </div>
    <div class="form-row" v-if="mode === 'register'">
      <input
        v-model="password_confirm"
        class="form-row__input"
        type="password"
        placeholder="Confirmer mot de passe"
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
        <span v-if="status === 'loading'">Connexion en cours...</span>
        <span v-else>Connexion</span>
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
        <span v-if="status === 'loading'">Création en cours...</span>
        <span v-else>Créer mon compte</span>
      </button>
    </div>
  </div>
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
    console.log(this.$store.state.user);
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
      this.$store
        .dispatch("register", {
          username: this.username,
          email: this.email,
          password: this.password,
          password2: this.password_confirm,
        })
        .then(
          function (response) {
            console.log(response);
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
    min-width: 100%;
    color: black;
    flex: 1;

    &::placeholder {
      color: #aaaaaa;
    }
  }
}
</style>
