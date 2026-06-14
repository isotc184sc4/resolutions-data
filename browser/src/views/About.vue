<template>
  <div class="std-page about-page">
    <!-- Back link -->
    <button @click="$router.back()" class="back-link animate-up" style="--nth: 1">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="back-link__icon"><path d="m15 18-6-6 6-6"/></svg>
      Back
    </button>

    <!-- 1. Hero / Header -->
    <header class="about-header animate-up" style="--nth: 2">
      <h1 class="about-title">About This Archive</h1>
      <p class="about-subtitle">
        A digital record of 1,456 resolutions from ISO/TC 184/SC 4, spanning 1989 to today.
      </p>
    </header>

    <!-- Content Sections -->
    <div class="about-content">
      
      <!-- 2. The Edoxen Format -->
      <section class="about-section animate-up" style="--nth: 3">
        <h2 class="about-heading">The Edoxen Format</h2>
        <div class="about-body">
          <p>
            Resolutions in this archive are stored in plain-text YAML files using the <strong>Edoxen format</strong>. This structured representation ensures resolutions remain human-readable while being entirely machine-parsable.
          </p>
          <div class="code-wrapper">
            <pre class="code-block"><code><span class="code-key">metadata</span>:
  <span class="code-key">title</span>: <span class="code-string">Resolutions of the plenary meeting of ISO/TC 184/SC 4, Stavanger, Norway</span>
  <span class="code-key">dates</span>:
  - <span class="code-key">start</span>: <span class="code-string">'2024-10-18'</span>
    <span class="code-key">end</span>: <span class="code-string">'2024-10-25'</span>
    <span class="code-key">kind</span>: <span class="code-string">meeting</span>
  <span class="code-key">source</span>: <span class="code-string">ISO/TC 184/SC 4 Secretariat</span>
  <span class="code-key">venue</span>: <span class="code-string">Stavanger, Norway</span>

