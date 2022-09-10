<template>
  <div @click="logout" class="button">Déconnexion</div>
</template>

<script>
export default {
  name: "HomeView",
  methods: {
    logout: function () {
      const self = this;
      this.$store.commit("logout");
      self.$router.push("/");
    },
  },
};
</script>
