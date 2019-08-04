import Vue from 'Vue'
import Vuex from 'vuex'
import api from './api'

Vue.use(Vuex)

const createStore = () => new Vuex.Store({
  state: {
    categories: [],
    things: [],
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
    }
  },
  actions: {
    async initialFetch(context) {
      try {
        const { data: categories } = await api.get("/api/categories/")
        const { data: things } = await api.get("/api/things/")
        context.commit('setCategories', { categories })
        context.commit('setThings', { things })
      } catch (error) {
        console.error(error)
      }
    },
    async addNewCategory(context, newCategory) {
      try {
        await api.post("/api/categories/", { name: newCategory })
        context.commit("setCategories", {
          categories: [
            ...context.state.categories,
            { name: newCategory, user: window.userID }
          ]
        })
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
