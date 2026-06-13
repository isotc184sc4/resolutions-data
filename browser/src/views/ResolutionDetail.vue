<template>
  <div v-if="resolution" class="std-page res-detail-page">

    <!-- Back link -->
    <button @click="$router.back()" class="std-page__back back-link">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="back-link__icon"><path d="m15 18-6-6 6-6"/></svg>
      Go Back
    </button>

    <!-- Header -->
    <header class="std-page__header res-detail-header">
      <div class="std-page__meta res-detail-meta">
        <span v-if="resolution.is_acclamation" class="std-page__badge res-detail-badge--acclamation">Acclamation</span>
        <span v-else-if="resolution.id" class="std-page__badge font-mono" style="font-weight:600">{{ resolution.id }}</span>
        
        <router-link 
          v-if="resolution.source_file" 
          :to="{ name: 'meeting-detail', params: { sourceFile: resolution.source_file } }" 
          class="std-page__badge std-page__badge--link"
        >
          <template v-if="resolution.venue">{{ resolution.venue }}</template>
          <template v-else-if="resolution.source_title">{{ resolution.source_title }}</template>
        </router-link>
        
        <span v-if="resolution.meeting_date" class="std-page__badge" style="color:var(--color-slate-600);">{{ formatDate(resolution.meeting_date) }}</span>
        <span v-if="!resolution.is_acclamation" class="std-page__badge">
          <template v-if="resolution.source_type === 'plenary'">Plenary resolution</template>
          <template v-else-if="resolution.source_type === 'ballot'">Ballot resolution</template>
          <template v-else-if="resolution.source_type === '7372ma'">7372 MA resolution</template>
          <template v-else>Resolution</template>
        </span>
        <a v-if="resolution.group_id" :href="`/groups/${resolution.group_id}/`" class="std-page__badge std-page__badge--link" style="color:var(--color-blue-accent); border-color:var(--color-blue-accent);">{{ resolution.group_id.toUpperCase() }}</a>
      </div>

      <h1 v-if="resolution.title" class="std-page__title res-detail-title">{{ resolution.title }}</h1>

      <p v-if="resolution.source_title" class="res-detail-subtitle">
        {{ resolution.source_title }}
      </p>
    </header>

    <!-- Content -->
    <div class="std-page__content res-detail-content">

      <section v-if="resolution.subject" class="std-page__section">
        <h2 class="std-page__section-heading res-detail-section-title">Subject</h2>
        <div class="std-page__body res-detail-body">
          <p>{{ resolution.subject }}</p>
        </div>
      </section>

      <section v-if="resolution.considerations && resolution.considerations.length > 0" class="std-page__section">
        <h2 class="std-page__section-heading res-detail-section-title">Considerations</h2>
        <div class="std-page__body res-detail-list">
          <div v-for="(cons, idx) in resolution.considerations" :key="idx" class="consideration-item res-detail-card">
            <span v-if="cons.type" class="res-detail-card-type">{{ cons.type }}</span>
            <div class="res-detail-richtext" v-html="asciidocify(cons.message)"></div>
          </div>
        </div>
      </section>

      <section v-if="resolution.actions && resolution.actions.length > 0" class="std-page__section">
        <h2 class="std-page__section-heading res-detail-section-title">Actions</h2>
        <div class="std-page__body res-detail-list">
          <div v-for="(act, idx) in resolution.actions" :key="idx" class="action-item res-detail-card res-detail-card--action">
            <span v-if="act.type" class="res-detail-card-type res-detail-card-type--action">{{ act.type }}</span>
            <p v-if="act.subject" class="res-detail-card-subject">{{ act.subject }}</p>
            <div class="res-detail-richtext" v-html="asciidocify(act.message)"></div>
            <template v-if="act.dates">
              <div class="res-detail-dates">
                <span v-for="(d, didx) in act.dates" :key="didx" class="res-detail-date">
                  Effective: {{ d.start }}<template v-if="d.end"> &ndash; {{ d.end }}</template>
                </span>
              </div>
            </template>
          </div>
        </div>
      </section>

      <section v-if="resolution.approvals && resolution.approvals.length > 0" class="std-page__section">
        <h2 class="std-page__section-heading res-detail-section-title">Approval</h2>
        <div class="std-page__body">
          <div v-for="(app, idx) in resolution.approvals" :key="idx" class="approval-panel" :style="idx > 0 ? 'margin-top:1rem' : ''">
            <p style="color:var(--color-slate-700);">
              <strong v-if="app.degree" style="text-transform: capitalize; color:var(--color-slate-900);">{{ app.degree }}</strong>
              <template v-if="app.message"> &mdash; {{ app.message }}</template>
            </p>
          </div>
        </div>
      </section>

      <section v-if="resolution.categories && resolution.categories.length > 0" class="std-page__section">
        <h2 class="std-page__section-heading res-detail-section-title">Categories</h2>
        <div style="display:flex;flex-wrap:wrap;gap:0.5rem">
          <span v-for="(cat, idx) in resolution.categories" :key="idx" class="std-page__badge">{{ cat }}</span>
        </div>
      </section>

    </div>
  </div>
  <div v-else-if="!isLoaded" class="res-loading">
    <div class="loading-pulse">
      <div class="loading-pulse__line" style="width: 75%; height: 2rem;"></div>
      <div class="loading-pulse__line" style="width: 50%;"></div>
      <div class="loading-pulse__line" style="width: 100%; height: 8rem; margin-top: 2rem;"></div>
    </div>
  </div>
  <div v-else class="res-not-found">
    <div class="empty-state">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="empty-state__icon"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
      <h3>Resolution not found</h3>
      <p>The resolution you requested could not be found or does not exist.</p>
      <router-link to="/" class="std-chip" style="text-decoration:none;">View All Resolutions</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useResolutions } from '../composables/useResolutions'
