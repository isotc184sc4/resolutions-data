<template>
  <div class="res-page">
    <header class="res-page__header">
      <h1>Resolutions</h1>
      <p class="res-page__subtitle">All plenary resolutions of ISO/TC 184/SC 4 "Industrial data", searchable by identifier, title, or keyword.</p>
    </header>

    <div class="std-filter" id="std-filter">
      <div class="std-filter__search-wrap">
        <svg class="std-filter__search-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <circle cx="11" cy="11" r="8"/>
          <path d="m21 21-4.35-4.35"/>
        </svg>
        <input 
          type="search" 
          v-model="searchQuery" 
          class="std-filter__search" 
          placeholder="Search resolutions…" 
          autocomplete="off" 
          spellcheck="false" 
          aria-label="Search resolutions" 
        />
      </div>
      <div class="std-filter__controls">
        <div class="std-filter__field">
          <span class="std-filter__label">Year</span>
          <div class="std-filter__chips">
            <button 
              class="std-chip" 
              :class="{ 'is-active': selectedYear === '' }"
              @click="selectedYear = ''"
            >All</button>
            <button 
              v-for="year in availableYears" 
              :key="year"
              class="std-chip"
              :class="{ 'is-active': selectedYear === year }"
              @click="selectedYear = year"
            >{{ year }}</button>
          </div>
        </div>
      </div>
      <div class="std-filter__meta">
        <span>{{ filteredResolutions.length }} results</span>
      </div>
    </div>

    <div class="std-results" v-if="isLoaded">
      <router-link 
        v-for="res in paginatedResolutions" 
        :key="res.source_file + res.id" 
        :to="`/resolution/${res.id}`"
        class="std-results__card"
      >
        <div class="std-results__name">
          <span v-if="res.is_acclamation" class="std-results__type" style="background:#6366f1;color:#fff;font-size:0.75rem;">Acclamation</span>
          <template v-else>
            <span>{{ res.id }}</span>
            <span class="std-results__type">Plenary</span>
          </template>
        </div>
        <div class="std-results__title">{{ res.is_acclamation ? 'Acclamation' : (res.title || 'Resolution ' + res.id) }}</div>
        <div v-if="res.snippet" class="std-results__snippet" style="font-size:0.875rem;color:var(--color-slate-500);margin-top:0.25rem;">{{ res.snippet }}</div>
        <div style="display:flex;gap:0.375rem;align-items:center;flex-wrap:wrap;margin-top:auto;padding-top:1rem;">
          <span v-if="res.meeting_date" class="std-results__badge">{{ formatDate(res.meeting_date) }}</span>
          <span v-if="res.venue" class="std-results__badge">{{ res.venue }}</span>
        </div>
      </router-link>
    </div>
    <div v-else style="padding-top: 2.5rem; padding-bottom: 2.5rem; text-align: center;">
      Loading...
    </div>
    
    <div v-if="hasMore" style="margin-top: 2rem; text-align: center;">
      <button @click="loadMore" class="std-chip" style="font-size: 0.875rem; font-weight: 500;">
        Load More
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useResolutions } from '../composables/useResolutions'

const { resolutions, isLoaded, loadData, search } = useResolutions()

const searchQuery = ref('')
const selectedYear = ref('')
const limit = ref(50)

onMounted(() => {
  loadData()
})

const availableYears = computed(() => {
  const years = new Set<string>()
  resolutions.value.forEach(r => {
    if (r.year) years.add(r.year)
  })
  return Array.from(years).sort((a, b) => b.localeCompare(a))
})

const filteredResolutions = computed(() => {
  if (!isLoaded.value) return []
  
  let results = resolutions.value
  
  if (searchQuery.value.trim()) {
    const matchedIds = search(searchQuery.value.trim())
    results = Array.from(matchedIds).map(id => resolutions.value[id]).filter(Boolean)
  }
  
  if (selectedYear.value) {
    results = results.filter(r => r.year === selectedYear.value)
  }
  
  if (searchQuery.value.trim()) {
    results.sort((a, b) => {
      if (a.meeting_date !== b.meeting_date) {
        return (b.meeting_date || '').localeCompare(a.meeting_date || '')
      }
      return parseFloat(b.id) - parseFloat(a.id)
    })
  }
  
  return results
})

const paginatedResolutions = computed(() => {
  return filteredResolutions.value.slice(0, limit.value)
})

const hasMore = computed(() => {
  return limit.value < filteredResolutions.value.length
})

const loadMore = () => {
  limit.value += 50
}

const formatDate = (iso: string) => {
  if (!iso) return ''
  const d = new Date(iso + 'T00:00:00')
  return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
}

watch([searchQuery, selectedYear], () => {
  limit.value = 50 // Reset pagination on filter change
})
</script>
