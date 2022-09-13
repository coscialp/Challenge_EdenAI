<template>
  <router-view></router-view>
</template>

<style lang="scss">
@import "styles/variables";
* {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  margin: 0;
  padding: 0;
}

body {
  min-height: 100vh;
  background-image: $background-color;
}

.button {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  padding: 16px;
  border: none;
  border-radius: 8px;
  background: $primary-color;
  color: white;
  font-weight: 800;
  font-size: 16px;
  transition: all 0.4s;

  &:hover {
    cursor: pointer;
    background: $secondary-color;
  }

  &--disable {
    background: $button-background-color--disable;
    color: $button-color--disable;

    &:hover {
      cursor: not-allowed;
      background: $button-background-color--disable;
    }
  }
}
</style>