<span class="code-key">resolutions</span>:
- <span class="code-key">identifier</span>: <span class="code-string">'1142'</span>
  <span class="code-key">subject</span>: <span class="code-string">ISO/TC 184/SC 4 "Industrial data"</span>
  <span class="code-key">title</span>: <span class="code-string">Set 8-week ballot duration for new work item proposals</span>
  <span class="code-key">dates</span>:
  - <span class="code-key">start</span>: <span class="code-string">'2024-10-15'</span>
    <span class="code-key">kind</span>: <span class="code-string">decision</span>
  <span class="code-key">actions</span>:
  - <span class="code-key">type</span>: <span class="code-string">requests</span>
    <span class="code-key">message</span>: |<span class="code-string">
      SC 4 requests its Committee Manager to apply the
      8-week ballot duration to the following NP ballots...</span>
  <span class="code-key">considerations</span>:
  - <span class="code-key">type</span>: <span class="code-string">noting</span>
    <span class="code-key">message</span>: |<span class="code-string">
      SC 4 notes that shorter ballot durations...</span>
  <span class="code-key">approvals</span>:
  - <span class="code-key">degree</span>: <span class="code-string">unanimous</span>
    <span class="code-key">message</span>: <span class="code-string">Approved without objection</span></code></pre>
          </div>
          <p>
            Each file contains two main sections: <code>metadata</code>, containing information about the meeting, and a <code>resolutions</code> array, detailing the individual decisions made. A resolution includes its identifier, subject, title, relevant dates, any context under <code>considerations</code>, and the <code>actions</code> mandated by the committee.
          </p>
          <p>
            <a href="https://github.com/metanorma/edoxen" target="_blank" rel="noopener noreferrer" class="text-link">View the Edoxen schema on GitHub &rarr;</a>
          </p>
        </div>
      </section>

      <!-- 3. Action Types -->
      <section class="about-section animate-up" style="--nth: 4">
        <h2 class="about-heading">Action Types</h2>
        <div class="about-body">
          <p>
            Every resolution is composed of typed <code>actions</code> that categorize what the committee decided to do (e.g., requesting an action, approving a document, or thanking a host). This semantic typing allows for advanced filtering and analysis of the committee's historical activities.
          </p>
          <div class="action-grid">
            <span 
              v-for="chip in actionChips" 
              :key="chip.type"
              class="action-chip"
              :style="{ '--chip-bg': chip.bg, '--chip-text': chip.text }"
            >
              {{ chip.type }}
            </span>
          </div>
        </div>
      </section>

      <!-- 4. URN Identifiers -->
      <section class="about-section animate-up" style="--nth: 5">
        <h2 class="about-heading">URN Identifiers</h2>
        <div class="about-body">
          <p>
            Resources in this archive are assigned Uniform Resource Names (URNs) to provide persistent, location-independent identifiers.
          </p>
          <ul class="urn-list">
            <li>
              <strong>Resolution URNs:</strong>
              <code class="inline-code">urn:iso:tc:184:sc:4:resolution:{id}</code>
              <br><span class="urn-example">Example: <code class="inline-code">urn:iso:tc:184:sc:4:resolution:1142</code></span>
            </li>
            <li>
              <strong>Meeting URNs:</strong>
              <code class="inline-code">urn:iso:tc:184:sc:4:meeting:{source_file}</code>
              <br><span class="urn-example">Example: <code class="inline-code">urn:iso:tc:184:sc:4:meeting:plenary-2024-10-stavanger-norway</code></span>
            </li>
          </ul>
          <p class="urn-note">
            Note that per <a href="https://datatracker.ietf.org/doc/html/rfc5141" target="_blank" rel="noopener" class="text-link">RFC 5141</a>, "documents at or below the Technical Committee level" are not covered by the standard <code>urn:iso:std:</code> namespace. Section 2.6 delegates URN management for TC resources to the Technical Committees themselves.
          </p>
        </div>
      </section>

      <!-- 5. Data Pipeline -->
      <section class="about-section animate-up" style="--nth: 6">
        <h2 class="about-heading">Data Pipeline</h2>
        <div class="about-body">
          <div class="pipeline-steps">
            <div class="pipeline-step">
              <div class="pipeline-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
              </div>
              <h3 class="pipeline-title">1. YAML Source Files</h3>
              <p class="pipeline-desc">Authoritative plenary files maintained in the repository.</p>
            </div>
            
            <div class="pipeline-arrow">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </div>

            <div class="pipeline-step">
              <div class="pipeline-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
              </div>
              <h3 class="pipeline-title">2. Build Script</h3>
              <p class="pipeline-desc">Node.js process that parses YAML and generates static JSON assets.</p>
            </div>

            <div class="pipeline-arrow">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </div>

            <div class="pipeline-step">
              <div class="pipeline-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
              </div>
              <h3 class="pipeline-title">3. Client Search</h3>
              <p class="pipeline-desc">FlexSearch index built entirely in the browser at load time.</p>
            </div>

            <div class="pipeline-arrow">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </div>

            <div class="pipeline-step">
              <div class="pipeline-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
              </div>
              <h3 class="pipeline-title">4. Vue SPA</h3>
              <p class="pipeline-desc">The compiled application, deployed statically to GitHub Pages.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 6. About the Committee -->
      <section class="about-section animate-up" style="--nth: 7">
        <h2 class="about-heading">About {{ committee.name }}</h2>
        <div class="about-body">
          <div class="committee-card">
            <h3 class="committee-title">{{ committee.title }}</h3>
            <p class="committee-scope">{{ committee.scope }}</p>
            
            <div class="committee-stats">
              <div class="stat-item">
                <span class="stat-value">{{ committee.established }}</span>
                <span class="stat-label">Established</span>
              </div>
              <div class="stat-item">
                <span class="stat-value">{{ committee.publishedStandards }}</span>
                <span class="stat-label">Published Standards</span>
              </div>
              <div class="stat-item">
                <span class="stat-value">{{ committee.participatingMembers }}</span>
                <span class="stat-label">Participating Members</span>
              </div>
              <div class="stat-item">
                <span class="stat-value">{{ committee.observingMembers }}</span>
                <span class="stat-label">Observing Members</span>
              </div>
            </div>

            <div class="committee-links">
              <a :href="committee.links.isoCommittee" target="_blank" rel="noopener noreferrer" class="committee-link">
                Committee Page
              </a>
              <a :href="committee.links.committeeSite" target="_blank" rel="noopener noreferrer" class="committee-link">
                SC 4 Website
              </a>
              <a :href="committee.links.github" target="_blank" rel="noopener noreferrer" class="committee-link">
                GitHub Organization
              </a>
              <a :href="committee.links.linkedin" target="_blank" rel="noopener noreferrer" class="committee-link">
                LinkedIn
              </a>
            </div>
          </div>
        </div>
      </section>

    </div>
  </div>
</template>

<script setup lang="ts">
import { committee } from '../data/committee'
import { getActionColor } from '../data/actionTypes'

// Top action types by frequency (from data analysis)
const actionTypes = [
  'requests', 'thanks', 'appoints', 'approves', 'resolves', 'directs',
  'asks', 'encourages', 'accepts', 'instructs', 'nominates', 'decides',
  'agrees', 'adopts', 'establishes', 'welcomes', 'creates', 'recommends',
  'endorses', 'notes', 'recognizes', 'confirms', 'appreciation', 'allocates',
  'supports', 'disbands', 'acknowledges', 'assigns', 'appreciates'
]

