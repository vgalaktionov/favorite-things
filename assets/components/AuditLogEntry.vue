<template>
  <div class="box">
    <table>
      <thead>
        <tr>
          <td>Change no.</td>
          <td>Action</td>
          <td>Timestamp</td>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>{{ index }}</td>
          <td>
            <span class="tag is-light">{{ logEntry.action }}</span>
          </td>
          <td>{{ new Date(logEntry.timestamp).toLocaleString() }}</td>
        </tr>
      </tbody>
    </table>
    <table>
      <thead>
        <tr>
          <td>Field</td>
          <td>Before</td>
          <td>After</td>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(value, key) in logEntry.changes" :key="key">
          <td>{{ key }}</td>
          <td class="has-text-danger">{{ value[0] }}</td>
          <td class="has-text-success">{{ value[1] }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: ["logEntry", "index"]
}
</script>
