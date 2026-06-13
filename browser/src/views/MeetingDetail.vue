<template>
  <div class="res-page">
    <div v-if="!isLoaded" style="padding-top: 2.5rem; text-align: center;">
      <div class="loading-pulse">
        <div class="loading-pulse__line"></div>
        <div class="loading-pulse__line" style="width: 16rem; height: 2rem;"></div>
      </div>
    </div>
    <div v-else-if="!meeting" class="empty-state" style="margin-top: 2rem;">
      <h3>Meeting not found</h3>
      <p>The meeting you are looking for does not exist.</p>
      <router-link :to="{ name: 'meetings' }" class="std-chip" style="margin-top: 1rem; display: inline-block; text-decoration: none;">Back to Meetings</router-link>
    </div>
    <template v-else>
      <header class="res-page__header" style="margin-top: 1rem;">
        <router-link :to="{ name: 'meetings' }" class="back-link group" style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.875rem; color: var(--color-slate-500); text-decoration: none; margin-bottom: 1.5rem; width: max-content;">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="back-link__icon" style="transition: transform 0.2s;"><path d="m15 18-6-6 6-6"/></svg>
          Back to Meetings
        </router-link>
        
        <div style="margin-bottom: 0.75rem; display: flex; flex-wrap: wrap; gap: 0.5rem;">
          <span class="std-results__badge" style="background: var(--color-slate-100); color: var(--color-slate-700);">{{ meeting.year }}</span>
          <span v-if="meeting.meeting_date" class="std-results__badge">{{ formatDate(meeting.meeting_date) }}</span>
        </div>
        
        <h1 class="meeting-detail__title">{{ meeting.venue || 'Virtual Meeting' }}</h1>
        <p class="res-page__subtitle" style="max-width: 48rem;">{{ meeting.source_title }}</p>
      </header>

      <div class="std-filter__meta" style="border-bottom: 1px solid var(--color-slate-200); padding-bottom: 1rem; margin-bottom: 2rem;">
        <h2 style="font-family: var(--font-serif); font-size: 1.25rem;">{{ meeting.resolution_count }} Resolutions</h2>
      </div>

      <div class="std-results">
        <router-link 
          v-for="res in meetingResolutions" 
          :key="res.id" 
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
            <span v-if="res.subject" class="std-results__badge truncate-text" style="max-width: 100%; background:var(--color-slate-100);color:var(--color-slate-700);">{{ res.subject }}</span>
          </div>
        </router-link>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useMeetings } from '../composables/useMeetings'

const route = useRoute()
const { getMeeting, getMeetingResolutions, isLoaded, loadData } = useMeetings()

const sourceFile = computed(() => route.params.sourceFile as string)

onMounted(() => {
  loadData()
})

const meeting = computed(() => {
  return isLoaded.value ? getMeeting(sourceFile.value) : null
})

const meetingResolutions = computed(() => {
  return isLoaded.value ? getMeetingResolutions(sourceFile.value) : []
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

.meeting-detail__title {
  font-family: var(--font-serif);
  color: var(--color-slate-900);
  margin-bottom: 1rem;
  line-height: 1.1;
  font-size: 1.875rem;
}
@media (min-width: 768px) {
  .meeting-detail__title { font-size: 2.25rem; }
}
@media (min-width: 1024px) {
  .meeting-detail__title { font-size: 3rem; }
}
.dark .meeting-detail__title { color: white; }

.back-link:hover {
  color: var(--color-slate-900);
}
.dark .back-link:hover {
  color: white;
}
.back-link:hover .back-link__icon {
  transform: translateX(-4px);
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
