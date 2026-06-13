<template>
  <div class="res-page">
    <header class="res-page__header">
      <h1 class="animate-up" style="--nth: 1">Meetings</h1>
      <p class="res-page__subtitle animate-up" style="--nth: 2">Browse resolutions by plenary meeting.</p>
    </header>

    <div class="std-filter animate-up" style="--nth: 3">
      <div class="std-filter__search-wrap">
        <svg class="std-filter__search-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <circle cx="11" cy="11" r="8"/>
          <path d="m21 21-4.35-4.35"/>
        </svg>
        <input 
          type="search" 
          v-model="searchQuery" 
          class="std-filter__search" 
          placeholder="Search meetings by venue or year…" 
          autocomplete="off" 
          spellcheck="false" 
          aria-label="Search meetings" 
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
        <span>{{ filteredMeetings.length }} meetings</span>
      </div>
    </div>

    <div class="std-results" v-if="isLoaded">
      <router-link 
        v-for="(meeting, index) in paginatedMeetings" 
        :key="meeting.source_file" 
        :to="{ name: 'meeting-detail', params: { sourceFile: meeting.source_file } }"
        class="std-results__card meeting-card animate-card"
        :style="`--nth: ${index % limit}`"
      >
        <div class="std-results__name">
          <span>{{ meeting.year }} Plenary</span>
          <span class="std-results__type">{{ meeting.resolution_count }} Resolutions</span>
        </div>
        <div class="std-results__title meeting-card__title">{{ meeting.venue || 'Unknown Venue' }}</div>
        
        <div class="card-footer">
          <span v-if="meeting.meeting_date" class="std-results__badge">{{ formatDate(meeting.meeting_date) }}</span>
          <span v-if="meeting.acclamation_count > 0" class="std-results__badge badge-acclamation">{{ meeting.acclamation_count }} Acclamations</span>
          
          <div class="card-hover-arrow">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
          </div>
        </div>
      </router-link>
      
      <div v-if="filteredMeetings.length === 0" class="empty-state">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="empty-state__icon"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <h3>No meetings found</h3>
        <p>Try adjusting your search or year filter.</p>
        <button class="std-chip btn-mt" @click="searchQuery=''; selectedYear=''">Clear filters</button>
      </div>
    </div>
    
    <div v-else class="loading-container">
      <div class="skeleton-grid">
        <div v-for="n in 6" :key="n" class="skeleton-card">
          <div class="skeleton-badge"></div>
          <div class="skeleton-title"></div>
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
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useMeetings } from '../composables/useMeetings'

const { meetings, isLoaded, loadData } = useMeetings()

const searchQuery = ref('')
const selectedYear = ref('')
const limit = ref(50)

onMounted(() => {
  loadData()
})

const availableYears = computed(() => {
  const years = new Set<string>()
  meetings.value.forEach(m => {
    if (m.year) years.add(m.year)
  })
  return Array.from(years).sort((a, b) => b.localeCompare(a))
})

const filteredMeetings = computed(() => {
  let list = meetings.value
  
  if (selectedYear.value) {
    list = list.filter(m => m.year === selectedYear.value)
  }
  
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(m => 
      (m.venue && m.venue.toLowerCase().includes(q)) ||
      (m.year && m.year.toLowerCase().includes(q)) ||
      (m.source_title && m.source_title.toLowerCase().includes(q))
    )
  }
  
  return list
})

const paginatedMeetings = computed(() => {
  return filteredMeetings.value.slice(0, limit.value)
})

const hasMore = computed(() => {
  return limit.value < filteredMeetings.value.length
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
/* Animations */
.animate-up {
  opacity: 0;
  transform: translateY(20px);
  animation: fadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  animation-delay: calc(var(--nth) * 0.1s);
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-card {
  opacity: 0;
  transform: translateY(15px);
  animation: fadeUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  animation-delay: calc(var(--nth) * 0.05s);
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

.btn-mt {
  margin-top: 1rem;
}

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
  font-size: 1.125rem !important;
  color: var(--color-slate-900) !important;
}
.dark .meeting-card__title {
  color: white !important;
}
.meeting-card:hover .meeting-card__title {
  color: var(--color-blue-accent) !important;
}

.card-footer {
  display: flex;
  gap: 0.375rem;
  align-items: center;
  flex-wrap: wrap;
  margin-top: auto;
  padding-top: 1rem;
}

.badge-acclamation {
  background: var(--color-slate-100);
  color: var(--color-slate-700);
}
.dark .badge-acclamation {
  background: var(--color-slate-800);
  color: var(--color-slate-300);
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
.skeleton-title {
  background-color: var(--color-slate-200);
  border-radius: 0.25rem;
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
.dark .skeleton-badge,
.dark .skeleton-title {
  background-color: var(--color-slate-800);
}

.skeleton-badge {
  height: 1rem;
  width: 5rem;
  border-radius: 9999px;
}

.skeleton-title {
  height: 1.75rem;
  width: 80%;
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