// Compute colors for display
const actionChips = actionTypes.map(type => ({
  type,
  ...getActionColor(type)
}))
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

.about-page {
  max-width: 56rem;
  margin: 0 auto;
  padding-bottom: 4rem;
}

/* Back Link */
.back-link {
  background: transparent;
  border: none;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-slate-500);
  transition: color 0.2s;
  padding: 0;
  margin-bottom: 2rem;
}
.back-link:hover,
.back-link:focus-visible {
  color: var(--color-blue-accent);
  outline: none;
}
.dark .back-link:hover,
.dark .back-link:focus-visible {
  color: #66a3e0;
}
.back-link__icon {
  transition: transform 0.2s;
}
.back-link:hover .back-link__icon {
  transform: translateX(-4px);
}

/* Header */
.about-header {
  margin-bottom: 4rem;
}

.about-title {
  font-family: var(--font-serif);
  font-size: 2rem;
  color: var(--color-slate-900);
  line-height: 1.2;
  margin-bottom: 1rem;
}
@media (min-width: 768px) {
  .about-title { font-size: 2.75rem; }
}
@media (min-width: 1024px) {
  .about-title { font-size: 3.5rem; }
}
.dark .about-title { color: white; }

.about-subtitle {
  font-size: 1.125rem;
  color: var(--color-slate-500);
  font-style: italic;
  padding-left: 1rem;
  border-left: 2px solid var(--color-slate-200);
}
.dark .about-subtitle { 
  color: var(--color-slate-400);
  border-left-color: var(--color-slate-700);
}

/* Content Container */
.about-content {
  display: flex;
  flex-direction: column;
  gap: 4rem;
  background: white;
  padding: 3rem;
  border-radius: 1rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.025);
  border: 1px solid var(--color-slate-200);
}
@media (max-width: 768px) {
  .about-content {
    padding: 1.5rem;
    gap: 3rem;
  }
}
.dark .about-content {
  background: var(--color-slate-900);
  border-color: var(--color-slate-800);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
}

/* Sections */
.about-section {
  display: flex;
  flex-direction: column;
}

.about-heading {
  font-family: var(--font-serif);
  font-size: 1.25rem;
  color: var(--color-slate-900);
  border-bottom: 2px solid var(--color-slate-100);
  padding-bottom: 0.5rem;
  margin-bottom: 1.5rem;
  font-weight: 600;
  letter-spacing: -0.01em;
}
@media (min-width: 768px) {
  .about-heading { font-size: 1.5rem; }
}
.dark .about-heading {
  color: white;
  border-bottom-color: var(--color-slate-800);
}

.about-body {
  font-size: 1.125rem;
  line-height: 1.75;
  color: var(--color-slate-700);
}
.dark .about-body { color: var(--color-slate-300); }
.about-body p { margin-bottom: 1.5rem; }
.about-body p:last-child { margin-bottom: 0; }

