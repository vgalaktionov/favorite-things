<template>
  <div class="columns">
    <div class="column is-3">
      <div class="box">
        <Categories />
      </div>
    </div>
    <div class="column">
      <Things />
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex"
import Vue from "vue"
import Categories from "./Categories"
import Things from "./Things"

export default {
  components: {
    Categories,
    Things
  },
  created() {
    this.$store.dispatch("initialFetch")
    this.$forceUpdate()
  }
}
</script>

<style>
</style>
