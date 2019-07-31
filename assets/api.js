import axios from 'axios'
import Cookie from 'js-cookie'


export default axios.create({
  headers: {
    'X-CSRFToken': Cookie.get('csrftoken')
  }
})
