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
        class="std-results__card meeting-card"
      >
        <div class="std-results__name">
          <span v-if="res.is_acclamation" class="std-results__type" style="background:#6366f1;color:#fff;font-size:0.75rem;">Acclamation</span>
          <template v-else>
            <span>{{ res.id }}</span>
            <span class="std-results__type">Plenary</span>
          </template>
        </div>
        <div class="std-results__title meeting-card__title">{{ res.is_acclamation ? 'Acclamation' : (res.title || 'Resolution ' + res.id) }}</div>
        <div v-if="res.snippet" class="std-results__snippet" style="font-size:0.875rem;color:var(--color-slate-500);margin-top:0.25rem;">{{ res.snippet }}</div>
        <div style="display:flex;gap:0.375rem;align-items:center;flex-wrap:wrap;margin-top:auto;padding-top:1rem;">
          <span v-if="res.meeting_date" class="std-results__badge">{{ formatDate(res.meeting_date) }}</span>
          <span v-if="res.venue" class="std-results__badge truncate-text" style="max-width: 150px">{{ res.venue }}</span>
        </div>
      </router-link>
      
      <div v-if="filteredResolutions.length === 0" class="empty-state">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="empty-state__icon"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <h3>No results found</h3>
        <p>Try adjusting your search or year filter.</p>
        <button class="std-chip" style="margin-top:1rem;" @click="searchQuery=''; selectedYear=''">Clear filters</button>
      </div>
    </div>
    <div v-else style="padding-top: 2.5rem; padding-bottom: 2.5rem; text-align: center;">
      <div class="loading-pulse">
        <div class="loading-pulse__line"></div>
        <div class="loading-pulse__line" style="width: 8rem"></div>
      </div>
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
  let list = resolutions.value
  
  if (selectedYear.value) {
    list = list.filter(r => r.year === selectedYear.value)
  }
  
  if (searchQuery.value) {
    const q = searchQuery.value.trim()
    const matchedIndices = search(q)
    
    if (matchedIndices && matchedIndices.size > 0) {
      list = list.filter((_, i) => matchedIndices.has(i))
    } else {
      const qLower = q.toLowerCase()
      list = list.filter(r => 
        (r.title && r.title.toLowerCase().includes(qLower)) ||
        (r.id && r.id.toLowerCase().includes(qLower)) ||
        (r.subject && r.subject.toLowerCase().includes(qLower)) ||
        (r.venue && r.venue.toLowerCase().includes(qLower))
      )
    }
  }
  
  return list
})

const paginatedResolutions = computed(() => {
  return filteredResolutions.value.slice(0, limit.value)
})

const hasMore = computed(() => {
  return limit.value < filteredResolutions.value.length
})

function loadMore() {
  limit.value += 50
}

watch([searchQuery, selectedYear], () => {
  limit.value = 50
})

function formatDate(dateStr: string) {
  if (!dateStr) return ''
  try {
    const d = new Date(dateStr)
    return d.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric', timeZone: 'UTC' })
  } catch(e) {
    return dateStr
  }
}
</script>

<style scoped>
.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 4rem 1rem;
  background: white;
  border-radius: 1rem;
  border: 1px dashed var(--color-slate-200);
}
.dark .empty-state {
  background: var(--color-slate-900);
  border-color: var(--color-slate-800);
}
.empty-state__icon {
  width: 3rem;
  height: 3rem;
  margin: 0 auto 1rem;
  color: var(--color-slate-300);
}
.dark .empty-state__icon { color: var(--color-slate-600); }
.empty-state h3 {
  font-family: var(--font-serif);
  font-size: 1.25rem;
  color: var(--color-slate-900);
  margin-bottom: 0.5rem;
}
.dark .empty-state h3 { color: white; }
.empty-state p { color: var(--color-slate-500); }

.meeting-card {
  transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}
.meeting-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
}
.dark .meeting-card:hover {
  box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.4), 0 4px 6px -4px rgb(0 0 0 / 0.4);
}
.meeting-card__title {
  transition: color 0.2s;
}
.meeting-card:hover .meeting-card__title {
  color: var(--color-blue-accent);
}

.truncate-text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.loading-pulse {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
.loading-pulse__line {
  height: 1rem;
  width: 6rem;
  background-color: var(--color-slate-200);
  border-radius: 0.25rem;
}
.dark .loading-pulse__line {
  background-color: var(--color-slate-700);
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: .5; }
}
</style>

