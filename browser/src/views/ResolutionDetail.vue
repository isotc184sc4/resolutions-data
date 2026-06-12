<template>
  <div v-if="resolution" class="std-page">

    <!-- Back link -->
    <router-link to="/" class="std-page__back">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block;vertical-align:-3px;margin-right:0.375rem"><path d="m15 18-6-6 6-6"/></svg>
      All Resolutions
    </router-link>

    <!-- Header -->
    <header class="std-page__header">
      <div class="std-page__meta">
        <span v-if="resolution.is_acclamation" class="std-page__badge" style="background:#6366f1;color:#fff;">Acclamation</span>
        <span v-else-if="resolution.id" class="std-page__badge" style="font-family:'Noto Sans Mono',monospace;font-weight:600">{{ resolution.id }}</span>
        <span v-if="resolution.meeting_date" class="std-page__badge">{{ resolution.meeting_date }}</span>
        <span v-if="!resolution.is_acclamation" class="std-page__badge">
          <template v-if="resolution.source_type === 'plenary'">Plenary resolution</template>
          <template v-else-if="resolution.source_type === 'ballot'">Ballot resolution</template>
          <template v-else-if="resolution.source_type === '7372ma'">7372 MA resolution</template>
          <template v-else>Resolution</template>
        </span>
        <a v-if="resolution.group_id" :href="`/groups/${resolution.group_id}/`" class="std-page__badge std-page__badge--link">{{ resolution.group_id.toUpperCase() }}</a>
      </div>

      <h1 v-if="resolution.title" class="std-page__title">{{ resolution.title }}</h1>

      <p v-if="resolution.source_title" class="std-page__label" style="margin-top:0.5rem;font-style:italic">
        {{ resolution.source_title }}
        <template v-if="resolution.venue">({{ resolution.venue }})</template>
      </p>
    </header>

    <!-- Content -->
    <div class="std-page__content">

      <section v-if="resolution.subject" class="std-page__section">
        <h2 class="std-page__section-heading">Subject</h2>
        <div class="std-page__body">
          <p>{{ resolution.subject }}</p>
        </div>
      </section>

      <section v-if="resolution.considerations && resolution.considerations.length > 0" class="std-page__section">
        <h2 class="std-page__section-heading">Considerations</h2>
        <div class="std-page__body">
          <div v-for="(cons, idx) in resolution.considerations" :key="idx" class="consideration-item" :style="idx > 0 ? 'margin-top:1rem' : ''">
            <span v-if="cons.type" class="std-page__badge" style="margin-bottom:0.5rem; text-transform: capitalize;">{{ cons.type }}</span>
            <div v-html="asciidocify(cons.message)"></div>
          </div>
        </div>
      </section>

      <section v-if="resolution.actions && resolution.actions.length > 0" class="std-page__section">
        <h2 class="std-page__section-heading">Actions</h2>
        <div class="std-page__body">
          <div v-for="(act, idx) in resolution.actions" :key="idx" class="action-item" :style="idx > 0 ? 'margin-top:1rem' : ''">
            <span v-if="act.type" class="std-page__badge" style="margin-bottom:0.5rem; text-transform: capitalize;">{{ act.type }}</span>
            <p v-if="act.subject" style="font-weight:600;margin-bottom:0.25rem">{{ act.subject }}</p>
            <div v-html="asciidocify(act.message)"></div>
            <template v-if="act.dates">
              <p v-for="(d, didx) in act.dates" :key="didx" class="std-page__badge" style="margin-top:0.5rem">
                Effective: {{ d.start }}<template v-if="d.end"> &ndash; {{ d.end }}</template>
              </p>
            </template>
          </div>
        </div>
      </section>

      <section v-if="resolution.approvals && resolution.approvals.length > 0" class="std-page__section">
        <h2 class="std-page__section-heading">Approval</h2>
        <div class="std-page__body">
          <div v-for="(app, idx) in resolution.approvals" :key="idx" class="approval-panel" :style="idx > 0 ? 'margin-top:1rem' : ''">
            <p>
              <strong v-if="app.degree" style="text-transform: capitalize;">{{ app.degree }}</strong>
              <template v-if="app.message"> &mdash; {{ app.message }}</template>
            </p>
          </div>
        </div>
      </section>

      <section v-if="resolution.categories && resolution.categories.length > 0" class="std-page__section">
        <h2 class="std-page__section-heading">Categories</h2>
        <div style="display:flex;flex-wrap:wrap;gap:0.5rem">
          <span v-for="(cat, idx) in resolution.categories" :key="idx" class="std-page__badge">{{ cat }}</span>
        </div>
      </section>

    </div>
  </div>
  <div v-else-if="!isLoaded" style="padding-top: 5rem; padding-bottom: 5rem; text-align: center;">
    Loading...
  </div>
  <div v-else style="padding-top: 5rem; padding-bottom: 5rem; text-align: center; color: #64748b;">
    Resolution not found.
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
  const param = route.params.id as string
  const [source_file, id] = param.split('|')
  
  if (source_file && id) {
    return resolutions.value.find(r => r.source_file === source_file && r.id === id)
  }
  // Fallback if URL doesn't have the source file
  return resolutions.value.find(r => r.id === param)
})
</script>
