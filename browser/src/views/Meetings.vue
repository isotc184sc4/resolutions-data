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

    <div class="timeline-section animate-up" style="--nth: 4" v-if="isLoaded">
      <!-- Legend -->
      <div class="timeline-legend">
        <div class="legend-item legend-item--size">
          <span class="legend-size-small"></span>
          <span class="legend-size-medium"></span>
          <span class="legend-size-large"></span>
          <span class="legend-size-label">Node size = resolution count</span>
        </div>
        <div class="legend-item">
          <span class="legend-flag-example">🇯🇵</span>
          <span>Host country</span>
        </div>
        <div class="legend-item">
          <span class="legend-flag-example">🌐</span>
          <span>Virtual</span>
        </div>
      </div>

      <div v-if="filteredMeetings.length === 0" class="empty-state">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="empty-state__icon"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <h3>No meetings found</h3>
        <p>Try adjusting your search or year filter.</p>
        <button class="std-chip btn-mt" @click="searchQuery=''; selectedYear=''">Clear filters</button>
      </div>
      
      <div v-else class="decade-list">
        <section v-for="decade in meetingsByDecade" :key="decade.label" class="decade-block">
          <div class="decade-header">
            <h2 class="decade-title">{{ decade.label }}</h2>
            <span class="decade-summary">{{ decade.meetings.length }} meetings &middot; {{ decade.resCount }} resolutions</span>
          </div>
          
          <div class="timeline-track">
            <router-link 
              v-for="m in decade.meetings" 
              :key="m.source_file"
              :to="{ name: 'meeting-detail', params: { sourceFile: m.source_file } }"
              class="timeline-entry"
            >
              <div class="timeline-node-wrap">
                <span 
                  class="timeline-node"
                  :class="{
                    'node--small': m.resolution_count <= 5,
                    'node--medium': m.resolution_count > 5 && m.resolution_count <= 15,
                    'node--large': m.resolution_count > 15
                  }"
                ></span>
              </div>
              
              <div class="timeline-content">
                <div class="timeline-year">{{ m.year }}</div>
                <div class="timeline-venue">
                  <span v-if="venueToFlag(m.venue)" class="timeline-flag">{{ venueToFlag(m.venue) }}</span>
                  {{ m.venue || 'Virtual Meeting' }}
                </div>
                <div class="timeline-meta">
                  <span v-if="m.meeting_date" class="meta-date">{{ formatDate(m.meeting_date) }}</span>
                  <span class="meta-count">{{ m.resolution_count }} resolution{{ m.resolution_count !== 1 ? 's' : '' }}</span>
                </div>
              </div>

              <div class="timeline-arrow">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
              </div>
            </router-link>
          </div>
        </section>
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
import { venueToFlag } from '../data/countryFlags'

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

