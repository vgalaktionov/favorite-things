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
          @keyup.enter="() => addNewCategory(newCategory)"
        />
      </div>
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
    ...mapActions(["addNewCategory", "removeCategory"])
  }
}
</script>
