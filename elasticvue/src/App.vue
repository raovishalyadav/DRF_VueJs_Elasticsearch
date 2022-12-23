<template>
  <div class="container mt-5">
    <form @submit.prevent="search" class="mb-3">
      <div class="form-group row">
        <label for="query" class="col-sm-2 col-form-label"><font-awesome-icon icon="fa-solid fa-magnifying-glass" /> Search:</label>
        <div class="col-sm-10">
          <input id="query" v-model="query" class="form-control" />
        </div>
      </div>
      <div class="form-group row my-4"> <!-- added the my-4 class here -->
        <label for="searchType" class="col-sm-2 col-form-label"><font-awesome-icon icon="fa-solid fa-filter" /> Search Type:</label>
        <div class="col-sm-10">
          <select id="searchType" v-model="searchType" class="form-control form-select">
            <option value="full-text">Full-text</option>
            <option value="boolean">Boolean</option>
            <option value="fuzzy">Fuzzy</option>
            <option value="wildcard">Wildcard</option>
            <option value="regex">Regex</option>
          </select>

        </div>
      </div>
      <div class="form-group text-center">
        <button type="submit" class="btn btn-info">Search</button>
      </div>
    </form>


    <div v-if="query && submitted">
      <p class="mb-3">{{ total.value }} results found for '{{query}}'</p>
      <ul class="list-group">
        <li v-for="article in articles" :key="article.id" class="list-group-item">
          Title:{{ article._source.title }}<br>Content:{{ article._source.content }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      articles: [],
      query: '',
      searchType: 'full-text',
      total: { value: 0 },
      submitted: false,
    }
  },
  methods: {
    async search() {
      try {
        this.loading = true
        let params = {}
        if (this.searchType === 'full-text') {
          params.q = `title:${this.query} OR content:${this.query}`
        } else if (this.searchType === 'boolean') {
          params.q = `title:${this.query} AND content:${this.query}`
        } else if (this.searchType === 'fuzzy') {
          params.q = `title:${this.query}~ OR content:${this.query}~`
        } else if (this.searchType === 'wildcard') {
          params.q = `title:*${this.query}* OR content:*${this.query}*`
        } else if (this.searchType === 'regex') {
          params.q = `title:/${this.query}/ OR content:/${this.query}/`
        }
        const result = await axios.get('http://localhost:9200/articles/_search', {
          params,
        })
        this.articles = result.data.hits.hits
        this.total = result.data.hits.total
        this.submitted = true
      } catch (error) {
        console.error(error)
      }
    },
  },
}
</script>
