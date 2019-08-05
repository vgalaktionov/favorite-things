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
          <table class="metadata" v-if="thingData.metadata">
            <tr v-for="(value, key) in JSON.parse(thingData.metadata)" :key="key">
              <td>{{ key }}:</td>
              <td>{{ value }}</td>
            </tr>
          </table>
        </em>
        <div class="is-clearfix"></div>
        <br />
        <details>
          <summary>
            <strong>Audit Log</strong>
          </summary>
          <br />
          <AuditLogEntry v-for="log in thingData.audit_log" :key="log.timestamp" :log-entry="log" />
        </details>
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
import AuditLogEntry from "./AuditLogEntry"

import api from "../api"

export default {
  props: ["thingData"],
  components: {
    AuditLogEntry
  },
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

table.metadata tr td {
  font-style: italic;
  border: 0px solid white;
}

.card {
  margin-bottom: 1rem;
}
</style>
