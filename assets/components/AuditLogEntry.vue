<template>
  <div class="box">
    <table class="log-meta">
      <tr>
        <td>Action:</td>
        <td>
          <span class="tag is-light">{{ logEntry.action }}</span>
        </td>
      </tr>
      <tr>
        <td>Timestamp:</td>
        <td>{{ new Date(logEntry.timestamp).toLocaleString() }}</td>
      </tr>
    </table>
    <table>
      <thead>
        <tr>
          <th>Field</th>
          <th>Before</th>
          <th>After</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(value, key) in logEntry.changes" :key="key">
          <td>{{ key }}</td>
          <td>
            <pre class="has-text-danger">{{ value[0] }}</pre>
          </td>
          <td>
            <pre class="has-text-success">{{ value[1] }}</pre>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: ["logEntry"]
}
</script>

<style scoped>
table.log-meta tr,
table.log-meta td {
  border: 0px solid white;
}

table.log-meta tr td:first-child {
  font-weight: bold;
}
</style>
