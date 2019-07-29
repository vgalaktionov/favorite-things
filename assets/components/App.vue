<template>
  <div class="container">Hello {{ bundler }}</div>
</template>

<script>
import Vue from "vue"

export default {
  data() {
    return {
      bundler: "Parcel"
    }
  }
}
</script>

<style>
.container {
  color: green;
}
</style>
