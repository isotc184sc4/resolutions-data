<template>
  <div class="home-page">
    <div class="hero-section">
      <div class="hero-bg">
        <div class="hero-bg__mesh"></div>
        <div class="hero-bg__grid"></div>
      </div>
      
      <div class="hero-content">
        <h1 class="hero-title animate-up" style="--nth: 1">
          Four Decades of <br/> <span class="text-blue-accent">Industrial Decisions</span>
        </h1>
        
        <p class="hero-subtitle animate-up" style="--nth: 2">
          1,456 plenary resolutions from 86 meetings, spanning 1984 to 2026. Standards developed for the people who need them.
        </p>

        <div class="hero-stats animate-up" style="--nth: 3">
          <div class="stat-item">
            <span class="stat-value">1,456</span>
            <span class="stat-label">Resolutions</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">86</span>
            <span class="stat-label">Meetings</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">822</span>
            <span class="stat-label">Published Standards</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">1984</span>
            <span class="stat-label">Established</span>
          </div>
        </div>

        <div class="hero-search-wrapper animate-up" style="--nth: 4">
          <div class="hero-search-input-box">
            <svg class="hero-search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <circle cx="11" cy="11" r="8"/>
              <path d="m21 21-4.35-4.35"/>
            </svg>
            <input 
              ref="searchInputRef"
              type="search" 
              v-model="searchQuery" 
              class="hero-search-input" 
              placeholder="Search resolutions by topic, number, or keyword..." 
              autocomplete="off" 
              spellcheck="false" 
              aria-label="Search resolutions" 
            />
            <div class="hero-search-hint">
              <kbd>/</kbd> to search
            </div>
          </div>
        </div>

        <div class="hero-actions animate-up" style="--nth: 5">
          <button @click="scrollToResults" class="hero-btn hero-btn--primary">
            Browse Resolutions
          </button>
          <router-link :to="{ name: 'meetings' }" class="hero-btn hero-btn--secondary">
            Browse Meetings
          </router-link>
        </div>
      </div>
    </div>

    <div class="res-page" id="results-section">
      <div class="std-filter std-filter--elevated">
        <div class="std-filter__controls">
          <div class="std-filter__field">
            <span class="std-filter__label">Filter by Year</span>
            <div class="std-filter__chips">
              <button 
                class="std-chip" 
                :class="{ 'is-active': selectedYear === '' }"
                @click="selectedYear = ''"
              >All Years</button>
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
          <span class="meta-separator" v-if="searchQuery">&bull;</span>
          <span v-if="searchQuery">matching "{{ searchQuery }}"</span>
        </div>
      </div>

      <div class="std-results" v-if="isLoaded">
        <router-link 
          v-for="(res, index) in paginatedResolutions" 
          :key="res.source_file + res.id" 
          :to="{ name: 'resolution-detail', params: { id: res.id } }"
          class="std-results__card meeting-card animate-card"
          :style="`--nth: ${index % limit}`"
        >
          <div class="std-results__name">
            <span v-if="res.is_acclamation" class="std-results__type type-acclamation">Acclamation</span>
            <template v-else>
              <span>{{ res.id }}</span>
              <span class="std-results__type">Plenary</span>
            </template>
          </div>
          <div class="std-results__title meeting-card__title">
            {{ res.is_acclamation ? 'Acclamation' : (res.title || 'Resolution ' + res.id) }}
          </div>
          <div v-if="res.snippet" class="std-results__snippet snippet-text">{{ res.snippet }}</div>
          
          <div class="card-footer">
            <span v-if="res.meeting_date" class="std-results__badge badge-date">{{ formatDate(res.meeting_date) }}</span>
            <span v-if="res.venue" class="std-results__badge badge-venue truncate-text">{{ res.venue }}</span>
            <div class="card-hover-arrow">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </div>
          </div>
        </router-link>
        
        <div v-if="filteredResolutions.length === 0" class="empty-state">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="empty-state__icon"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
          <h3>No results found</h3>
          <p>Try adjusting your search or year filter.</p>
          <button class="std-chip btn-mt" @click="searchQuery=''; selectedYear=''">Clear filters</button>
        </div>
      </div>
      
      <div v-else class="loading-container">
        <div class="skeleton-grid">
          <div v-for="n in 6" :key="n" class="skeleton-card">
            <div class="skeleton-badge"></div>
            <div class="skeleton-title"></div>
            <div class="skeleton-title w-3-4"></div>
            <div class="skeleton-text"></div>
            <div class="skeleton-text"></div>
            <div class="skeleton-footer">
              <div class="skeleton-badge"></div>
              <div class="skeleton-badge"></div>
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="hasMore" class="load-more-container">
        <button @click="loadMore" class="std-chip load-more-btn">
          Load More
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useResolutions } from '../composables/useResolutions'

