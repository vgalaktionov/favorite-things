<template>
  <div>
    <div class="field">
      <p class="control has-icons-right">
        <input
          class="input is-info is-large"
          type="text"
          placeholder="Search..."
          v-model="searchTerm"
        />
        <span class="icon is-small is-right">
          <i class="fas fa-search"></i>
        </span>
      </p>
    </div>
    <Thing v-for="thing in filteredThings" :key="thing.id" :thing-data="thing" />
  </div>
</template>

<script>
import api from "../api"
import Thing from "./Thing"

export default {
  components: { Thing },
  data() {
    return {
      searchTerm: null
    }
  },
  computed: {
    things() {
      return this.$store.state.things || []
    },
    selectedCategories() {
      return this.$store.getters.selectedCategories || []
    },
    filteredThings() {
      let filtered = this.things
      if (this.selectedCategories.length) {
        filtered = filtered.filter(({ category }) =>
          this.selectedCategories.includes(category)
        )
      }
      if (this.searchTerm) {
        const regex = new RegExp(this.searchTerm)
        filtered = filtered.filter(({ title, description }) => {
          return regex.test(title) || regex.test(description)
        })
      }
      return filtered
    }
  }
}
</script>

<style scoped>
</style>
