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
          @keyup.enter="add"
        />
      </div>
      <p class="help">Press Enter to add the category</p>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex"
import api from "../api"

export default {
  data() {
    return {
      newCategory: null
    }
  },
  computed: {
    categories() {
      return this.$store.state.categories || []
    }
  },
  methods: {
    ...mapActions(["addNewCategory", "removeCategory"]),
    add() {
      this.addNewCategory(this.newCategory)
      this.newCategory = null
    }
  }
}
</script>
