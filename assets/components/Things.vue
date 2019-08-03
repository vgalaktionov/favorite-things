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
      things: [],
      searchTerm: null
    }
  },
  async mounted() {
    try {
      const { data } = await api.get("/api/things/")
      this.things = data
    } catch (error) {
      console.error(error)
    }
  },
  computed: {
    filteredThings() {
      if (!this.searchTerm) return this.things
      const regex = new RegExp(this.searchTerm)
      return this.things.filter(({ title, description }) => {
        return regex.test(title) || regex.test(description)
      })
    }
  }
}
</script>

<style scoped>
</style>