.text-link {
  color: var(--color-blue-accent);
  text-decoration: underline;
  text-underline-offset: 4px;
  transition: color 0.2s;
}
.text-link:hover { color: #005090; }
.dark .text-link { color: #66a3e0; }
.dark .text-link:hover { color: #8cbdff; }

/* Code Blocks */
.code-wrapper {
  margin: 1.5rem 0;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  border: 1px solid var(--color-slate-200);
}
.dark .code-wrapper {
  border-color: var(--color-slate-700);
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.5);
}

.code-block {
  margin: 0;
  padding: 1.5rem;
  background: var(--color-slate-50);
  color: var(--color-slate-800);
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.875rem;
  line-height: 1.5;
  overflow-x: auto;
  white-space: pre;
}
.dark .code-block {
  background: #0f172a; /* Slate 950 */
  color: var(--color-slate-200);
}

/* Syntax Highlighting Fake Classes */
.code-key { color: #b91c1c; font-weight: 500; }
.code-string { color: #047857; }
.dark .code-key { color: #f87171; font-weight: 500; }
.dark .code-string { color: #34d399; }

/* Action Grid */
.action-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 1rem;
}

.action-chip {
  display: inline-block;
  font-size: 0.875rem;
  font-weight: 600;
  letter-spacing: 0.025em;
  text-transform: capitalize;
  padding: 0.375rem 0.875rem;
  border-radius: 9999px;
  background: var(--chip-bg);
  color: var(--chip-text);
  border: 1px solid rgba(0,0,0,0.05);
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}
.dark .action-chip {
  border-color: rgba(255,255,255,0.1);
}

/* URN List */
.urn-list {
  list-style: none;
  padding: 0;
  margin: 1.5rem 0;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.urn-list li {
  background: var(--color-slate-50);
  padding: 1.25rem;
  border-radius: 0.5rem;
  border: 1px solid var(--color-slate-100);
}
.dark .urn-list li {
  background: rgba(30, 41, 59, 0.5);
  border-color: var(--color-slate-800);
}
.urn-list strong {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--color-slate-900);
}
.dark .urn-list strong { color: white; }
.urn-example {
  display: inline-block;
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: var(--color-slate-500);
}

.inline-code {
  background: var(--color-slate-200);
  color: var(--color-slate-800);
  padding: 0.2rem 0.4rem;
  border-radius: 0.25rem;
  font-family: ui-monospace, SFMono-Regular, monospace;
  font-size: 0.875em;
}
.dark .inline-code {
  background: var(--color-slate-800);
  color: var(--color-slate-200);
}

.urn-note {
  font-size: 0.9375rem;
  color: var(--color-slate-500);
  border-left: 2px solid var(--color-blue-accent);
  padding-left: 1rem;
  background: rgba(var(--color-blue-accent-rgb, 14, 116, 144), 0.05);
  padding: 1rem;
  border-radius: 0 0.5rem 0.5rem 0;
}
.dark .urn-note {
  background: rgba(59, 130, 246, 0.1);
  color: var(--color-slate-400);
}

/* Data Pipeline */
.pipeline-steps {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  margin-top: 1.5rem;
}
@media (min-width: 768px) {
  .pipeline-steps {
    flex-direction: row;
    align-items: flex-start;
    justify-content: space-between;
  }
}

.pipeline-step {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  background: var(--color-slate-50);
  padding: 1.5rem;
  border-radius: 0.75rem;
  border: 1px solid var(--color-slate-100);
  width: 100%;
}
.dark .pipeline-step {
  background: rgba(30, 41, 59, 0.5);
  border-color: var(--color-slate-800);
}

.pipeline-icon {
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  background: var(--color-blue-accent);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}
.pipeline-title {
  font-weight: 600;
  font-size: 1rem;
  color: var(--color-slate-900);
  margin-bottom: 0.5rem;
}
.dark .pipeline-title { color: white; }

.pipeline-desc {
  font-size: 0.875rem;
  color: var(--color-slate-500);
  line-height: 1.4;
  margin: 0 !important;
}
.dark .pipeline-desc { color: var(--color-slate-400); }

.pipeline-arrow {
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-slate-300);
  padding: 1rem 0;
  transform: rotate(90deg);
}
@media (min-width: 768px) {
  .pipeline-arrow {
    transform: rotate(0deg);
    padding: 2.5rem 0 0;
  }
}
.dark .pipeline-arrow { color: var(--color-slate-600); }

/* Committee Section */
.committee-card {
  background: var(--color-slate-50);
  padding: 2rem;
  border-radius: 0.75rem;
  border: 1px solid var(--color-slate-100);
}
.dark .committee-card {
  background: rgba(30, 41, 59, 0.5);
  border-color: var(--color-slate-800);
}

.committee-title {
  font-family: var(--font-serif);
  font-size: 1.5rem;
  color: var(--color-slate-900);
  margin-bottom: 0.5rem;
}
.dark .committee-title { color: white; }

.committee-scope {
  font-size: 1rem;
  color: var(--color-slate-600);
  margin-bottom: 2rem !important;
  font-style: italic;
}
.dark .committee-scope { color: var(--color-slate-400); }

.committee-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}
@media (min-width: 640px) {
  .committee-stats { grid-template-columns: repeat(4, 1fr); }
}

.stat-item {
  display: flex;
  flex-direction: column;
}
.stat-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-blue-accent);
  line-height: 1.2;
}
.dark .stat-value { color: #66a3e0; }
.stat-label {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-slate-500);
  font-weight: 600;
}
.dark .stat-label { color: var(--color-slate-400); }

.committee-links {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  border-top: 1px solid var(--color-slate-200);
  padding-top: 1.5rem;
}
.dark .committee-links { border-top-color: var(--color-slate-700); }

.committee-link {
  display: inline-flex;
  align-items: center;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-slate-700);
  background: white;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  border: 1px solid var(--color-slate-200);
  text-decoration: none;
  transition: all 0.2s;
}
.dark .committee-link {
  background: var(--color-slate-800);
  color: var(--color-slate-200);
  border-color: var(--color-slate-700);
}
.committee-link:hover {
  border-color: var(--color-blue-accent);
  color: var(--color-blue-accent);
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.dark .committee-link:hover {
  border-color: #66a3e0;
  color: #66a3e0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.4);
}
</style>
