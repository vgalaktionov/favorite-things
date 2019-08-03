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
  </div>
</template>

<script>
export default {
  props: ["thingData"]
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
</style>
