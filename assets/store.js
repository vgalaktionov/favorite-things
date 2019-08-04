import Vue from 'Vue'
import Vuex from 'vuex'
import api from './api'

Vue.use(Vuex)

const createStore = () => new Vuex.Store({
  state: {
    categories: [],
    things: [],
    showModal: false,
    editingThing: null
  },
  getters: {
    selectedCategories(state) {
      return state.categories.filter(({ selected }) => !!selected).map(c => c.id)
    }
  },
  mutations: {
    setCategories(state, { categories }) {
      state.categories = categories
    },
    setThings(state, { things }) {
      state.things = things
    },
    setShowModal(state, { show, editing }) {
      state.showModal = show
      state.editingThing = editing
    },
  },
  actions: {
    async fetchCategories(context) {
      try {
        const { data: categories } = await api.get("/api/categories/")
        context.commit('setCategories', { categories })
      } catch (error) {
        console.error(error)
      }
    },
    async fetchThings(context) {
      try {
        const { data: things } = await api.get("/api/things/")
        context.commit('setThings', { things })
      } catch (error) {
        console.error(error)
      }
    },
    async addNewCategory(context, newCategory) {
      try {
        await api.post("/api/categories/", { name: newCategory })
        context.dispatch("fetchCategories")
      } catch (error) {
        console.error(error)
      }
    },
    async removeCategory(context, idToRemove) {
      try {
        await api.delete(`/api/categories/${idToRemove}/`)
        context.commit("setCategories", { categories: context.state.categories.filter(({ id }) => id !== idToRemove) })
      } catch (error) {
        console.error(error)
      }
    }
  }
})

export default createStore