import { asciidocify } from '../utils/asciidoc'

const route = useRoute()
const { resolutions, isLoaded, loadData } = useResolutions()

onMounted(() => {
  loadData()
})

const resolution = computed(() => {
  if (!isLoaded.value) return null

  const meetingId = route.params.meetingId as string
  const resolutionId = route.params.resolutionId as string
  if (meetingId && resolutionId) {
    return resolutions.value.find(r => r.source_file === meetingId && r.id === resolutionId)
  }

  const id = route.params.id as string
  if (id) {
    return resolutions.value.find(r => r.id === id)
  }
  return null
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
.res-detail-page {
  max-width: 56rem;
  margin: 0 auto;
}

.back-link {
  background: transparent;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: var(--color-slate-500);
  transition: color 0.2s;
  padding: 0;
}
.back-link:hover {
  color: var(--color-slate-900);
}
.dark .back-link:hover {
  color: white;
}
.back-link__icon {
  transition: transform 0.2s;
}
.back-link:hover .back-link__icon {
  transform: translateX(-4px);
}

.res-detail-header {
  margin-bottom: 3rem;
  border-bottom: 1px solid var(--color-slate-200);
  padding-bottom: 2rem;
}
.dark .res-detail-header {
  border-bottom-color: var(--color-slate-800);
}

.res-detail-meta {
  margin-bottom: 1rem;
}

.res-detail-badge--acclamation {
  background: #6366f1;
  color: white;
  border-color: transparent;
}

.res-detail-title {
  font-family: var(--font-serif);
  font-size: 1.875rem;
  color: var(--color-slate-900);
  line-height: 1.2;
  margin-bottom: 1rem;
}
@media (min-width: 768px) {
  .res-detail-title { font-size: 2.25rem; }
}
@media (min-width: 1024px) {
  .res-detail-title { font-size: 3rem; }
}
.dark .res-detail-title { color: white; }

.res-detail-subtitle {
  font-size: 1.125rem;
  color: var(--color-slate-500);
  font-style: italic;
}
.dark .res-detail-subtitle { color: var(--color-slate-400); }

.res-detail-content {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.res-detail-section-title {
  font-family: var(--font-serif);
  font-size: 1.25rem;
  color: var(--color-slate-800);
  border-bottom: 1px solid var(--color-slate-100);
  padding-bottom: 0.5rem;
  margin-bottom: 1.5rem;
}
@media (min-width: 768px) {
  .res-detail-section-title { font-size: 1.5rem; }
}
.dark .res-detail-section-title {
  color: var(--color-slate-200);
  border-bottom-color: var(--color-slate-800);
}

.res-detail-body {
  font-size: 1.125rem;
  line-height: 1.75;
  color: var(--color-slate-700);
}
.dark .res-detail-body { color: var(--color-slate-300); }

.res-detail-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.res-detail-card {
  background: var(--color-slate-50);
  padding: 1.5rem;
  border-radius: 0.75rem;
  border: 1px solid var(--color-slate-100);
}
.dark .res-detail-card {
  background: rgba(30, 41, 59, 0.5);
  border-color: var(--color-slate-800);
}

.res-detail-card--action {
  background: white;
  box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  border-color: var(--color-slate-200);
}
.dark .res-detail-card--action {
  background: var(--color-slate-900);
  border-color: var(--color-slate-700);
}

.res-detail-card-type {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--color-slate-500);
  margin-bottom: 0.75rem;
}
.dark .res-detail-card-type { color: var(--color-slate-400); }

.res-detail-card-type--action {
  color: var(--color-blue-accent);
}

.res-detail-card-subject {
  font-weight: 600;
  font-size: 1.125rem;
  color: var(--color-slate-900);
  margin-bottom: 0.75rem;
}
.dark .res-detail-card-subject { color: white; }

.res-detail-richtext {
  color: var(--color-slate-700);
  line-height: 1.75;
}
.dark .res-detail-richtext { color: var(--color-slate-300); }
.res-detail-richtext :deep(p) { margin-bottom: 1rem; }
.res-detail-richtext :deep(p:last-child) { margin-bottom: 0; }
.res-detail-richtext :deep(a) { color: var(--color-blue-accent); text-decoration: underline; }

.res-detail-dates {
  margin-top: 1rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.res-detail-date {
  display: inline-flex;
  align-items: center;
  padding: 0.125rem 0.625rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  background: var(--color-slate-100);
  color: var(--color-slate-800);
}
.dark .res-detail-date {
  background: var(--color-slate-800);
  color: var(--color-slate-300);
}

.res-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 6rem 1rem;
}

.res-not-found {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 6rem 1rem;
  text-align: center;
}

.empty-state {
  display: inline-block;
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
.empty-state p {
  color: var(--color-slate-500);
  margin-bottom: 1.5rem;
}

.loading-pulse {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 42rem;
  gap: 1rem;
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
.loading-pulse__line {
  height: 1rem;
  background-color: var(--color-slate-200);
  border-radius: 0.25rem;
}
.dark .loading-pulse__line {
  background-color: var(--color-slate-800);
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: .5; }
}
</style>

