<template>
  <header>
    <nav>
      <button class="button" @click="logout()">Déconnexion</button>
    </nav>
  </header>
</template>

<script>
export default {
  name: "NavBar",
  methods: {
    logout: function () {
      const self = this;
      this.$store.commit("logout");
      self.$router.push("/");
    },
  },
};
</script>

<style lang="scss" scoped></style>
