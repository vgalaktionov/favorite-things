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
    <AddEditThing />
  </div>
</template>

<script>
import { mapState } from "vuex"
import Vue from "vue"
import Categories from "./Categories"
import Things from "./Things"
import AddEditThing from "./AddEditThing"

export default {
  name: "App",
  components: {
    Categories,
    Things,
    AddEditThing
  },
  created() {
    this.$store.dispatch("fetchCategories")
    this.$store.dispatch("fetchThings")
  }
}
</script>

<style>
</style>