function formatDate(dateStr: string) {
  if (!dateStr) return ''
  try {
    const d = new Date(dateStr)
    return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric', timeZone: 'UTC' })
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

/* Timeline Section */
.timeline-section {
  margin-top: 3rem;
}

/* Legend */
.timeline-legend {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 1.5rem;
  padding: 1rem 1.5rem;
  background: var(--color-slate-50);
  border: 1px solid var(--color-slate-200);
  border-radius: 0.5rem;
  margin-bottom: 2.5rem;
  font-size: 0.8125rem;
  color: var(--color-slate-600);
}
.dark .timeline-legend {
  background: rgba(30, 41, 59, 0.5);
  border-color: var(--color-slate-800);
  color: var(--color-slate-400);
}

.legend-item {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.legend-flag-example {
  font-size: 1.25rem;
  line-height: 1;
}

.legend-item--size {
  gap: 0.375rem;
}
.legend-size-small,
.legend-size-medium,
.legend-size-large {
  display: inline-block;
  border-radius: 50%;
  background: var(--color-slate-400);
}
.legend-size-small { width: 0.375rem; height: 0.375rem; }
.legend-size-medium { width: 0.625rem; height: 0.625rem; }
.legend-size-large { width: 0.875rem; height: 0.875rem; }
.legend-size-label {
  margin-left: 0.25rem;
  font-style: italic;
}

/* Decade List */
.decade-list {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.decade-block {
  position: relative;
}

.decade-header {
  display: flex;
  align-items: baseline;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid var(--color-slate-100);
}
.dark .decade-header {
  border-bottom-color: var(--color-slate-800);
}

.decade-title {
  font-family: var(--font-serif);
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-slate-900);
  line-height: 1;
}
.dark .decade-title {
  color: white;
}

.decade-summary {
  font-size: 0.8125rem;
  color: var(--color-slate-500);
  font-weight: 500;
}
.dark .decade-summary {
  color: var(--color-slate-400);
}

/* Timeline Track */
.timeline-track {
  position: relative;
  display: flex;
  flex-direction: column;
}

/* Timeline Entry */
.timeline-entry {
  display: grid;
  grid-template-columns: 2rem 1fr auto;
  align-items: center;
  gap: 1.25rem;
  padding: 1rem 1.25rem;
  text-decoration: none;
  border-radius: 0.5rem;
  transition: background-color 0.2s ease, box-shadow 0.2s ease;
  position: relative;
}

/* Vertical connecting line */
.timeline-entry::before {
  content: '';
  position: absolute;
  left: calc(1rem - 1px);
  top: 0;
  bottom: 0;
  width: 2px;
  background: var(--color-slate-200);
  z-index: 0;
}
.dark .timeline-entry::before {
  background: var(--color-slate-700);
}

/* Remove the line for the first and last entry's outside portions */
.timeline-entry:first-child::before {
  top: 50%;
}
.timeline-entry:last-child::before {
  bottom: 50%;
}

.timeline-entry:hover,
.timeline-entry:focus-visible {
  background: var(--color-slate-50);
  outline: none;
}
.dark .timeline-entry:hover,
.dark .timeline-entry:focus-visible {
  background: rgba(30, 41, 59, 0.5);
}

/* Node */
.timeline-node-wrap {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
}

.timeline-node {
  display: block;
  border-radius: 50%;
  background: var(--color-blue-accent);
  border: 3px solid white;
  box-shadow: 0 0 0 1px var(--color-blue-accent);
  transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}
.dark .timeline-node {
  border-color: var(--color-slate-900);
}

.node--small { width: 0.5rem; height: 0.5rem; }
.node--medium { width: 0.75rem; height: 0.75rem; }
.node--large { width: 1rem; height: 1rem; }

.timeline-entry:hover .timeline-node,
.timeline-entry:focus-visible .timeline-node {
  transform: scale(1.3);
}

/* Content */
.timeline-content {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
  min-width: 0;
}

.timeline-year {
  font-family: var(--font-serif);
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--color-slate-900);
  line-height: 1.3;
}
.dark .timeline-year {
  color: white;
}

.timeline-venue {
  font-size: 0.9375rem;
  color: var(--color-slate-600);
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.dark .timeline-venue {
  color: var(--color-slate-300);
}

.timeline-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  font-size: 0.75rem;
  color: var(--color-slate-500);
  margin-top: 0.125rem;
}
.dark .timeline-meta {
  color: var(--color-slate-400);
}

.meta-count {
  font-weight: 600;
  color: var(--color-slate-600);
}
.dark .meta-count {
  color: var(--color-slate-300);
}

.timeline-flag {
  margin-right: 0.375rem;
  font-size: 1.375rem;
  line-height: 1;
  vertical-align: -2px;
}

/* Arrow */
.timeline-arrow {
  color: var(--color-slate-300);
  opacity: 0;
  transform: translateX(-8px);
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  flex-shrink: 0;
}

.timeline-entry:hover .timeline-arrow,
.timeline-entry:focus-visible .timeline-arrow {
  opacity: 1;
  transform: translateX(0);
  color: var(--color-blue-accent);
}

/* Responsive */
@media (max-width: 640px) {
  .timeline-entry {
    grid-template-columns: 1.5rem 1fr auto;
    gap: 0.75rem;
    padding: 0.75rem;
  }
  .timeline-year {
    font-size: 1rem;
  }
  .timeline-venue {
    font-size: 0.875rem;
  }
  .timeline-meta {
    gap: 0.5rem;
  }
  .timeline-legend {
    gap: 1rem;
    padding: 0.75rem 1rem;
  }
  .legend-item--size {
    display: none;
  }
}

/* Empty State */
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