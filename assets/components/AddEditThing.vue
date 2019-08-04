<template>
  <div class="modal" :class="{'is-active': showModal}">
    <div class="modal-background"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">{{ editingThing ? 'Edit' : 'Add' }} Thing</p>
        <button class="modal-close is-large" @click="cancel"></button>
      </header>
      <section class="modal-card-body">
        <div class="field">
          <label class="label">Title</label>
          <div class="control">
            <input class="input" type="text" placeholder="Title" v-model="title" />
          </div>
        </div>
        <div class="field">
          <label class="label">Description</label>
          <div class="control">
            <textarea class="textarea" placeholder="Description" v-model="description"></textarea>
          </div>
        </div>
        <div class="field">
          <label class="label">Category</label>
          <div class="control">
            <div class="select">
              <select v-model="category">
                <option
                  v-for="category in categories"
                  :key="category.id"
                  :value="category.id"
                >{{ category.name }}</option>
              </select>
            </div>
          </div>
        </div>
        <div class="field">
          <label class="label">Ranking</label>
          <div class="control">
            <input type="number" class="input" v-model="ranking" />
          </div>
        </div>
        <div class="field">
          <label class="label">Metadata</label>
          <div class="control">
            <Editor
              @init="editorInit"
              lang="json"
              theme="xcode"
              width="100%"
              height="100"
              v-model="metadata"
            />
          </div>
          <p class="help">Please enter valid JSON.</p>
        </div>
      </section>
      <footer class="modal-card-foot">
        <button class="button is-success" @click="submit">Save</button>
        <button class="button" @click="cancel">Cancel</button>
      </footer>
    </div>
  </div>
</template>

<script>
import Editor from "vue2-ace-editor"
import api from "../api"

export default {
  data() {
    return {
      edit: false,
      id: null,
      title: "",
      description: "",
      ranking: null,
      category: null,
      metadata: ""
    }
  },
  components: {
    Editor
  },
  computed: {
    categories() {
      return this.$store.state.categories || []
    },
    showModal() {
      return this.$store.state.showModal || false
    },
    editingThing() {
      const thing =
        this.$store.state.things.find(
          t => t.id === this.$store.state.editingThing
        ) || null
      // if (thing) {
      //   Object.assign(this, thing)
      // }
      return thing
    }
  },
  methods: {
    editorInit(editor) {
      require("brace/ext/language_tools")
      require("brace/mode/json")
      require("brace/theme/xcode")
    },
    cancel() {
      this.$store.commit("setShowModal", { show: false, edit: false })
    },
    async submit() {
      try {
        await api.post("/api/things/", {
          id: this.id,
          title: this.title,
          description: this.description,
          category: this.category,
          ranking: this.ranking,
          metadata: JSON.parse(this.metadata)
        })
      } catch (error) {
        console.error(error)
      }
      this.$store.dispatch("fetchThings")
      this.$store.commit("setShowModal", { show: false, edit: false })
    }
  }
}
</script>
