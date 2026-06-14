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

    <div class="timeline-container animate-up" style="--nth: 4" v-if="isLoaded">
      <div v-if="filteredMeetings.length === 0" class="empty-state">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="empty-state__icon"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <h3>No meetings found</h3>
        <p>Try adjusting your search or year filter.</p>
        <button class="std-chip btn-mt" @click="searchQuery=''; selectedYear=''">Clear filters</button>
      </div>
      
      <div v-else class="decade-timeline">
        <div v-for="decade in meetingsByDecade" :key="decade.label" class="decade-row">
          <div class="decade-label">{{ decade.label }}</div>
          
          <div class="decade-track">
            <div class="decade-line"></div>
            <div class="decade-dots">
              <router-link 
                v-for="m in decade.meetings" 
                :key="m.source_file"
                :to="{ name: 'meeting-detail', params: { sourceFile: m.source_file } }"
                class="meeting-dot"
                :class="{ 'has-acclamation': m.acclamation_count > 0 }"
                :aria-label="m.year + ' Plenary: ' + m.venue"
              >
                <div class="meeting-tooltip">
                  <div class="tooltip-title">{{ m.venue || 'Unknown Venue' }}</div>
                  <div class="tooltip-meta">{{ m.year }} &bull; {{ m.resolution_count }} res</div>
                </div>
              </router-link>
            </div>
          </div>
          
          <div class="decade-stats">
            {{ decade.meetings.length }} meetings &middot; {{ decade.resCount }} resolutions
          </div>
        </div>
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
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useMeetings } from '../composables/useMeetings'

const router = useRouter()
const route = useRoute()

const { meetings, isLoaded, loadData } = useMeetings()

const searchQuery = ref((route.query.q as string) || '')
const selectedYear = ref((route.query.year as string) || '')

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

const meetingsByDecade = computed(() => {
  const decades: Record<string, { meetings: any[], resCount: number, accCount: number }> = {}
  filteredMeetings.value.forEach(m => {
    const year = parseInt(m.year)
    if (isNaN(year)) return
    const decade = Math.floor(year / 10) * 10 + 's'
    if (!decades[decade]) {
      decades[decade] = { meetings: [], resCount: 0, accCount: 0 }
    }
    decades[decade].meetings.push(m)
    decades[decade].resCount += (m.resolution_count || 0)
    decades[decade].accCount += (m.acclamation_count || 0)
  })
  
  return Object.keys(decades)
    .sort((a, b) => b.localeCompare(a))
    .map(key => ({
      label: key,
      resCount: decades[key].resCount,
      accCount: decades[key].accCount,
      meetings: decades[key].meetings.sort((a, b) => a.year.localeCompare(b.year))
    }))
})

watch([searchQuery, selectedYear], () => {
  const query: Record<string, string> = {}
  if (searchQuery.value) query.q = searchQuery.value
  if (selectedYear.value) query.year = selectedYear.value
  router.replace({ query })
})
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

.timeline-container {
  margin-top: 3rem;
  padding: 2rem;
  background: white;
  border-radius: 1rem;
  border: 1px solid var(--color-slate-200);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.025);
}
.dark .timeline-container {
  background: var(--color-slate-900);
  border-color: var(--color-slate-800);
}

.decade-timeline {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.decade-row {
  display: grid;
  grid-template-columns: 80px 1fr auto;
  align-items: center;
  gap: 2rem;
}

@media (max-width: 1024px) {
  .decade-row {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}

.decade-label {
  font-family: var(--font-serif);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-slate-900);
}
.dark .decade-label {
  color: white;
}

.decade-track {
  position: relative;
  display: flex;
  align-items: center;
  min-height: 40px;
}

.decade-line {
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 2px;
  background-color: var(--color-slate-200);
  transform: translateY(-50%);
  z-index: 1;
}
.dark .decade-line {
  background-color: var(--color-slate-700);
}

.decade-dots {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  gap: 2rem;
  flex-wrap: wrap;
  width: 100%;
}

.meeting-dot {
  position: relative;
  width: 16px;
  height: 16px;
  background-color: white;
  border: 3px solid var(--color-slate-400);
  border-radius: 50%;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  cursor: pointer;
}
.dark .meeting-dot {
  background-color: var(--color-slate-900);
  border-color: var(--color-slate-500);
}

.meeting-dot:hover,
.meeting-dot:focus-visible {
  border-color: var(--color-blue-accent);
  transform: scale(1.5);
  outline: none;
  z-index: 10;
  box-shadow: 0 0 0 4px rgba(0, 97, 173, 0.1);
}

.meeting-dot.has-acclamation {
  border-color: #6366f1;
}
.meeting-dot.has-acclamation:hover,
.meeting-dot.has-acclamation:focus-visible {
  border-color: #4f46e5;
  box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2);
}

.meeting-tooltip {
  position: absolute;
  bottom: calc(100% + 10px);
  left: 50%;
  transform: translateX(-50%) translateY(10px);
  background: var(--color-slate-900);
  color: white;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  white-space: nowrap;
  opacity: 0;
  visibility: hidden;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -2px rgba(0, 0, 0, 0.1);
  pointer-events: none;
}
.dark .meeting-tooltip {
  background: white;
  color: var(--color-slate-900);
}

.meeting-tooltip::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border-width: 6px;
  border-style: solid;
  border-color: var(--color-slate-900) transparent transparent transparent;
}
.dark .meeting-tooltip::after {
  border-color: white transparent transparent transparent;
}

.meeting-dot:hover .meeting-tooltip,
.meeting-dot:focus-visible .meeting-tooltip {
  opacity: 1;
  visibility: visible;
  transform: translateX(-50%) translateY(0);
}

.tooltip-title {
  font-weight: 600;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.tooltip-meta {
  font-size: 0.75rem;
  color: var(--color-slate-300);
}
.dark .tooltip-meta {
  color: var(--color-slate-600);
}

.decade-stats {
  font-size: 0.875rem;
  color: var(--color-slate-500);
  font-weight: 500;
  white-space: nowrap;
}
.dark .decade-stats {
  color: var(--color-slate-400);
}

.empty-state {
  text-align: center;
  padding: 4rem 1rem;
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