const { resolutions, isLoaded, loadData, search } = useResolutions()

const searchQuery = ref('')
const selectedYear = ref('')
const limit = ref(50)
const searchInputRef = ref<HTMLInputElement | null>(null)

onMounted(() => {
  loadData()
  window.addEventListener('keydown', handleGlobalKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleGlobalKeydown)
})

function handleGlobalKeydown(e: KeyboardEvent) {
  if (e.key === '/' && document.activeElement !== searchInputRef.value) {
    e.preventDefault()
    searchInputRef.value?.focus()
    scrollToResults()
  } else if (e.key === 'Escape' && document.activeElement === searchInputRef.value) {
    searchQuery.value = ''
    searchInputRef.value?.blur()
  }
}

function scrollToResults() {
  const resultsEl = document.getElementById('results-section')
  if (resultsEl) {
    const y = resultsEl.getBoundingClientRect().top + window.scrollY - 100
    window.scrollTo({ top: y, behavior: 'smooth' })
  }
}

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
  if (searchQuery.value || selectedYear.value) {
    scrollToResults()
  }
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
.home-page {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.hero-section {
  position: relative;
  width: 100%;
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  overflow: hidden;
  background-color: #020617;
  color: #fff;
  border-bottom: 1px solid #1e293b;
}
.dark .hero-section {
  background-color: #020617;
}

.hero-bg {
  position: absolute;
  inset: 0;
  z-index: 0;
}

.hero-bg__mesh {
  position: absolute;
  inset: 0;
  background: 
    radial-gradient(circle at 15% 50%, rgba(0, 97, 173, 0.15), transparent 25%),
    radial-gradient(circle at 85% 30%, rgba(227, 0, 15, 0.12), transparent 25%);
  opacity: 0.8;
}

.hero-bg__grid {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(to right, rgba(255,255,255,0.03) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(255,255,255,0.03) 1px, transparent 1px);
  background-size: 40px 40px;
  mask-image: linear-gradient(to bottom, black 40%, transparent 100%);
  -webkit-mask-image: linear-gradient(to bottom, black 40%, transparent 100%);
}

.hero-content {
  position: relative;
  z-index: 10;
  max-width: 64rem;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.hero-title {
  font-family: var(--font-serif);
  font-size: clamp(2.5rem, 6vw, 4.5rem);
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.02em;
  margin-bottom: 1.5rem;
  color: #f8fafc;
}

.text-blue-accent {
  color: #66a3e0;
}

.hero-subtitle {
  font-size: clamp(1.125rem, 2vw, 1.375rem);
  color: #94a3b8;
  max-width: 48rem;
  line-height: 1.6;
  margin-bottom: 3rem;
  font-weight: 400;
}

.hero-stats {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2rem;
  margin-bottom: 3.5rem;
  width: 100%;
}

@media (min-width: 768px) {
  .hero-stats {
    gap: 4rem;
  }
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.stat-value {
  font-family: var(--font-serif);
  font-size: 2.5rem;
  font-weight: 600;
  color: #fff;
  line-height: 1;
}

.stat-label {
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #64748b;
  font-weight: 600;
}

.hero-search-wrapper {
  width: 100%;
  max-width: 42rem;
  margin-bottom: 3rem;
}

.hero-search-input-box {
  position: relative;
  width: 100%;
  display: flex;
  align-items: center;
}

.hero-search-icon {
  position: absolute;
  left: 1.25rem;
  color: #64748b;
  pointer-events: none;
}

.hero-search-input {
  width: 100%;
  padding: 1.25rem 4rem 1.25rem 3.5rem;
  font-size: 1.125rem;
  border-radius: 9999px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(12px);
  color: #fff;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  -webkit-appearance: none;
}

.hero-search-input::placeholder {
  color: #475569;
}

.hero-search-input:focus {
  outline: none;
  border-color: #0061ad;
  background: rgba(15, 23, 42, 0.8);
  box-shadow: 0 0 0 4px rgba(0, 97, 173, 0.2), 0 20px 25px -5px rgba(0, 0, 0, 0.2);
}

.hero-search-hint {
  position: absolute;
  right: 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.75rem;
  color: #64748b;
  pointer-events: none;
}

.hero-search-hint kbd {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.1);
  font-family: var(--font-sans);
  font-weight: 600;
  color: #94a3b8;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
}

.hero-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.875rem 1.75rem;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 9999px;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.hero-btn--primary {
  background-color: #0061ad;
  color: #fff;
  border: 1px solid transparent;
  box-shadow: 0 4px 6px -1px rgba(0, 97, 173, 0.3), 0 2px 4px -1px rgba(0, 97, 173, 0.2);
}

.hero-btn--primary:hover {
  background-color: #005090;
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 97, 173, 0.4), 0 4px 6px -2px rgba(0, 97, 173, 0.2);
}

.hero-btn--secondary {
  background-color: transparent;
  color: #cbd5e1;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.hero-btn--secondary:hover {
  background-color: rgba(255, 255, 255, 0.05);
  color: #fff;
  border-color: rgba(255, 255, 255, 0.3);
}

/* Animations */
.animate-up {
  opacity: 0;
  transform: translateY(20px);
  animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  animation-delay: calc(var(--nth) * 0.15s);
}

@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-card {
  opacity: 0;
  transform: translateY(15px);
  animation: fadeUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  animation-delay: calc(var(--nth) * 0.05s);
}

.std-filter--elevated {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
  border: 1px solid rgba(226, 232, 240, 0.8);
  margin-top: -2rem;
  position: relative;
  z-index: 20;
}
.dark .std-filter--elevated {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
  border-color: rgba(51, 65, 85, 0.8);
}

.meta-separator {
  margin: 0 0.5rem;
  color: var(--color-slate-300);
}
.dark .meta-separator {
  color: var(--color-slate-700);
}

/* Card refinements */
.type-acclamation {
  background: #6366f1 !important;
  color: #fff !important;
  font-size: 0.75rem !important;
}

.snippet-text {
  font-size: 0.875rem;
  color: var(--color-slate-500);
  margin-top: 0.25rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  gap: 0.375rem;
  align-items: center;
  flex-wrap: wrap;
  margin-top: auto;
  padding-top: 1rem;
  position: relative;
}

.badge-venue {
  max-width: 150px;
}

.card-hover-arrow {
  margin-left: auto;
  color: var(--color-blue-accent);
  opacity: 0;
  transform: translateX(-10px);
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.meeting-card:hover .card-hover-arrow {
  opacity: 1;
  transform: translateX(0);
}

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
.btn-mt { margin-top: 1rem; }

.meeting-card {
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.3s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.3s;
}
.meeting-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 20px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
  border-color: var(--color-blue-accent);
}
.dark .meeting-card:hover {
  box-shadow: 0 12px 20px -5px rgb(0 0 0 / 0.4), 0 8px 10px -6px rgb(0 0 0 / 0.4);
}
.meeting-card__title {
  transition: color 0.3s;
  font-weight: 600;
  font-size: 1rem !important;
  color: var(--color-slate-900) !important;
}
.dark .meeting-card__title {
  color: white !important;
}
.meeting-card:hover .meeting-card__title {
  color: var(--color-blue-accent) !important;
}

.truncate-text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.load-more-container {
  margin-top: 3rem;
  text-align: center;
}

.load-more-btn {
  font-size: 0.875rem;
  font-weight: 600;
  padding: 0.5rem 1.5rem;
}

/* Skeleton Loading */
.loading-container {
  padding: 2.5rem 0;
  width: 100%;
}

.skeleton-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 0.75rem;
}

.skeleton-card {
  padding: 1rem;
  background: white;
  border-radius: 0.75rem;
  border: 1px solid var(--color-slate-200);
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.dark .skeleton-card {
  background: rgb(15 23 42 / 0.4);
  border-color: var(--color-slate-800);
}

.skeleton-badge,
.skeleton-title,
.skeleton-text {
  background-color: var(--color-slate-200);
  border-radius: 0.25rem;
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
.dark .skeleton-badge,
.dark .skeleton-title,
.dark .skeleton-text {
  background-color: var(--color-slate-800);
}

.skeleton-badge {
  height: 1rem;
  width: 4rem;
  border-radius: 9999px;
}

.skeleton-title {
  height: 1.5rem;
  width: 100%;
}

.w-3-4 { width: 75%; }

.skeleton-text {
  height: 1rem;
  width: 100%;
}

.skeleton-footer {
  display: flex;
  gap: 0.5rem;
  margin-top: auto;
  padding-top: 1rem;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: .5; }
}
</style>
