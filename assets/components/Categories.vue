<template>
  <div class="has-text-centered">
    <h4 class="is-size-4">Categories</h4>
    <br />
    <div class="field" v-for="category in categories" :key="category.id">
      <div class="control">
        <label class="checkbox">
          <input type="checkbox" v-model="category.selected" />
          {{ category.name }}
          <a
            class="delete"
            v-if="category.user"
            @click.prevent="() => removeCategory(category.id)"
          ></a>
        </label>
      </div>
    </div>
    <div class="field">
      <div class="control">
        <input
          class="input is-primary"
          type="text"
          placeholder="Add new categories..."
          v-model="newCategory"
          @keyup.enter="addNewCategory"
        />
      </div>
    </div>
  </div>
</template>

<script>
import api from "../api"

export default {
  data() {
    return {
      categories: [],
      newCategory: null
    }
  },
  async mounted() {
    try {
      const { data } = await api.get("/api/categories/")
      this.categories = data
    } catch (error) {
      console.error(error)
    }
  },
  methods: {
    async addNewCategory() {
      try {
        await api.post("/api/categories/", { name: this.newCategory })
        this.categories.push({ name: this.newCategory, user: window.userID })
        this.newCategory = null
      } catch (error) {
        console.error(error)
      }
    },
    async removeCategory(idToRemove) {
      try {
        await api.delete(`/api/categories/${idToRemove}/`)
        this.categories = this.categories.filter(({ id }) => id !== idToRemove)
      } catch (error) {
        console.error(error)
      }
    }
  }
}
</script>
