<template>
  <div class="card">
    <header class="card-header">
      <p class="card-header-title">{{ thingData.title }}</p>
      <span class="tag is-pulled-right is-info">{{ thingData.category_string }}</span>
    </header>
    <div class="card-content">
      <div class="content">
        <p>{{ thingData.description }}</p>
        <strong>Metadata:</strong>
        <em>
          <dl v-if="thingData.metadata">
            <span v-for="(value, key) in JSON.parse(thingData.metadata)" :key="key">
              <dt>{{ key }}:</dt>
              <dd>{{ value }}</dd>
            </span>
          </dl>
        </em>
        <div class="is-clearfix"></div>
        <br />
        <strong>Created:</strong>
        <time>{{ new Date(thingData.created_date).toLocaleString() }}</time>
        &nbsp;&nbsp;&nbsp;
        <strong>Modified:</strong>
        <time>{{ new Date(thingData.modified_date).toLocaleString() }}</time>
      </div>
    </div>
    <footer class="card-footer">
      <a class="card-footer-item" @click="() => edit(thingData.id)">
        Edit
        <span class="icon is-right">
          <i class="fas fa-edit"></i>
        </span>
      </a>
      <a class="card-footer-item has-text-danger" @click="() => remove(thingData.id)">
        Delete
        <span class="icon is-right">
          <i class="fas fa-times"></i>
        </span>
      </a>
    </footer>
  </div>
</template>

<script>
import AddEditThing from "./AddEditThing"
import api from "../api"

export default {
  props: ["thingData"],
  methods: {
    edit(id) {
      this.$store.commit("setShowModal", { show: true, editing: id })
    },
    async remove(id) {
      try {
        await api.delete(`/api/things/${id}/`)
        this.$store.dispatch("fetchThings")
      } catch (error) {
        console.error(error)
      }
    }
  }
}
</script>

<style scoped>
.tag {
  margin-top: 1rem;
  margin-right: 1rem;
}

dt,
dd {
  float: left;
}
dt {
  clear: both;
}

.card {
  margin-bottom: 1rem;
}
</style>
